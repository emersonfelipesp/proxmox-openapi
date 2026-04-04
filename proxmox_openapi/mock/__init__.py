"""Mock API module for Proxmox OpenAPI."""

from proxmox_openapi.mock.app import create_mock_app
from proxmox_openapi.mock.routes import (
    generated_proxmox_mock_route_state,
    register_generated_proxmox_mock_routes,
)
from proxmox_openapi.mock.schema_helpers import (
    deep_merge,
    merge_with_schema_defaults,
    resolved_schema,
    sample_value_for_schema,
    schema_fingerprint,
    schema_kind,
)
from proxmox_openapi.mock.state import (
    SharedMemoryMockStore,
    mock_state_owner_pid,
    reset_shared_mock_state,
    shared_mock_store,
)

__all__ = [
    "create_mock_app",
    "generated_proxmox_mock_route_state",
    "register_generated_proxmox_mock_routes",
    "deep_merge",
    "merge_with_schema_defaults",
    "sample_value_for_schema",
    "schema_fingerprint",
    "schema_kind",
    "resolved_schema",
    "SharedMemoryMockStore",
    "mock_state_owner_pid",
    "reset_shared_mock_state",
    "shared_mock_store",
]
