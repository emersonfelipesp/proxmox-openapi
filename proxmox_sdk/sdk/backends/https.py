"""Async HTTPS backend for the Proxmox SDK (aiohttp-based)."""

from __future__ import annotations

import asyncio
import io
import logging
import posixpath
import re
import ssl
from typing import TYPE_CHECKING, Any
from urllib.parse import urlsplit, urlunsplit

import aiohttp

from proxmox_sdk.sdk.auth.base import AuthStrategy
from proxmox_sdk.sdk.backends.base import AbstractBackend
from proxmox_sdk.sdk.exceptions import (
    ProxmoxConnectionError,
    ProxmoxTimeoutError,
    ResourceException,
)
from proxmox_sdk.sdk.resource import _filter_none

if TYPE_CHECKING:
    from proxmox_sdk.sdk.auth.ticket import TicketAuth
    from proxmox_sdk.sdk.services import ServiceConfig

logger = logging.getLogger(__name__)

# Files larger than this use streaming multipart encoding.
STREAMING_SIZE_THRESHOLD = 10 * 1024 * 1024  # 10 MiB

_IPV6_BARE = re.compile(r"^[0-9a-fA-F:]+$")
_IPV6_BRACKETED = re.compile(r"^\[([^\]]+)\](?::(\d+))?$")
_HOST_WITH_PORT = re.compile(r"^([^:\[]+):(\d+)$")


def _parse_host(host: str, default_port: int) -> tuple[str, int]:
    """Parse a host string into (normalised_netloc, port).

    Handles:
    - Plain hostname: ``pve.example.com`` → ``(pve.example.com, default_port)``
    - host:port: ``pve.example.com:8006`` → ``(pve.example.com, 8006)``
    - Bare IPv6: ``2001:db8::1`` → ``([2001:db8::1], default_port)``
    - Bracketed IPv6: ``[2001:db8::1]`` → ``([2001:db8::1], default_port)``
    - Bracketed IPv6 with port: ``[2001:db8::1]:8007`` → ``([2001:db8::1], 8007)``
    """
    # Bare IPv6 — multiple colons, no brackets
    if _IPV6_BARE.match(host) and host.count(":") > 1:
        return f"[{host}]", default_port

    # Bracketed IPv6 (with or without port)
    m = _IPV6_BRACKETED.match(host)
    if m:
        addr, port_str = m.group(1), m.group(2)
        return f"[{addr}]", int(port_str) if port_str else default_port

    # host:port (non-IPv6)
    m = _HOST_WITH_PORT.match(host)
    if m:
        return m.group(1), int(m.group(2))

    return host, default_port


def _build_base_url(
    host: str,
    port: int,
    path_prefix: str = "",
) -> str:
    """Build a base HTTPS URL from host components."""
    netloc, resolved_port = _parse_host(host, port)
    netloc = f"{netloc}:{resolved_port}"
    prefix = path_prefix.strip("/")
    path = f"/{prefix}" if prefix else ""
    return f"https://{netloc}{path}"


def _build_ssl_context(verify_ssl: bool, cert: str | None) -> ssl.SSLContext | bool:
    """Build an SSL context from configuration."""
    if not verify_ssl:
        return False
    ctx = ssl.create_default_context()
    if cert:
        # cert may be a CA bundle file or a client cert PEM.
        # Try CA bundle first; if that fails, fall back to client cert chain.
        # Log a warning on fallback so operators notice that custom CA verification
        # is NOT active (server cert will be validated against system CAs instead).
        try:
            ctx.load_verify_locations(cafile=cert)
        except ssl.SSLError:
            logger.warning(
                "cert %r could not be loaded as a CA bundle (ssl.SSLError); "
                "treating it as a client cert chain instead. "
                "Custom CA will NOT be used for server certificate verification — "
                "verification will fall back to system CAs.",
                cert,
            )
            ctx.load_cert_chain(cert)
    return ctx


