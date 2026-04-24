"""Abstract authentication strategy protocol for the Proxmox SDK."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

import aiohttp


@runtime_checkable
class AuthStrategy(Protocol):
    """Protocol that all SDK authentication handlers must implement.

    There are two concrete implementations:

    - :class:`~proxmox_sdk.sdk.auth.token.TokenAuth` — stateless API token auth.
    - :class:`~proxmox_sdk.sdk.auth.ticket.TicketAuth` — stateful ticket/password auth
      with automatic renewal and 2FA support.
    """

    def build_headers(self, method: str) -> dict[str, str]:
        """Return HTTP headers required for this auth strategy."""
        ...

    def build_cookies(self) -> dict[str, str]:
        """Return cookies required for this auth strategy."""
        ...

    async def ensure_ready(
        self,
        session: aiohttp.ClientSession,
        ticket_url: str,
        *,
        ssl: Any = None,
        proxy: str | None = None,
    ) -> None:
        """Ensure authentication state is valid before a request is sent.

        For stateless strategies (token auth) this is a no-op.
        For stateful strategies (ticket auth) this performs the initial
        authentication or renews an expiring ticket.

        Args:
            session: Active aiohttp session to use for auth requests.
            ticket_url: Full URL for the ``POST /access/ticket`` endpoint.
            ssl: SSL context or bool passed through to aiohttp.
            proxy: HTTP proxy URL forwarded to auth requests.
        """
        ...


__all__ = ["AuthStrategy"]
