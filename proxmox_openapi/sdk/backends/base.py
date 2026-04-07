"""Abstract backend base class for the Proxmox SDK."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AbstractBackend(ABC):
    """Abstract base class that all SDK backends must subclass.

    Backends are responsible for executing API calls — they know how to reach
    the Proxmox service (HTTPS, SSH, local pvesh, or in-memory mock) and
    how to authenticate.  The ``ProxmoxResource`` navigation layer calls
    ``request()`` and never interacts with the transport directly.
    """

    @abstractmethod
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Execute a Proxmox API call.

        Args:
            method: HTTP verb — GET, POST, PUT, PATCH, DELETE.
            path: Full API path including prefix, e.g. ``/api2/json/nodes``.
            params: Query parameters (used by GET/DELETE).
            data: Request body (used by POST/PUT/PATCH).

        Returns:
            Unwrapped response data (Proxmox ``data`` field extracted).

        Raises:
            ResourceException: API returned HTTP >= 400.
            AuthenticationError: Authentication failed.
        """

    @abstractmethod
    async def close(self) -> None:
        """Release held resources (sessions, connections, threads)."""

    async def get_tokens(self) -> tuple[str, str]:
        """Return (ticket, csrf_token) for HTTPS ticket-auth backends.

        The default implementation raises :class:`RuntimeError`.
        Override in backends that support ticket authentication.

        Raises:
            RuntimeError: Always, unless overridden.
        """
        raise RuntimeError(
            "get_tokens() is only available for the HTTPS backend with password auth"
        )


__all__ = ["AbstractBackend"]
