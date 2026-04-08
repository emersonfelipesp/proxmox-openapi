"""Dynamic Proxmox API resource navigation."""

from __future__ import annotations

import posixpath
from typing import TYPE_CHECKING, Any
from urllib.parse import urlsplit, urlunsplit

if TYPE_CHECKING:
    from proxmox_openapi.sdk.backends.base import AbstractBackend


def _url_join(base: str, *args: str) -> str:
    """Join API path segments using posixpath (handles trailing slashes cleanly)."""
    # Fast path: most Proxmox SDK paths are relative strings with no scheme/netloc.
    # Avoid the full urlsplit/urlunsplit round-trip in that common case.
    if "://" not in base:
        return posixpath.join(base or "/", *[str(a) for a in args])
    scheme, netloc, path, query, fragment = urlsplit(base)
    path = posixpath.join(path or "/", *[str(a) for a in args])
    return urlunsplit((scheme, netloc, path, query, fragment))


def _filter_none(d: dict[str, Any]) -> dict[str, Any]:
    """Remove None values — prevents pvesh/API errors."""
    # Fast path: skip allocation when no Nones are present (common case).
    if all(v is not None for v in d.values()):
        return d
    return {k: v for k, v in d.items() if v is not None}


class ProxmoxResource:
    """Dynamic Proxmox API resource that builds URLs via attribute access.

    Each attribute access creates a new ``ProxmoxResource`` with the
    extended path.  Calling the resource adds a resource ID to the path.
    HTTP methods execute the request against the backend.

    Navigation styles::

        proxmox.nodes.get()
        proxmox.nodes("pve1").qemu.get()
        proxmox.nodes("pve1").qemu(100).status.current.get()
        proxmox.nodes("pve1/qemu/100").status.current.get()
        proxmox.nodes(["pve1", "qemu", "100"]).status.current.get()

    HTTP methods::

        await proxmox.nodes.get()
        await proxmox.nodes("pve1").qemu.post(vmid=100, name="test")
        await proxmox.nodes("pve1").qemu(100).config.put(memory=4096)
        await proxmox.nodes("pve1").qemu(100).delete()

    Aliases::

        await proxmox.nodes("pve1").qemu.create(...)   # post
        await proxmox.nodes("pve1").qemu(100).set(...)  # put
    """

    __slots__ = ("_path", "_backend")

    def __init__(self, path: str, backend: AbstractBackend) -> None:
        object.__setattr__(self, "_path", path)
        object.__setattr__(self, "_backend", backend)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def __getattr__(self, item: str) -> ProxmoxResource:
        if item.startswith("_"):
            raise AttributeError(item)
        return ProxmoxResource(
            path=_url_join(self._path, item),
            backend=self._backend,
        )

    def __call__(
        self,
        resource_id: str | int | list | tuple | None = None,
    ) -> ProxmoxResource:
        """Add a resource ID (or list of IDs) to the current path."""
        if resource_id is None:
            return self
        if isinstance(resource_id, (list, tuple)):
            # Flatten: nodes(["pve1", "qemu", "100"]) → /nodes/pve1/qemu/100
            return ProxmoxResource(
                path=_url_join(self._path, *[str(r) for r in resource_id]),
                backend=self._backend,
            )
        # Support slash-separated IDs: nodes("pve1/qemu/100")
        return ProxmoxResource(
            path=_url_join(self._path, *str(resource_id).split("/")),
            backend=self._backend,
        )

    def __repr__(self) -> str:
        return f"ProxmoxResource(path={self._path!r})"

    # ------------------------------------------------------------------
    # HTTP methods
    # ------------------------------------------------------------------

    async def get(self, *path_args: str, **params: Any) -> Any:
        """HTTP GET — retrieve a resource or list.

        Extra positional args extend the path before the call::

            await proxmox.nodes.get("pve1")  # same as proxmox.nodes("pve1").get()
        """
        resource = self._extend(*path_args)
        return await resource._backend.request(
            "GET",
            resource._path,
            params=_filter_none(params) or None,
        )

    async def post(self, *path_args: str, **data: Any) -> Any:
        """HTTP POST — create a resource."""
        resource = self._extend(*path_args)
        return await resource._backend.request(
            "POST",
            resource._path,
            data=_filter_none(data) or None,
        )

    async def put(self, *path_args: str, **data: Any) -> Any:
        """HTTP PUT — replace/update a resource."""
        resource = self._extend(*path_args)
        return await resource._backend.request(
            "PUT",
            resource._path,
            data=_filter_none(data) or None,
        )

    async def patch(self, *path_args: str, **data: Any) -> Any:
        """HTTP PATCH — partial update."""
        resource = self._extend(*path_args)
        return await resource._backend.request(
            "PATCH",
            resource._path,
            data=_filter_none(data) or None,
        )

    async def delete(self, *path_args: str, **params: Any) -> Any:
        """HTTP DELETE — remove a resource."""
        resource = self._extend(*path_args)
        return await resource._backend.request(
            "DELETE",
            resource._path,
            params=_filter_none(params) or None,
        )

    # Proxmoxer-compatible aliases
    async def create(self, *path_args: str, **data: Any) -> Any:
        """Alias for :meth:`post` (proxmoxer compatibility)."""
        return await self.post(*path_args, **data)

    async def set(self, *path_args: str, **data: Any) -> Any:
        """Alias for :meth:`put` (proxmoxer compatibility)."""
        return await self.put(*path_args, **data)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _extend(self, *args: str) -> ProxmoxResource:
        """Return a new resource with extra path segments appended."""
        if not args:
            return self
        return ProxmoxResource(
            path=_url_join(self._path, *[str(a) for a in args]),
            backend=self._backend,
        )


__all__ = ["ProxmoxResource"]