class HttpsBackend(AbstractBackend):
    """Async HTTPS backend — the primary way to connect to a real Proxmox service.

    Supports:
    - Password auth with automatic ticket renewal and 2FA/TOTP
    - API token auth (stateless)
    - IPv6 host normalization
    - Reverse-proxy path prefix
    - HTTP proxy
    - Configurable SSL/TLS and client certificates
    - File upload (small: in-memory, large: aiohttp streaming multipart)
    - None-value filtering on params and data

    Example::

        backend = HttpsBackend(
            host="pve.example.com",
            service_config=SERVICES["PVE"],
            auth=TicketAuth(username="admin@pam", password="secret", ...),
            verify_ssl=False,
        )
        async with backend:
            nodes = await backend.request("GET", "/api2/json/nodes")
    """

    def __init__(
        self,
        *,
        host: str,
        service_config: ServiceConfig,
        auth: AuthStrategy,
        port: int | None = None,
        path_prefix: str = "",
        verify_ssl: bool = True,
        cert: str | None = None,
        timeout: int = 5,
        connect_timeout: int | None = None,
        proxies: dict[str, str] | None = None,
        max_retries: int = 0,
        retry_backoff: float = 0.5,
    ) -> None:
        resolved_port = port if port is not None else service_config.default_port
        self._base_url = _build_base_url(host, resolved_port, path_prefix)
        # Cache parsed URL components to avoid re-parsing on every _url_for() call.
        _parsed = urlsplit(self._base_url)
        self._base_scheme = _parsed.scheme
        self._base_netloc = _parsed.netloc
        self._base_path = _parsed.path or "/"
        self._service_config = service_config
        self._auth = auth
        self._ssl = _build_ssl_context(verify_ssl, cert)
        self._timeout = aiohttp.ClientTimeout(total=timeout, connect=connect_timeout)
        _proxies = proxies or {}
        self._proxy = _proxies.get("https") or _proxies.get("http")
        self._max_retries = max_retries
        self._retry_backoff = retry_backoff

        self._session: aiohttp.ClientSession | None = None
        self._session_loop: asyncio.AbstractEventLoop | None = None
        self._ticket_url = f"{self._base_url}/access/ticket"

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------

    async def __aenter__(self) -> HttpsBackend:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # AbstractBackend interface
    # ------------------------------------------------------------------

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Execute an HTTPS request against the Proxmox API."""
        session = await self._ensure_session()
        await self._ensure_authenticated(session)

        clean_params = (_filter_none(params) or None) if params else None
        clean_data = _filter_none(data) if data else None

        method = method.upper()
        url = self._url_for(path)
        headers = {
            "Accept": "application/json",
            **self._auth.build_headers(method),
        }
        cookies = self._auth.build_cookies()
        proxy = self._proxy

        # Detect file uploads (io.IOBase values in data dict)
        if clean_data and _has_file(clean_data):
            return await self._upload(
                session, method, url, clean_data, headers, cookies, clean_params, proxy
            )

        # Regular JSON request
        json_body = clean_data if method not in ("GET", "DELETE") else None
        if method in ("GET", "DELETE") and clean_data:
            # For GET/DELETE, merge data into params (edge cases)
            if clean_params:
                clean_params.update(clean_data)
            else:
                clean_params = clean_data
            json_body = None

        # Only safe methods are retried to avoid accidental double-mutation.
        is_safe = method in ("GET", "HEAD")
        attempts = self._max_retries + 1 if is_safe else 1
        last_exc: ResourceException | None = None

        for attempt in range(attempts):
            if attempt > 0:
                delay = min(self._retry_backoff * (2 ** (attempt - 1)), 30.0)
                await asyncio.sleep(delay)

            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    cookies=cookies,
                    params=clean_params,
                    json=json_body,
                    ssl=self._ssl,
                    timeout=self._timeout,
                    proxy=proxy,
                ) as resp:
                    return await self._handle_response(resp, method, path)

            except asyncio.TimeoutError as exc:
                logger.warning("Request timed out: %s %s (attempt %d)", method, path, attempt + 1)
                last_exc = ProxmoxTimeoutError(f"Request timed out: {method} {path}")
                last_exc.__cause__ = exc

            except aiohttp.ClientSSLError as exc:
                # SSL errors are not transient; raise immediately without retry.
                logger.error("SSL error: %s %s — %s", method, path, exc)
                raise ProxmoxConnectionError(f"SSL error connecting to Proxmox API: {exc}") from exc

            except aiohttp.ClientConnectorError as exc:
                logger.warning(
                    "Cannot connect to Proxmox API: %s %s — %s (attempt %d)",
                    method,
                    path,
                    exc,
                    attempt + 1,
                )
                last_exc = ProxmoxConnectionError(f"Cannot connect to Proxmox API: {exc}")
                last_exc.__cause__ = exc

            except aiohttp.ClientError as exc:
                logger.warning(
                    "HTTPS request failed: %s %s — %s (attempt %d)",
                    method,
                    path,
                    exc,
                    attempt + 1,
                )
                last_exc = ProxmoxConnectionError(f"Network error: {exc}")
                last_exc.__cause__ = exc

            except ResourceException as exc:
                if exc.status_code in (502, 503, 504):
                    logger.warning(
                        "Retryable HTTP %d: %s %s (attempt %d)",
                        exc.status_code,
                        method,
                        path,
                        attempt + 1,
                    )
                    last_exc = exc
                else:
                    raise

        assert last_exc is not None
        raise last_exc

    async def close(self) -> None:
        """Close the underlying aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = None
            self._session_loop = None
            return

        current_loop = asyncio.get_running_loop()
        if self._session_loop is None or self._session_loop is current_loop:
            await self._session.close()
        else:
            logger.debug(
                "close() called from different loop than session creation; "
                "scheduling close on original loop"
            )
            try:
                if self._session_loop.is_running():

                    def _schedule_close() -> None:
                        asyncio.create_task(self._session.close())

                    self._session_loop.call_soon_threadsafe(_schedule_close)
            except Exception:
                logger.debug("Failed to schedule session close on original loop", exc_info=True)

        self._session = None
        self._session_loop = None

    # ------------------------------------------------------------------
    # Token access
    # ------------------------------------------------------------------

    async def get_tokens(self) -> tuple[str, str]:
        """Return (ticket, csrf_token) for the HTTPS ticket-auth backend.

        Raises:
            RuntimeError: If token auth is used (no ticket exists).
        """
        from proxmox_sdk.sdk.auth.ticket import TicketAuth

        if not isinstance(self._auth, TicketAuth):
            raise RuntimeError("get_tokens() is only available with password/ticket auth")
        if not self._auth.is_authenticated:
            session = await self._ensure_session()
            await self._ensure_authenticated(session)
        assert self._auth._ticket and self._auth._csrf_token
        return self._auth._ticket, self._auth._csrf_token

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _ensure_session(self) -> aiohttp.ClientSession:
        current_loop = asyncio.get_running_loop()

        if (
            self._session is not None
            and not self._session.closed
            and self._session_loop is not None
            and self._session_loop is not current_loop
        ):
            logger.warning(
                "Detected aiohttp session loop mismatch; rebuilding session on current loop"
            )
            old_session = self._session
            old_loop = self._session_loop
            self._session = None
            self._session_loop = None

            # Attempt best-effort cleanup on the loop that owns the old session.
            try:
                if old_loop.is_running():

                    def _schedule_close() -> None:
                        asyncio.create_task(old_session.close())

                    old_loop.call_soon_threadsafe(_schedule_close)
            except Exception:
                logger.debug("Failed to schedule stale aiohttp session close", exc_info=True)

        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector()
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=self._timeout,
            )
            self._session_loop = current_loop
        return self._session

    async def _ensure_authenticated(self, session: aiohttp.ClientSession) -> None:
        await self._auth.ensure_ready(session, self._ticket_url, ssl=self._ssl, proxy=self._proxy)

    def _url_for(self, path: str) -> str:
        """Build full URL from a path, respecting path prefix."""
        # Avoid double-prefixing: if path already starts with base_url, return it
        if path.startswith("http://") or path.startswith("https://"):
            return path
        joined_path = posixpath.join(self._base_path, path.lstrip("/"))
        return urlunsplit((self._base_scheme, self._base_netloc, joined_path, "", ""))

    async def _handle_response(
        self,
        resp: aiohttp.ClientResponse,
        method: str,
        path: str,
    ) -> Any:
        """Parse and unwrap a Proxmox API response."""
        try:
            raw = await resp.json(content_type=None)
        except Exception:
            raw = {"data": await resp.text()}

        if resp.status >= 400:
            errors = raw.get("errors") if isinstance(raw, dict) else None
            content = raw.get("data", "") if isinstance(raw, dict) else str(raw)
            raise ResourceException(
                status_code=resp.status,
                status_message=resp.reason or "",
                content=str(content),
                errors=errors,
            )

        if isinstance(raw, dict) and "data" in raw:
            return raw["data"]
        return raw

    async def _upload(
        self,
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        data: dict[str, Any],
        headers: dict[str, str],
        cookies: dict[str, str],
        params: dict[str, Any] | None,
        proxy: str | None,
    ) -> Any:
        """Handle multipart file uploads using aiohttp FormData."""
        form = aiohttp.FormData()
        for key, value in data.items():
            if isinstance(value, io.IOBase):
                filename = getattr(value, "name", key)
                if hasattr(filename, "split"):
                    import os

                    filename = os.path.basename(filename)
                form.add_field(key, value, filename=filename)
            else:
                form.add_field(key, str(value))

        # Remove Content-Type so aiohttp sets multipart boundary
        upload_headers = {k: v for k, v in headers.items() if k.lower() != "content-type"}

        try:
            async with session.request(
                method=method,
                url=url,
                headers=upload_headers,
                cookies=cookies,
                data=form,
                params=params,
                ssl=self._ssl,
                timeout=aiohttp.ClientTimeout(total=3600),  # uploads can be slow
                proxy=proxy,
            ) as resp:
                return await self._handle_response(resp, method, url)

        except aiohttp.ClientError as exc:
            raise ResourceException(
                status_code=503,
                status_message="Service Unavailable",
                content=f"File upload failed: {exc}",
            ) from exc

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_config(
        cls,
        config: Any,  # ProxmoxConfig — avoid circular import
        service_config: ServiceConfig,
    ) -> HttpsBackend:
        """Build an HttpsBackend from a ProxmoxConfig dataclass."""
        from proxmox_sdk.sdk.auth.ticket import TicketAuth
        from proxmox_sdk.sdk.auth.token import TokenAuth, parse_token_id

        if config.token_id and config.token_secret:
            user, token_name = parse_token_id(config.token_id)
            auth: TicketAuth | TokenAuth = TokenAuth(
                user=user,
                token_name=token_name,
                token_value=config.token_secret,
                service_config=service_config,
            )
        else:
            auth = TicketAuth(
                username=config.username or "",
                password=config.password or "",
                service_config=service_config,
                otp=getattr(config, "otp", None),
                otptype=getattr(config, "otptype", "totp"),
            )

        # Extract host from api_url
        parsed = urlsplit(str(config.api_url))
        host = parsed.netloc or parsed.path

        return cls(
            host=host,
            service_config=service_config,
            auth=auth,
            verify_ssl=config.verify_ssl,
            cert=getattr(config, "cert", None),
            timeout=getattr(config, "timeout", 5),
            connect_timeout=getattr(config, "connect_timeout", None),
            proxies=getattr(config, "proxies", None),
            path_prefix=getattr(config, "path_prefix", ""),
            max_retries=getattr(config, "max_retries", 0),
            retry_backoff=getattr(config, "retry_backoff", 0.5),
        )


def _has_file(data: dict[str, Any]) -> bool:
    """True if any value in the dict is a file-like object."""
    return any(isinstance(v, io.IOBase) for v in data.values())


__all__ = ["HttpsBackend", "STREAMING_SIZE_THRESHOLD"]
