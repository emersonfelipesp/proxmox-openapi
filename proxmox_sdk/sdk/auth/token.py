"""API token authentication (stateless)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from proxmox_sdk.sdk.services import ServiceConfig


class TokenAuth:
    """Stateless API token authentication handler.

    Builds the ``Authorization`` header required by Proxmox token auth.
    No session management or renewal needed — tokens do not expire.

    Token header format:
        PVE/PMG:  ``{prefix}APIToken={user}!{token_name}={token_value}``
        PBS:      ``PBSAPIToken={user}!{token_name}:{token_value}``

    The separator (``=`` vs ``:``) comes from the service configuration.

    Usage::

        auth = TokenAuth(
            user="monitoring@pve",
            token_name="api-read",
            token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            service_config=SERVICES["PVE"],
        )
        headers = auth.build_headers("GET")
    """

    def __init__(
        self,
        *,
        user: str,
        token_name: str,
        token_value: str,
        service_config: ServiceConfig,
    ) -> None:
        self._user = user
        self._token_name = token_name
        self._token_value = token_value
        self._service_config = service_config

        # Pre-build the header value — it never changes.
        service_prefix = service_config.auth_cookie_name.replace("AuthCookie", "")
        sep = service_config.token_separator
        self._header_value = f"{service_prefix}APIToken={user}!{token_name}{sep}{token_value}"

    def build_headers(self, method: str) -> dict[str, str]:  # noqa: ARG002
        """Return the Authorization header (method is ignored for tokens)."""
        return {"Authorization": self._header_value}

    def build_cookies(self) -> dict[str, str]:
        """Token auth uses headers, not cookies."""
        return {}

    async def ensure_ready(
        self,
        session: object,
        ticket_url: str,
        *,
        ssl: object = None,
        proxy: str | None = None,
    ) -> None:
        """Token auth is stateless — no authentication step required."""


def parse_token_id(token_id: str) -> tuple[str, str]:
    """Split a Proxmox token_id string into (user, token_name).

    Proxmox token IDs use the format ``user@realm!token_name``.
    Returns ``(token_id, "")`` when the ``!`` separator is absent.
    """
    parts = token_id.rsplit("!", 1)
    if len(parts) == 2:
        return parts[0], parts[1]
    return token_id, ""


__all__ = ["TokenAuth", "parse_token_id"]
