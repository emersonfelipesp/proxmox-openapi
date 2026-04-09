"""Real Proxmox API route registration with validation."""

from __future__ import annotations

import inspect
from typing import Any

from fastapi import APIRouter, Body, FastAPI, Path, Query

from proxmox_openapi.exception import ProxmoxOpenAPIException
from proxmox_openapi.proxmox.client import ProxmoxClient
from proxmox_openapi.proxmox.config import ProxmoxConfig
from proxmox_openapi.proxmox_codegen.utils import slugify_identifier
from proxmox_openapi.routes.helpers import (
    SUPPORTED_METHODS as _SUPPORTED_METHODS,
)
from proxmox_openapi.routes.helpers import (
    load_model_module as _load_model_module_shared,
)
from proxmox_openapi.routes.helpers import (
    mounted_fastapi_path as _mounted_fastapi_path,
)
from proxmox_openapi.routes.helpers import (
    normalize_body_value as _normalize_body_value,
)
from proxmox_openapi.routes.helpers import (
    operation_id as _operation_id,
)
from proxmox_openapi.routes.helpers import (
    operation_parameters as _operation_parameters,
)
from proxmox_openapi.routes.helpers import (
    operation_request_model as _operation_request_model,
)
from proxmox_openapi.routes.helpers import (
    operation_response_model as _operation_response_model,
)
from proxmox_openapi.routes.helpers import (
    path_parameter_name_map as _path_parameter_name_map,
)
from proxmox_openapi.routes.helpers import (
    render_path as _render_path,
)
from proxmox_openapi.routes.helpers import (
    request_schema as _request_schema,
)
from proxmox_openapi.routes.helpers import (
    schema_to_annotation as _schema_to_annotation,
)
from proxmox_openapi.routes.helpers import (
    server_prefix as _server_prefix,
)
from proxmox_openapi.schema import (
    DEFAULT_PROXMOX_OPENAPI_TAG,
    load_proxmox_generated_openapi,
)

_GENERATED_ROUTE_NAME_PREFIX = "generated_proxmox_real__"


def _load_model_module(openapi_document: dict[str, object], version_tag: str) -> Any:
    """Load Pydantic models module from OpenAPI schema."""
    return _load_model_module_shared(openapi_document, version_tag, module_prefix="proxmox")


def _build_generated_endpoint(
    *,
    path_template: str,
    method: str,
    operation: dict[str, object],
    request_model: type | None,
    request_schema: dict[str, Any] | None,
    response_model: type | None,
    operation_id: str,
    proxmox_client: ProxmoxClient,
) -> object:
    """Build FastAPI endpoint that calls real Proxmox API."""
    path_param_name_map = _path_parameter_name_map(operation)
    path_param_map = {python: original for original, python in path_param_name_map.items()}
    query_param_map: dict[str, str] = {}
    signature_parameters: list[inspect.Parameter] = []
    used_names: set[str] = set()

    def _unique_name(base: str) -> str:
        candidate = base
        suffix = 1
        while candidate in used_names:
            candidate = f"{base}_{suffix}"
            suffix += 1
        return candidate

    # Add path and query parameters
    for parameter in _operation_parameters(operation):
        location = parameter.get("in")
        original_name = parameter.get("name")
        if not isinstance(original_name, str):
            continue

        schema = parameter.get("schema") if isinstance(parameter.get("schema"), dict) else {}
        description = parameter.get("description")
        required = bool(parameter.get("required"))
        python_name = (
            path_param_name_map[original_name]
            if location == "path" and original_name in path_param_name_map
            else slugify_identifier(original_name)
        )
        if python_name in used_names:
            python_name = _unique_name(f"op_{python_name}")
        annotation = _schema_to_annotation(schema)
        alias = original_name if python_name != original_name else None

        if location == "path":
            signature_parameters.append(
                inspect.Parameter(
                    python_name,
                    inspect.Parameter.KEYWORD_ONLY,
                    annotation=annotation,
                    default=Path(..., description=description),
                )
            )
            used_names.add(python_name)
        elif location == "query":
            query_param_map[python_name] = original_name
            if not required:
                annotation = annotation | None  # type: ignore[assignment]
            signature_parameters.append(
                inspect.Parameter(
                    python_name,
                    inspect.Parameter.KEYWORD_ONLY,
                    annotation=annotation,
                    default=Query(... if required else None, description=description, alias=alias),
                )
            )
            used_names.add(python_name)

    # Add request body parameter
    if request_schema is not None:
        annotation = request_model or _schema_to_annotation(request_schema)
        signature_parameters.append(
            inspect.Parameter(
                "request_body",
                inspect.Parameter.KEYWORD_ONLY,
                annotation=annotation,
                default=Body(...),
            )
        )

    async def generated_endpoint(**kwargs: Any) -> Any:
        request_body = kwargs.pop("request_body", None)
        path_values = {original: kwargs.pop(python) for python, original in path_param_map.items()}
        query_values = {
            original: kwargs.get(python)
            for python, original in query_param_map.items()
            if kwargs.get(python) is not None
        }
        body_value = _normalize_body_value(request_body)
        concrete_path = _render_path(path_template, path_values)

        try:
            # Call real Proxmox API
            result = await proxmox_client.request(
                method=method,
                path=concrete_path,
                params=query_values or None,
                json=body_value,
            )

            # Validate response if model exists
            if response_model is not None:
                try:
                    return response_model.model_validate(result)
                except Exception as error:
                    raise ProxmoxOpenAPIException(
                        message=f"Proxmox API response validation failed for {method} {path_template}",
                        detail="Response does not match generated model schema",
                        python_exception=str(error),
                    )

            return result

        except Exception as error:
            if hasattr(error, "status_code"):  # Already an HTTPException
                raise
            raise ProxmoxOpenAPIException(
                message=f"Proxmox API request failed for {method} {path_template}",
                detail=str(error),
            )

    generated_endpoint.__name__ = f"{_GENERATED_ROUTE_NAME_PREFIX}{method.lower()}__{operation_id}"
    generated_endpoint.__qualname__ = generated_endpoint.__name__
    generated_endpoint.__signature__ = inspect.Signature(  # type: ignore[attr-defined]
        parameters=signature_parameters,
        return_annotation=response_model or dict[str, object],
    )
    return generated_endpoint


