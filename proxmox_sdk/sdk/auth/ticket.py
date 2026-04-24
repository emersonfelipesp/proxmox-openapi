"""Password / ticket authentication with automatic renewal and 2FA support."""

from __future__ import annotations

import asyncio
import time
from typing import TYPE_CHECKING, Any

import aiohttp

from proxmox_sdk.sdk.exceptions import AuthenticationError

if TYPE_CHECKING:
    from proxmox_sdk.sdk.services import ServiceConfig

# Proxmox tickets are valid for 2 hours; renew after 1 hour (same as proxmoxer).
_TICKET_RENEW_INTERVAL: float = 3600.0


class TicketAuth:
    """Stateful password-based authentication handler.

    Authenticates once via ``POST /access/ticket``, stores the resulting
    ticket and CSRF token, and auto-renews before the ticket expires.
    Supports TOTP / OTP two-factor authentication.

    Usage::

        auth = TicketAuth(
            username="admin@pam",
            password="secret",
            service_config=SERVICES["PVE"],
        )
        await auth.authenticate(session, ticket_url)
        headers = auth.build_headers("POST")
        cookies = auth.build_cookies()
    """

    def __init__(
        self,
        *,
        username: str,
        password: str,
        service_config: ServiceConfig,
        otp: str | None = None,
        otptype: str = "totp",
    ) -> None:
        self._username = username
        self._password = password
        self._service_config = service_config
        self._otp = otp
        self._otptype = otptype

        self._ticket: str | None = None
        self._csrf_token: str | None = None
        self._acquired_at: float | None = None

    @property
    def is_authenticated(self) -> bool:
        """True if a valid ticket is held."""
        return self._ticket is not None

    async def authenticate(
        self,
        session: aiohttp.ClientSession,
        ticket_url: str,
        *,
        ssl: Any = None,
        proxy: str | None = None,
    ) -> None:
        """Perform the initial authentication flow.

        Args:
            session: Active aiohttp session to use for the auth request.
            ticket_url: Full URL for ``POST /access/ticket``.
            ssl: SSL context or bool to control certificate verification.
                Defaults to None (aiohttp's default). Pass the backend's
                SSL context to ensure consistent verification behaviour.
            proxy: HTTP proxy URL, forwarded to the auth POST request.

        Raises:
            AuthenticationError: If authentication fails.
        """
        ticket, csrf = await self._request_ticket(
            session, ticket_url, self._password, ssl=ssl, proxy=proxy
        )

        # Two-factor authentication: server signals NeedTFA
        if ticket == "NeedTFA" or (ticket and ticket.startswith("NeedTFA")):
            if not self._otp:
                raise AuthenticationError(
                    "Two-factor authentication required but no OTP code provided. "
                    "Pass otp=<code> when creating ProxmoxSDK."
                )
            ticket, csrf = await self._request_ticket(
                session,
                ticket_url,
                self._otp,
                tfa_challenge=ticket,
                ssl=ssl,
                proxy=proxy,
            )

        self._ticket = ticket
        self._csrf_token = csrf
        self._acquired_at = time.monotonic()

    async def maybe_renew(
        self,
        session: aiohttp.ClientSession,
        ticket_url: str,
        *,
        ssl: Any = None,
        proxy: str | None = None,
    ) -> None:
        """Renew the ticket if it is approaching expiration.

        Called before every request by the HTTPS backend.
        """
        if self._acquired_at is None:
            return
        age = time.monotonic() - self._acquired_at
        if age >= _TICKET_RENEW_INTERVAL:
            # Use current ticket as password for renewal (Proxmox supports this)
            assert self._ticket is not None
            ticket, csrf = await self._request_ticket(
                session, ticket_url, self._ticket, ssl=ssl, proxy=proxy
            )
            self._ticket = ticket
            self._csrf_token = csrf
            self._acquired_at = time.monotonic()

    async def ensure_ready(
        self,
        session: aiohttp.ClientSession,
        ticket_url: str,
        *,
        ssl: Any = None,
        proxy: str | None = None,
    ) -> None:
        """Authenticate or renew the ticket as needed before a request."""
        if not self.is_authenticated:
            await self.authenticate(session, ticket_url, ssl=ssl, proxy=proxy)
        else:
            await self.maybe_renew(session, ticket_url, ssl=ssl, proxy=proxy)

    def build_headers(self, method: str) -> dict[str, str]:
        """Return request headers for the given HTTP method."""
        headers: dict[str, str] = {}
        if self._ticket and method.upper() not in ("GET", "HEAD") and self._csrf_token:
            headers["CSRFPreventionToken"] = self._csrf_token
        return headers

    def build_cookies(self) -> dict[str, str]:
        """Return cookie dict carrying the auth ticket."""
        if not self._ticket:
            return {}
        return {self._service_config.auth_cookie_name: self._ticket}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _request_ticket(
        self,
        session: aiohttp.ClientSession,
        ticket_url: str,
        password: str,
        *,
        tfa_challenge: str | None = None,
        ssl: Any = None,
        proxy: str | None = None,
    ) -> tuple[str, str]:
        """POST to /access/ticket and return (ticket, csrf_token).

        Args:
            session: aiohttp session.
            ticket_url: Full URL for the ticket endpoint.
            password: Password or OTP code (for the second 2FA step).
            tfa_challenge: The challenge ticket returned in the first 2FA step.
            proxy: HTTP proxy URL to use for this request.

        Returns:
            Tuple of (ticket, csrf_prevention_token).

        Raises:
            AuthenticationError: On failure.
        """
        payload: dict[str, Any] = {
            "username": self._username,
            "password": password,
        }
        if tfa_challenge is not None:
            payload["tfa-challenge"] = tfa_challenge

        try:
            async with session.post(ticket_url, data=payload, ssl=ssl, proxy=proxy) as response:
                raw = await response.json(content_type=None)

                if response.status != 200:
                    detail = raw.get("errors") or raw.get("data") or str(raw)
                    raise AuthenticationError(
                        f"Proxmox authentication failed (HTTP {response.status}): {detail}"
                    )

                data: dict[str, Any] = raw.get("data") or {}
                ticket: str | None = data.get("ticket")
                csrf: str | None = data.get("CSRFPreventionToken")

                if not ticket:
                    raise AuthenticationError(
                        "Authentication succeeded but no ticket returned — "
                        "check username format (e.g. user@pam) and credentials."
                    )

                return ticket, csrf or ""

        except asyncio.TimeoutError as exc:
            raise AuthenticationError(
                f"Proxmox authentication timed out connecting to {ticket_url}"
            ) from exc
        except aiohttp.ClientError as exc:
            raise AuthenticationError(
                f"Network error during Proxmox authentication: {exc}"
            ) from exc


__all__ = ["TicketAuth"]
