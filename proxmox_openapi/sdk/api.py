"""ProxmoxSDK — main entry point for the Proxmox OpenAPI SDK."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from proxmox_openapi.sdk.sync import SyncProxmoxSDK

from proxmox_openapi.sdk.auth.token import parse_token_id
from proxmox_openapi.sdk.backends.base import AbstractBackend
from proxmox_openapi.sdk.resource import ProxmoxResource
from proxmox_openapi.sdk.services import SERVICES, ServiceConfig

logger = logging.getLogger(__name__)


class ProxmoxSDK:
    """Async Python SDK for the Proxmox API.

    Provides dynamic, attribute-based navigation of the Proxmox REST API
    over multiple transport backends (HTTPS, SSH, local pvesh, or in-memory
    mock).  No FastAPI server required.

    Quick start (async context manager)::

        async with ProxmoxSDK(
            host="pve.example.com",
            user="admin@pam",
            password="secret",
            verify_ssl=False,
        ) as proxmox:
            nodes = await proxmox.nodes.get()
            vms   = await proxmox.nodes("pve1").qemu.get()

    Token auth::

        proxmox = ProxmoxSDK(
            host="pve.example.com",
            user="monitoring@pve",
            token_name="api-read",
            token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        )

    Mock mode (no real Proxmox)::

        async with ProxmoxSDK.mock() as proxmox:
            nodes = await proxmox.nodes.get()

    SSH backend::

        proxmox = ProxmoxSDK(
            host="pve.example.com",
            user="root",
            password="secret",
            backend="ssh_paramiko",
        )

    Local backend (on Proxmox host)::

        proxmox = ProxmoxSDK(backend="local", service="PVE")

    Sync usage::

        proxmox = ProxmoxSDK.sync(host=..., user=..., password=...)
        nodes = proxmox.nodes.get()
    """

    def __init__(
        self,
        host: str | None = None,
        *,
        _backend: AbstractBackend | None = None,
        user: str | None = None,
        password: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        otp: str | None = None,
        otptype: str = "totp",
        service: Literal["PVE", "PMG", "PBS"] = "PVE",
        backend: str = "https",
        port: int | None = None,
        path_prefix: str = "",
        verify_ssl: bool = True,
        cert: str | None = None,
        timeout: int = 5,
        proxies: dict[str, str] | None = None,
        sudo: bool = False,
        private_key_file: str | None = None,
        identity_file: str | None = None,
        forward_ssh_agent: bool = False,
        config_file: str | None = None,
    ) -> None:
        service_upper = service.upper()
        if service_upper not in SERVICES:
            raise ValueError(f"Unknown service '{service}'. Supported: {list(SERVICES.keys())}")
        svc: ServiceConfig = SERVICES[service_upper]

        if _backend is not None:
            # Caller-supplied backend — skip factory entirely (e.g. for testing).
            self._service_config = svc
            self._backend_name = "custom"
            self._backend = _backend
            self._root = ProxmoxResource(path=svc.api_path_prefix, backend=self._backend)
            return

        if backend not in svc.supported_backends:
            raise ValueError(
                f"Backend '{backend}' is not supported for service '{service_upper}'. "
                f"Supported backends: {list(svc.supported_backends)}"
            )

        self._service_config = svc
        self._backend_name = backend
        self._backend = self._create_backend(
            backend=backend,
            host=host,
            user=user,
            password=password,
            token_name=token_name,
            token_value=token_value,
            otp=otp,
            otptype=otptype,
            service_config=svc,
            port=port,
            path_prefix=path_prefix,
            verify_ssl=verify_ssl,
            cert=cert,
            timeout=timeout,
            proxies=proxies,
            sudo=sudo,
            private_key_file=private_key_file,
            identity_file=identity_file,
            forward_ssh_agent=forward_ssh_agent,
            config_file=config_file,
        )
        self._root: ProxmoxResource = ProxmoxResource(
            path=svc.api_path_prefix,
            backend=self._backend,
        )

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> ProxmoxResource:
        """Return the root ProxmoxResource for API navigation."""
        return self._root

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # Direct navigation (use without context manager)
    # ------------------------------------------------------------------

    def __getattr__(self, item: str) -> ProxmoxResource:
        """Delegate attribute access to the root resource.

        Allows usage without the context manager::

            proxmox = ProxmoxSDK(...)
            nodes = await proxmox.nodes.get()
            await proxmox.close()
        """
        if item.startswith("_"):
            raise AttributeError(item)
        return getattr(self._root, item)

    def __call__(self, resource_id: str | int | list | tuple | None = None) -> ProxmoxResource:
        """Delegate call to the root resource."""
        return self._root(resource_id)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def close(self) -> None:
        """Release all backend resources (sessions, connections)."""
        await self._backend.close()

    # ------------------------------------------------------------------
    # Token access
    # ------------------------------------------------------------------

    async def get_tokens(self) -> tuple[str, str]:
        """Return (ticket, csrf_token) for HTTPS password-auth backends.

        Useful when you need to pass Proxmox auth tokens to another system.

        Raises:
            RuntimeError: If not using HTTPS + ticket auth.
        """
        return await self._backend.get_tokens()

    # ------------------------------------------------------------------
    # Class-method constructors
    # ------------------------------------------------------------------

    @classmethod
    def mock(
        cls,
        schema_version: str = "latest",
        service: Literal["PVE", "PMG", "PBS"] = "PVE",
    ) -> ProxmoxSDK:
        """Create a ProxmoxSDK instance backed by the in-memory mock.

        No real Proxmox host required.  Useful for tests and development.

        Example::

            async with ProxmoxSDK.mock() as proxmox:
                nodes = await proxmox.nodes.get()
        """
        instance = object.__new__(cls)
        svc = SERVICES[service.upper()]

        from proxmox_openapi.sdk.backends.mock import MockBackend

        backend = MockBackend(schema_version=schema_version, api_path_prefix=svc.api_path_prefix)
        instance._service_config = svc
        instance._backend_name = "mock"
        instance._backend = backend
        instance._root = ProxmoxResource(path=svc.api_path_prefix, backend=backend)
        return instance

    @classmethod
    def from_config(cls, config: Any) -> ProxmoxSDK:
        """Create a ProxmoxSDK instance from a ProxmoxConfig dataclass.

        Args:
            config: A :class:`~proxmox_openapi.proxmox.config.ProxmoxConfig` instance.

        Example::

            config = ProxmoxConfig.from_env()
            proxmox = ProxmoxSDK.from_config(config)
        """
        service = getattr(config, "service", "PVE")
        backend_name = getattr(config, "backend", "https")

        if backend_name == "mock" or getattr(config, "api_mode", "real") == "mock":
            schema_version = getattr(config, "schema_version", "latest")
            return cls.mock(schema_version=schema_version, service=service)

        # Extract credentials from ProxmoxConfig
        token_id: str | None = config.token_id
        token_secret: str | None = config.token_secret
        token_name: str | None = None
        token_value: str | None = None

        if token_id and token_secret:
            user, token_name = parse_token_id(token_id)
            token_value = token_secret
        else:
            user = config.username

        # Extract host from api_url
        from urllib.parse import urlsplit

        parsed = urlsplit(str(config.api_url or ""))
        host = parsed.netloc or parsed.path or "localhost"

        return cls(
            host=host,
            user=user,
            password=config.password,
            token_name=token_name,
            token_value=token_value,
            service=service,
            backend=backend_name,
            verify_ssl=config.verify_ssl,
            cert=getattr(config, "cert", None),
            timeout=getattr(config, "timeout", 5),
            proxies=getattr(config, "proxies", None),
            path_prefix=getattr(config, "path_prefix", ""),
            port=getattr(config, "port", None),
            otp=getattr(config, "otp", None),
            otptype=getattr(config, "otptype", "totp"),
        )

    @classmethod
    def sync(cls, **kwargs: Any) -> "SyncProxmoxSDK":
        """Create a synchronous wrapper for environments without async/await.

        Example::

            with ProxmoxSDK.sync(
                host="pve.example.com",
                user="admin@pam",
                password="secret",
            ) as proxmox:
                nodes = proxmox.nodes.get()
        """
        from proxmox_openapi.sdk.sync import SyncProxmoxSDK

        return SyncProxmoxSDK(**kwargs)

    @classmethod
    def sync_mock(
        cls,
        schema_version: str = "latest",
        service: Literal["PVE", "PMG", "PBS"] = "PVE",
    ) -> "SyncProxmoxSDK":
        """Create a synchronous mock SDK instance.

        No real Proxmox host required.  Useful for tests and development.
        All API calls block synchronously (no `async/await` needed).

        Args:
            schema_version: Proxmox schema version tag (default: "latest").
            service: Service type (default: "PVE").

        Returns:
            A SyncProxmoxSDK instance ready for blocking API calls.

        Example::

            with ProxmoxSDK.sync_mock() as proxmox:
                nodes = proxmox.nodes.get()
                vms = proxmox.nodes("pve").qemu.get()
        """
        from proxmox_openapi.sdk.sync import SyncProxmoxSDK

        instance = object.__new__(SyncProxmoxSDK)
        import asyncio

        instance._loop = asyncio.new_event_loop()
        instance._sdk = cls.mock(schema_version=schema_version, service=service)
        from proxmox_openapi.sdk.sync import SyncProxmoxResource

        instance._root = SyncProxmoxResource(instance._sdk._root, instance._loop)
        return instance

    # ------------------------------------------------------------------
    # Internal: backend factory
    # ------------------------------------------------------------------

    @staticmethod
    def _create_backend(  # noqa: C901
        *,
        backend: str,
        host: str | None,
        user: str | None,
        password: str | None,
        token_name: str | None,
        token_value: str | None,
        otp: str | None,
        otptype: str,
        service_config: ServiceConfig,
        port: int | None,
        path_prefix: str,
        verify_ssl: bool,
        cert: str | None,
        timeout: int,
        proxies: dict[str, str] | None,
        sudo: bool,
        private_key_file: str | None,
        identity_file: str | None,
        forward_ssh_agent: bool,
        config_file: str | None,
    ) -> Any:
        if backend == "mock":
            from proxmox_openapi.sdk.backends.mock import MockBackend

            return MockBackend(api_path_prefix=service_config.api_path_prefix)

        if backend == "local":
            from proxmox_openapi.sdk.backends.local import LocalBackend

            return LocalBackend(service_config=service_config, sudo=sudo)

        if backend == "https":
            from proxmox_openapi.sdk.auth.ticket import TicketAuth
            from proxmox_openapi.sdk.auth.token import TokenAuth
            from proxmox_openapi.sdk.backends.https import HttpsBackend

            if not host:
                raise ValueError("'host' is required for the HTTPS backend")

            if token_name and token_value:
                auth = TokenAuth(
                    user=user or "",
                    token_name=token_name,
                    token_value=token_value,
                    service_config=service_config,
                )
            elif user and password:
                auth = TicketAuth(
                    username=user,
                    password=password,
                    service_config=service_config,
                    otp=otp,
                    otptype=otptype,
                )
            else:
                raise ValueError(
                    "HTTPS backend requires either (user + password) "
                    "or (user + token_name + token_value)"
                )

            return HttpsBackend(
                host=host,
                service_config=service_config,
                auth=auth,
                port=port,
                path_prefix=path_prefix,
                verify_ssl=verify_ssl,
                cert=cert,
                timeout=timeout,
                proxies=proxies,
            )

        if backend == "ssh_paramiko":
            from proxmox_openapi.sdk.backends.ssh_paramiko import SshParamikoBackend

            if not host:
                raise ValueError("'host' is required for the ssh_paramiko backend")
            if not user:
                raise ValueError("'user' is required for the ssh_paramiko backend")

            return SshParamikoBackend(
                host=host,
                user=user,
                service_config=service_config,
                password=password,
                private_key_file=private_key_file,
                sudo=sudo,
            )

        if backend == "openssh":
            from proxmox_openapi.sdk.backends.openssh import OpenSshBackend

            if not host:
                raise ValueError("'host' is required for the openssh backend")
            if not user:
                raise ValueError("'user' is required for the openssh backend")

            return OpenSshBackend(
                host=host,
                user=user,
                service_config=service_config,
                password=password,
                identity_file=identity_file,
                forward_ssh_agent=forward_ssh_agent,
                config_file=config_file,
                sudo=sudo,
            )

        raise ValueError(
            f"Unknown backend '{backend}'. Supported: https, ssh_paramiko, openssh, local, mock"
        )


__all__ = ["ProxmoxSDK"]