def register_generated_proxmox_real_routes(
    app: FastAPI | APIRouter,
    *,
    version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG,
    openapi_document: dict[str, object] | None = None,
    proxmox_config: ProxmoxConfig,
) -> dict[str, object]:
    """Register real Proxmox API routes with validation.

    Args:
        app: FastAPI app or router
        version_tag: OpenAPI schema version tag
        openapi_document: Pre-loaded OpenAPI document (optional)
        proxmox_config: Proxmox connection configuration

    Returns:
        Registration statistics

    Raises:
        ProxmoxOpenAPIException: If schema not found or config invalid
    """
    document = openapi_document or load_proxmox_generated_openapi(version_tag=version_tag)
    if not document:
        raise ProxmoxOpenAPIException(
            message="Generated Proxmox OpenAPI schema not found",
            detail=f"Unable to load version tag '{version_tag}'",
        )

    proxmox_client = ProxmoxClient(proxmox_config)

    model_module = _load_model_module(document, version_tag)
    base_prefix = _server_prefix(document)
    path_items = {
        path: item
        for path, item in (document.get("paths") or {}).items()  # type: ignore[union-attr]
        if isinstance(item, dict)
    }

    route_count = 0
    method_count = 0

    for path_template, path_item in sorted(path_items.items()):
        for method, operation in sorted(path_item.items()):
            method_name = method.upper()
            if method_name not in _SUPPORTED_METHODS or not isinstance(operation, dict):
                continue

            operation_id = _operation_id(path_template, method_name, operation)
            request_schema_val = _request_schema(path_template, operation)
            request_model = _operation_request_model(
                model_module, path_template, operation, operation_id
            )
            response_model = _operation_response_model(model_module, operation_id)

            endpoint = _build_generated_endpoint(
                path_template=path_template,
                method=method_name,
                operation=operation,
                request_model=request_model,
                request_schema=request_schema_val,
                response_model=response_model,
                operation_id=operation_id,
                proxmox_client=proxmox_client,
            )

            route_name = f"{_GENERATED_ROUTE_NAME_PREFIX}{method_name.lower()}__{operation_id}"
            app.add_api_route(
                path=f"{base_prefix}{_mounted_fastapi_path(path_template, operation)}",
                endpoint=endpoint,
                methods=[method_name],
                name=route_name,
                summary=operation.get("summary"),  # type: ignore[arg-type]
                description=operation.get("description"),  # type: ignore[arg-type]
                response_model=response_model,
                tags=["proxmox real / generated"],
            )
            route_count += 1
            method_count += 1

    app.openapi_schema = None  # type: ignore[attr-defined]

    return {
        "route_count": route_count,
        "path_count": len(path_items),
        "method_count": method_count,
        "schema_version": document.get("info", {}).get("version", version_tag),  # type: ignore[union-attr]
        "base_prefix": base_prefix or "/",
    }


__all__ = ["register_generated_proxmox_real_routes"]
