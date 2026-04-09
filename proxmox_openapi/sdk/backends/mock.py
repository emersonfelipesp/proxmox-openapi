"""In-memory mock backend — no FastAPI server required."""

from __future__ import annotations

import logging
from copy import deepcopy
from typing import Any

from proxmox_openapi.mock.schema_helpers import (
    sample_value_for_schema,
    schema_fingerprint,
)
from proxmox_openapi.mock.state import shared_mock_store
from proxmox_openapi.schema import DEFAULT_PROXMOX_OPENAPI_TAG, load_proxmox_generated_openapi
from proxmox_openapi.sdk.backends.base import AbstractBackend

logger = logging.getLogger(__name__)


def _match_path(
    schema_paths: dict[str, Any],
    request_path: str,
) -> tuple[dict[str, Any] | None, dict[str, str]]:
    """Find the best-matching schema path template for ``request_path``.

    Returns ``(path_item_dict, extracted_path_params)`` or ``(None, {})``.
    Exact matches are preferred over templated matches.
    """
    request_parts = request_path.strip("/").split("/")

    exact = schema_paths.get(request_path)
    if exact:
        return exact, {}

    for template, path_item in schema_paths.items():
        t_parts = template.strip("/").split("/")
        if len(t_parts) != len(request_parts):
            continue
        params: dict[str, str] = {}
        matched = True
        for t, r in zip(t_parts, request_parts):
            if t.startswith("{") and t.endswith("}"):
                params[t[1:-1]] = r
            elif t != r:
                matched = False
                break
        if matched:
            return path_item, params

    return None, {}


def _response_schema(operation: dict[str, Any]) -> dict[str, Any] | None:
    """Extract the 200 response JSON schema from an operation dict."""
    try:
        return (
            operation.get("responses", {})
            .get("200", {})
            .get("content", {})
            .get("application/json", {})
            .get("schema")
        )
    except AttributeError:
        return None


class MockBackend(AbstractBackend):
    """In-memory mock backend that generates responses from the OpenAPI schema.

    Does not start a FastAPI server.  All data lives in the process-local
    ``SharedMemoryMockStore`` (same store used by the FastAPI mock server,
    so state can be shared across processes when needed).

    Supports:
    - GET: returns schema-derived mock data (deterministic, seed = path)
    - POST/PUT/PATCH: stores request data and returns the stored object
    - DELETE: removes from store, returns None

    Example::

        backend = MockBackend(schema_version="latest")
        nodes = await backend.request("GET", "/api2/json/nodes")
    """

    def __init__(
        self,
        schema_version: str = DEFAULT_PROXMOX_OPENAPI_TAG,
        api_path_prefix: str = "/api2/json",
        service: str = "PVE",
    ) -> None:
        self._schema_version = schema_version
        self._api_path_prefix = api_path_prefix
        self._service = service.upper()
        self._schema: dict[str, Any] | None = None
        self._paths: dict[str, Any] = {}
        self._fingerprint: str = ""
        self._store = None  # SharedMemoryMockStore, lazy

    def _ensure_schema(self) -> None:
        if self._schema is not None:
            return
        doc = load_proxmox_generated_openapi(
            version_tag=self._schema_version, service=self._service
        )
        if doc is None:
            logger.warning(
                "No Proxmox OpenAPI schema found for version '%s'. "
                "Mock backend will return empty responses.",
                self._schema_version,
            )
            self._schema = {}
            self._paths = {}
            return
        self._schema = doc
        self._paths = doc.get("paths") or {}
        self._fingerprint = schema_fingerprint(doc)
        self._store = shared_mock_store(self._fingerprint)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Return mock data for the given API path and method."""
        self._ensure_schema()

        method_upper = method.upper()

        # Strip API path prefix to match against schema paths
        schema_path = path
        if self._api_path_prefix and path.startswith(self._api_path_prefix):
            schema_path = path[len(self._api_path_prefix) :]
            if not schema_path.startswith("/"):
                schema_path = "/" + schema_path

        path_item, path_params = _match_path(self._paths, schema_path)

        if path_item is None:
            # Unknown path — return an empty object rather than raising
            logger.debug("MockBackend: no schema match for %s %s", method, path)
            return {} if method_upper == "GET" else None

        operation = path_item.get(method.lower())
        if operation is None:
            logger.debug("MockBackend: no operation for %s %s", method, path)
            return {} if method_upper == "GET" else None

        state_key = path

        if method_upper == "GET":
            return self._mock_get(path, operation, state_key, path_params)

        if method_upper == "DELETE":
            if self._store is not None:
                self._store.delete_object(state_key)
            return None

        # POST / PUT / PATCH — store and return
        return self._mock_mutate(path, operation, state_key, data or {})

    async def close(self) -> None:
        """Nothing to close for the mock backend."""

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _mock_get(
        self,
        path: str,
        operation: dict[str, Any],
        state_key: str,
        path_params: dict[str, str],
    ) -> Any:
        """Return stored value or generate a deterministic mock."""
        if self._store is not None:
            stored = self._store.get_object(state_key)
            if stored is not None and not self._store.is_deleted(state_key):
                return stored

        resp_schema = _response_schema(operation)
        value = sample_value_for_schema(resp_schema, seed=path)

        if self._store is not None:
            self._store.set_object(state_key, value)

        return deepcopy(value)

    def _mock_mutate(
        self,
        path: str,
        operation: dict[str, Any],
        state_key: str,
        request_data: dict[str, Any],
    ) -> Any:
        """Store request data and return a representative response."""
        resp_schema = _response_schema(operation)
        base = sample_value_for_schema(resp_schema, seed=path) if resp_schema else {}

        if isinstance(base, dict):
            merged = {**base, **{k: v for k, v in request_data.items() if v is not None}}
        else:
            merged = request_data or base

        if self._store is not None:
            self._store.set_object(state_key, merged)

        return deepcopy(merged) if merged else None


__all__ = ["MockBackend"]
