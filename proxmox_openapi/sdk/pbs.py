"""PBS (Proxmox Backup Server) SDK convenience module.

Provides :class:`PBSSDK` — a drop-in replacement for :class:`~proxmox_openapi.sdk.ProxmoxSDK`
pre-configured for PBS (port 8007, token separator ``:``, PBS auth cookie).

The same attribute-based API navigation is available — PBS endpoints are accessible
directly as resource attributes matching the PBS API structure:

- ``pbs.admin.datastore`` — datastore listing and management
- ``pbs.admin.datastore("my-store")`` — a specific datastore
- ``pbs.access.users`` — user management
- ``pbs.config.acl`` — ACL configuration
- ``pbs.nodes`` — cluster node information

Quick start — async mock (no real PBS required)::

    import asyncio
    from proxmox_openapi.sdk.pbs import PBSSDK

    async def main():
        async with PBSSDK.mock() as pbs:
            stores = await pbs.admin.datastore.get()
            print(stores)

    asyncio.run(main())

Quick start — sync mock::

    from proxmox_openapi.sdk.pbs import PBSSDK

    with PBSSDK.sync_mock() as pbs:
        stores = pbs.admin.datastore.get()

Real PBS connection (token auth)::

    from proxmox_openapi.sdk.pbs import PBSSDK

    pbs = PBSSDK(
        host="pbs.example.com",
        user="admin@pbs",
        token_name="api-token",
        token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    )
    async with pbs as client:
        stores = await client.admin.datastore.get()

Real PBS connection (password auth)::

    from proxmox_openapi.sdk.pbs import PBSSDK

    async with PBSSDK(
        host="pbs.example.com",
        user="admin@pbs",
        password="secret",
        verify_ssl=False,
    ) as pbs:
        stores = await pbs.admin.datastore.get()
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_openapi.sdk.api import ProxmoxSDK

if TYPE_CHECKING:
    from proxmox_openapi.sdk.sync import SyncProxmoxSDK


class PBSSDK(ProxmoxSDK):
    """PBS-specific SDK — identical to :class:`~proxmox_openapi.sdk.ProxmoxSDK` with
    ``service="PBS"`` locked in.

    The PBS service uses:
    - Default port **8007**
    - Token separator **``:``** (e.g. ``user@pbs!token:secret``)
    - Auth cookie ``PBSAuthCookie``
    - Supported backends: ``https``, ``mock``

    All :class:`~proxmox_openapi.sdk.ProxmoxSDK` context-manager, navigation,
    and lifecycle methods are inherited unchanged.
    """

    def __init__(
        self,
        host: str | None = None,
        *,
        user: str | None = None,
        password: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        otp: str | None = None,
        otptype: str = "totp",
        backend: str = "https",
        port: int | None = None,
        path_prefix: str = "",
        verify_ssl: bool = True,
        cert: str | None = None,
        timeout: int = 5,
        proxies: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            host,
            user=user,
            password=password,
            token_name=token_name,
            token_value=token_value,
            otp=otp,
            otptype=otptype,
            service="PBS",
            backend=backend,
            port=port,
            path_prefix=path_prefix,
            verify_ssl=verify_ssl,
            cert=cert,
            timeout=timeout,
            proxies=proxies,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Class-method constructors — lock service="PBS"
    # ------------------------------------------------------------------

    @classmethod
    def mock(cls, schema_version: str = "latest") -> "PBSSDK":  # type: ignore[override]
        """Create a PBSSDK instance backed by the PBS in-memory mock.

        No real PBS host required.  Uses the pre-generated PBS OpenAPI schema
        to serve deterministic mock responses and support CRUD state.

        Example::

            async with PBSSDK.mock() as pbs:
                stores = await pbs.admin.datastore.get()
        """
        return super().mock(schema_version=schema_version, service="PBS")  # type: ignore[return-value]

    @classmethod
    def sync_mock(cls, schema_version: str = "latest") -> "SyncProxmoxSDK":  # type: ignore[override]
        """Create a synchronous PBS mock SDK instance.

        No real PBS host required.  All API calls block synchronously.

        Example::

            with PBSSDK.sync_mock() as pbs:
                stores = pbs.admin.datastore.get()
                print(stores)
        """
        import asyncio

        from proxmox_openapi.sdk.sync import SyncProxmoxResource, SyncProxmoxSDK

        instance = object.__new__(SyncProxmoxSDK)
        instance._loop = asyncio.new_event_loop()
        instance._sdk = cls.mock(schema_version=schema_version)
        instance._root = SyncProxmoxResource(instance._sdk._root, instance._loop)
        return instance

    @classmethod
    def sync(cls, **kwargs: Any) -> "SyncProxmoxSDK":  # type: ignore[override]
        """Create a synchronous PBS SDK for real connections.

        Example::

            with PBSSDK.sync(
                host="pbs.example.com",
                user="admin@pbs",
                password="secret",
            ) as pbs:
                stores = pbs.admin.datastore.get()
        """
        kwargs.setdefault("service", "PBS")
        return super().sync(**kwargs)


__all__ = ["PBSSDK"]
