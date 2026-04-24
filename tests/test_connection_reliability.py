"""Tests for connection reliability: proxy fix, explicit error types, retry."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest

from proxmox_sdk.sdk.auth.ticket import TicketAuth
from proxmox_sdk.sdk.exceptions import (
    AuthenticationError,
    ProxmoxConnectionError,
    ProxmoxTimeoutError,
    ResourceException,
)
from proxmox_sdk.sdk.services import SERVICES

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_json_response(status: int, body: dict) -> AsyncMock:
    """Build a mock aiohttp response that returns *body* from .json()."""
    resp = AsyncMock()
    resp.status = status
    resp.reason = "OK" if status < 400 else "Error"
    resp.json = AsyncMock(return_value=body)

    # Support async context manager (async with session.request(...) as resp)
    cm = AsyncMock()
    cm.__aenter__ = AsyncMock(return_value=resp)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


def _make_ticket_auth() -> TicketAuth:
    return TicketAuth(
        username="admin@pam",
        password="secret",
        service_config=SERVICES["PVE"],
    )


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


def test_proxmox_timeout_error_is_resource_exception() -> None:
    err = ProxmoxTimeoutError("timed out")
    assert isinstance(err, ResourceException)
    assert err.status_code == 504


def test_proxmox_connection_error_is_resource_exception() -> None:
    err = ProxmoxConnectionError("refused")
    assert isinstance(err, ResourceException)
    assert err.status_code == 503


# ---------------------------------------------------------------------------
# TicketAuth proxy threading (Issue #3 core fix)
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_ticket_auth_passes_proxy_to_session_post() -> None:
    """Auth request must use the proxy so it works in proxy-only networks."""
    auth = _make_ticket_auth()
    ticket_url = "https://pve.example.com:8006/access/ticket"
    proxy_url = "http://proxy.internal:3128"

    ok_body = {"data": {"ticket": "PVE:admin@pam:abc", "CSRFPreventionToken": "csrf123"}}
    session = AsyncMock()
    session.post = MagicMock(return_value=_make_json_response(200, ok_body))

    await auth._request_ticket(session, ticket_url, "secret", ssl=False, proxy=proxy_url)

    call_kwargs = session.post.call_args.kwargs
    assert call_kwargs.get("proxy") == proxy_url, (
        "proxy= must be forwarded to session.post() for auth to work through proxy"
    )


@pytest.mark.anyio
async def test_ticket_auth_proxy_none_by_default() -> None:
    """Without a proxy configured the argument is omitted / None."""
    auth = _make_ticket_auth()
    ticket_url = "https://pve.example.com:8006/access/ticket"
    ok_body = {"data": {"ticket": "PVE:admin@pam:abc", "CSRFPreventionToken": "csrf123"}}
    session = AsyncMock()
    session.post = MagicMock(return_value=_make_json_response(200, ok_body))

    await auth._request_ticket(session, ticket_url, "secret", ssl=False)

    call_kwargs = session.post.call_args.kwargs
    assert call_kwargs.get("proxy") is None


@pytest.mark.anyio
async def test_ticket_auth_timeout_raises_authentication_error() -> None:
    auth = _make_ticket_auth()
    ticket_url = "https://pve.example.com:8006/access/ticket"
    session = AsyncMock()

    # Make the context manager raise on __aenter__
    cm = AsyncMock()
    cm.__aenter__ = AsyncMock(side_effect=asyncio.TimeoutError())
    cm.__aexit__ = AsyncMock(return_value=False)
    session.post = MagicMock(return_value=cm)

    with pytest.raises(AuthenticationError, match="timed out"):
        await auth._request_ticket(session, ticket_url, "secret", ssl=False)


# ---------------------------------------------------------------------------
# HttpsBackend error mapping
# ---------------------------------------------------------------------------


def _make_https_backend(max_retries: int = 0, retry_backoff: float = 0.0):
    from proxmox_sdk.sdk.auth.token import TokenAuth
    from proxmox_sdk.sdk.backends.https import HttpsBackend

    auth = TokenAuth(
        user="admin@pam",
        token_name="mytoken",
        token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        service_config=SERVICES["PVE"],
    )
    return HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=auth,
        verify_ssl=False,
        max_retries=max_retries,
        retry_backoff=retry_backoff,
    )


@pytest.mark.anyio
async def test_request_raises_proxmox_timeout_error_on_timeout() -> None:
    backend = _make_https_backend()

    cm = AsyncMock()
    cm.__aenter__ = AsyncMock(side_effect=asyncio.TimeoutError())
    cm.__aexit__ = AsyncMock(return_value=False)

    with (
        patch.object(backend, "_ensure_session") as mock_sess,
        patch.object(backend, "_ensure_authenticated"),
    ):
        session = AsyncMock()
        session.request = MagicMock(return_value=cm)
        mock_sess.return_value = session

        with pytest.raises(ProxmoxTimeoutError):
            await backend.request("GET", "/nodes")


@pytest.mark.anyio
async def test_request_raises_proxmox_connection_error_on_connector_error() -> None:
    backend = _make_https_backend()

    with (
        patch.object(backend, "_ensure_session") as mock_sess,
        patch.object(backend, "_ensure_authenticated"),
    ):
        session = AsyncMock()

        cm = AsyncMock()
        cm.__aenter__ = AsyncMock(
            side_effect=aiohttp.ClientConnectorError(
                connection_key=MagicMock(), os_error=OSError("connection refused")
            )
        )
        cm.__aexit__ = AsyncMock(return_value=False)
        session.request = MagicMock(return_value=cm)
        mock_sess.return_value = session

        with pytest.raises(ProxmoxConnectionError, match="Cannot connect"):
            await backend.request("GET", "/nodes")


@pytest.mark.anyio
async def test_request_raises_proxmox_connection_error_on_generic_client_error() -> None:
    backend = _make_https_backend()

    with (
        patch.object(backend, "_ensure_session") as mock_sess,
        patch.object(backend, "_ensure_authenticated"),
    ):
        session = AsyncMock()

        cm = AsyncMock()
        cm.__aenter__ = AsyncMock(side_effect=aiohttp.ClientError("generic error"))
        cm.__aexit__ = AsyncMock(return_value=False)
        session.request = MagicMock(return_value=cm)
        mock_sess.return_value = session

        with pytest.raises(ProxmoxConnectionError):
            await backend.request("GET", "/nodes")


# ---------------------------------------------------------------------------
# Retry behaviour
# ---------------------------------------------------------------------------


@pytest.mark.anyio
async def test_get_retries_on_503_up_to_max_retries() -> None:
    """GET should retry on 503 up to max_retries times."""
    backend = _make_https_backend(max_retries=2, retry_backoff=0.0)

    call_count = 0

    def _make_503_cm():
        nonlocal call_count
        call_count += 1
        resp = AsyncMock()
        resp.status = 503
        resp.reason = "Service Unavailable"
        resp.json = AsyncMock(return_value={"data": "unavailable"})
        cm = AsyncMock()
        cm.__aenter__ = AsyncMock(return_value=resp)
        cm.__aexit__ = AsyncMock(return_value=False)
        return cm

    with (
        patch.object(backend, "_ensure_session") as mock_sess,
        patch.object(backend, "_ensure_authenticated"),
    ):
        session = AsyncMock()
        session.request = MagicMock(side_effect=lambda **_: _make_503_cm())
        mock_sess.return_value = session

        with pytest.raises(ResourceException) as exc_info:
            await backend.request("GET", "/nodes")

        assert exc_info.value.status_code == 503
        assert call_count == 3  # 1 initial + 2 retries


@pytest.mark.anyio
async def test_post_does_not_retry_on_503() -> None:
    """POST must not be retried to avoid accidental double-mutation."""
    backend = _make_https_backend(max_retries=3, retry_backoff=0.0)

    call_count = 0

    def _make_503_cm():
        nonlocal call_count
        call_count += 1
        resp = AsyncMock()
        resp.status = 503
        resp.reason = "Service Unavailable"
        resp.json = AsyncMock(return_value={"data": "unavailable"})
        cm = AsyncMock()
        cm.__aenter__ = AsyncMock(return_value=resp)
        cm.__aexit__ = AsyncMock(return_value=False)
        return cm

    with (
        patch.object(backend, "_ensure_session") as mock_sess,
        patch.object(backend, "_ensure_authenticated"),
    ):
        session = AsyncMock()
        session.request = MagicMock(side_effect=lambda **_: _make_503_cm())
        mock_sess.return_value = session

        with pytest.raises(ResourceException) as exc_info:
            await backend.request("POST", "/nodes/pve1/qemu")

        assert exc_info.value.status_code == 503
        assert call_count == 1  # no retry on POST


@pytest.mark.anyio
async def test_get_succeeds_after_transient_503() -> None:
    """GET should succeed on the second attempt if the first returns 503."""
    backend = _make_https_backend(max_retries=1, retry_backoff=0.0)

    attempts = [0]

    def _make_cm():
        if attempts[0] == 0:
            attempts[0] += 1
            resp = AsyncMock()
            resp.status = 503
            resp.reason = "Service Unavailable"
            resp.json = AsyncMock(return_value={"data": "unavailable"})
        else:
            resp = AsyncMock()
            resp.status = 200
            resp.reason = "OK"
            resp.json = AsyncMock(return_value={"data": [{"node": "pve1"}]})
        cm = AsyncMock()
        cm.__aenter__ = AsyncMock(return_value=resp)
        cm.__aexit__ = AsyncMock(return_value=False)
        return cm

    with (
        patch.object(backend, "_ensure_session") as mock_sess,
        patch.object(backend, "_ensure_authenticated"),
    ):
        session = AsyncMock()
        session.request = MagicMock(side_effect=lambda **_: _make_cm())
        mock_sess.return_value = session

        result = await backend.request("GET", "/nodes")
        assert result == [{"node": "pve1"}]


# ---------------------------------------------------------------------------
# Constructor parameters
# ---------------------------------------------------------------------------


def test_https_backend_connect_timeout_in_client_timeout() -> None:
    """connect_timeout must be passed to aiohttp.ClientTimeout.connect."""
    from proxmox_sdk.sdk.auth.token import TokenAuth
    from proxmox_sdk.sdk.backends.https import HttpsBackend

    auth = TokenAuth(
        user="admin@pam",
        token_name="tok",
        token_value="val",
        service_config=SERVICES["PVE"],
    )
    backend = HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=auth,
        verify_ssl=False,
        timeout=30,
        connect_timeout=5,
    )
    assert backend._timeout.connect == 5
    assert backend._timeout.total == 30
