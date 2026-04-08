"""Shared helpers for dynamic FastAPI route registration (mock and real modes)."""

from __future__ import annotations

import sys
from copy import deepcopy
from types import ModuleType
from typing import Any, Callable

from proxmox_openapi.proxmox_codegen.pydantic_generator import (
    generate_pydantic_models_from_openapi,
)
from proxmox_openapi.proxmox_codegen.utils import (
    extract_path_params,
    pascal_case,
    slugify_identifier,
)

# HTTP methods supported by the generated route registration.
SUPPORTED_METHODS: frozenset[str] = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE"})


def schema_to_annotation(
    schema: dict[str, object] | None,
    *,
    resolver: Callable[[dict[str, object]], dict[str, object]] | None = None,
) -> object:
    """Convert a JSON schema dict to a Python type annotation.

    Args:
        schema: JSON schema dict, or ``None``.
        resolver: Optional callable to resolve ``$ref`` or normalise the schema
            before type mapping (used by mock mode to call ``resolved_schema``).
    """
    if not isinstance(schema, dict):
        return object
    if resolver is not None:
        schema = resolver(schema)
    schema_type = schema.get("type")
    if schema_type == "string":
        return str
    if schema_type == "integer":
        return int
    if schema_type == "number":
        return float
    if schema_type == "boolean":
        return bool
    if schema_type == "array":
        return list[schema_to_annotation(schema.get("items"), resolver=resolver)]  # type: ignore[misc]
    if schema_type == "object" or isinstance(schema.get("properties"), dict):
        return dict[str, object]
    return object


def load_model_module(
    openapi_document: dict[str, object],
    version_tag: str,
    *,
    module_prefix: str,
) -> ModuleType:
    """Generate Pydantic models from *openapi_document* and register as a dynamic module.

    Args:
        openapi_document: Parsed OpenAPI document dict.
        version_tag: Version string used in the module name (dots replaced with underscores).
        module_prefix: Namespace prefix, e.g. ``"mock"`` or ``"proxmox"``.
    """
    code = generate_pydantic_models_from_openapi(openapi_document)
    sanitised = version_tag.replace(".", "_")
    module = ModuleType(f"proxmox_openapi.{module_prefix}.generated_{sanitised}")
    sys.modules[module.__name__] = module
    exec(code, module.__dict__)  # noqa: S102
    for value in module.__dict__.values():
        if (
            isinstance(value, type)
            and getattr(value, "__module__", None) == module.__name__
            and hasattr(value, "model_rebuild")
        ):
            value.model_rebuild(_types_namespace=module.__dict__)
    return module


def request_schema(
    path_template: str,
    operation: dict[str, object],
) -> dict[str, object] | None:
    """Extract the request body JSON schema, removing path parameter properties."""
    schema = (
        operation.get("requestBody", {})  # type: ignore[union-attr]
        .get("content", {})  # type: ignore[union-attr]
        .get("application/json", {})  # type: ignore[union-attr]
        .get("schema")  # type: ignore[union-attr]
    )
    if not isinstance(schema, dict):
        return None

    path_param_names = set(extract_path_params(path_template))
    if not path_param_names:
        return deepcopy(schema)

    filtered = deepcopy(schema)
    properties = filtered.get("properties")
    if isinstance(properties, dict):
        filtered["properties"] = {
            name: value for name, value in properties.items() if name not in path_param_names
        }
    required = filtered.get("required")
    if isinstance(required, list):
        filtered["required"] = [name for name in required if name not in path_param_names]
    return filtered


def response_schema(operation: dict[str, object]) -> dict[str, object] | None:
    """Extract the 200 response JSON schema from an operation dict."""
    schema = (
        operation.get("responses", {})  # type: ignore[union-attr]
        .get("200", {})  # type: ignore[union-attr]
        .get("content", {})  # type: ignore[union-attr]
        .get("application/json", {})  # type: ignore[union-attr]
        .get("schema")  # type: ignore[union-attr]
    )
    return deepcopy(schema) if isinstance(schema, dict) else None


def operation_parameters(operation: dict[str, object]) -> list[dict[str, object]]:
    """Return the parameters list from an operation, filtering non-dict entries."""
    parameters = operation.get("parameters")
    if not isinstance(parameters, list):
        return []
    return [p for p in parameters if isinstance(p, dict)]


def path_parameter_name_map(operation: dict[str, object]) -> dict[str, str]:
    """Map original path parameter names to Python-safe identifiers."""
    used_names: set[str] = {"request_body"}
    mapping: dict[str, str] = {}

    for parameter in operation_parameters(operation):
        if parameter.get("in") != "path":
            continue
        original_name = parameter.get("name")
        if not isinstance(original_name, str):
            continue

        python_name = slugify_identifier(original_name)
        if python_name in used_names:
            candidate = f"op_{python_name}"
            suffix = 1
            while candidate in used_names:
                candidate = f"op_{python_name}_{suffix}"
                suffix += 1
            python_name = candidate

        used_names.add(python_name)
        mapping[original_name] = python_name

    return mapping


def mounted_fastapi_path(path_template: str, operation: dict[str, object]) -> str:
    """Convert an API path template to FastAPI path format (Python-safe parameter names)."""
    mounted = path_template
    for original, python in path_parameter_name_map(operation).items():
        mounted = mounted.replace(f"{{{original}}}", f"{{{python}}}")
    return mounted


def render_path(path_template: str, path_values: dict[str, Any]) -> str:
    """Substitute path parameter values into a path template."""
    rendered = path_template
    for name, value in path_values.items():
        rendered = rendered.replace(f"{{{name}}}", str(value))
    return rendered


def normalize_body_value(request_body: Any) -> Any:
    """Normalise a request body to a plain dict (handles Pydantic models)."""
    if hasattr(request_body, "model_dump"):
        return request_body.model_dump(by_alias=True, exclude_none=True)
    return request_body


def server_prefix(openapi_document: dict[str, object]) -> str:
    """Extract the server URL prefix from an OpenAPI document."""
    servers = openapi_document.get("servers")
    if isinstance(servers, list) and servers:
        first = servers[0]
        if isinstance(first, dict) and isinstance(first.get("url"), str):
            return first["url"].rstrip("/")  # type: ignore[return-value]
    return ""


def operation_id(path_template: str, method: str, operation: dict[str, object]) -> str:
    """Return the operation ID, generating one from path+method if absent."""
    return operation.get("operationId") or f"{method.lower()}_{path_template}"  # type: ignore[return-value]


def operation_request_model(
    model_module: ModuleType,
    path_template: str,
    operation: dict[str, object],
    op_id: str,
) -> type | None:
    """Return the Pydantic request model for an operation, or ``None``."""
    req_schema = request_schema(path_template, operation)
    if not isinstance(req_schema, dict):
        return None
    properties = req_schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        return None
    return getattr(model_module, f"{pascal_case(op_id)}Request", None)


def operation_response_model(model_module: ModuleType, op_id: str) -> type | None:
    """Return the Pydantic response model for an operation, or ``None``."""
    return getattr(model_module, f"{pascal_case(op_id)}Response", None)


__all__ = [
    "SUPPORTED_METHODS",
    "load_model_module",
    "mounted_fastapi_path",
    "normalize_body_value",
    "operation_id",
    "operation_parameters",
    "operation_request_model",
    "operation_response_model",
    "path_parameter_name_map",
    "render_path",
    "request_schema",
    "response_schema",
    "schema_to_annotation",
    "server_prefix",
]
