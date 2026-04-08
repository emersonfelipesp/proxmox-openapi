"""Schema helpers for generated mock routes."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from proxmox_openapi.schema import GeneratedOpenAPIDocument, ProxmoxSchemaValue


def schema_fingerprint(openapi_document: dict[str, object]) -> str:
    """Return a stable fingerprint for the loaded OpenAPI document.

    Args:
        openapi_document: OpenAPI v3 specification as dict

    Returns:
        SHA256 hex digest of the entire OpenAPI document
    """
    return GeneratedOpenAPIDocument.model_validate(openapi_document).fingerprint


def resolved_schema(schema: dict[str, Any] | None) -> dict[str, Any]:
    """Resolve the most useful inline schema representation for mock generation.

    Handles oneOf, allOf, and nested schemas by extracting the first/primary
    schema variant suitable for generating mock data.

    Args:
        schema: JSON schema dict (possibly with oneOf/allOf)

    Returns:
        Single resolved schema dict suitable for mock data generation
    """
    return ProxmoxSchemaValue.model_validate(schema).resolved()


def schema_kind(schema: dict[str, Any] | None) -> str:
    """Classify the resolved schema into a small set of storage kinds.

    Maps JSON schema type to storage classification for mock state management
    (e.g., 'list', 'object', 'scalar').

    Args:
        schema: JSON schema dict

    Returns:
        Classification string: 'list', 'object', 'scalar', or 'unknown'
    """
    return ProxmoxSchemaValue.model_validate(schema).kind()


def sample_value_for_schema(  # noqa: C901
    schema: dict[str, Any] | None,
    *,
    seed: str,
    field_name: str | None = None,
) -> Any:
    """Build a deterministic mock value for an inline schema."""
    return ProxmoxSchemaValue.model_validate(schema).sample_value(seed=seed, field_name=field_name)


def deep_merge(base: Any, override: Any) -> Any:
    """Merge dict-shaped payloads recursively and otherwise replace the value."""

    if isinstance(base, dict) and isinstance(override, dict):
        merged = deepcopy(base)
        for key, value in override.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = deepcopy(value)
        return merged
    return deepcopy(override)


def merge_with_schema_defaults(
    schema: dict[str, Any] | None,
    *,
    seed: str,
    override: Any | None = None,
) -> Any:
    """Merge user-provided values into a deterministic schema-backed seed value."""
    return ProxmoxSchemaValue.model_validate(schema).merge_defaults(seed=seed, override=override)
