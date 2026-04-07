"""Runtime-generated FastAPI routes for the standalone Proxmox mock API."""

from __future__ import annotations

import inspect
from copy import deepcopy
from dataclasses import dataclass
from types import ModuleType
from typing import Any

from fastapi import APIRouter, Body, FastAPI, HTTPException, Path, Query

from proxmox_openapi.exception import ProxmoxOpenAPIException
from proxmox_openapi.mock.schema_helpers import (
    merge_with_schema_defaults,
    resolved_schema,
    sample_value_for_schema,
    schema_fingerprint,
    schema_kind,
)
from proxmox_openapi.mock.state import shared_mock_store
from proxmox_openapi.proxmox_codegen.utils import extract_path_params, slugify_identifier
from proxmox_openapi.routes.helpers import (
    SUPPORTED_METHODS as _SUPPORTED_GENERATED_METHODS,
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
    request_schema as _request_schema_without_path_params,
)
from proxmox_openapi.routes.helpers import (
    response_schema as _response_schema,
)
from proxmox_openapi.routes.helpers import (
    schema_to_annotation as _schema_to_annotation_base,
)
from proxmox_openapi.routes.helpers import (
    server_prefix as _server_prefix,
)
from proxmox_openapi.schema import (
    DEFAULT_PROXMOX_OPENAPI_TAG,
    load_proxmox_generated_openapi,
)

_GENERATED_ROUTE_NAME_PREFIX = "generated_proxmox_mock__"
_GENERATED_ROUTE_STATE: dict[str, object] = {
    "route_names": set(),
    "route_count": 0,
    "path_count": 0,
    "method_count": 0,
    "schema_version": DEFAULT_PROXMOX_OPENAPI_TAG,
}


@dataclass(frozen=True, slots=True)
class RouteTopology:
    """Schema-derived state helpers for a single route."""

    path_template: str
    absolute_path_template: str
    method: str
    operation: dict[str, Any]
    request_schema: dict[str, Any] | None
    response_schema: dict[str, Any] | None
    same_path_get_schema: dict[str, Any] | None
    same_path_get_kind: str
    direct_child_template: str | None
    absolute_direct_child_template: str | None
    direct_child_param: str | None
    direct_child_param_schema: dict[str, Any] | None
    parent_collection_template: str | None
    absolute_parent_collection_template: str | None
    parent_collection_item_schema: dict[str, Any] | None


def _schema_to_annotation(schema: dict[str, object] | None) -> object:
    """Mock-mode wrapper: resolves $ref before delegating to the shared helper."""
    return _schema_to_annotation_base(schema, resolver=resolved_schema)


def _load_model_module(openapi_document: dict[str, object], version_tag: str) -> ModuleType:
    return _load_model_module_shared(openapi_document, version_tag, module_prefix="mock")


def _build_direct_child_index(
    path_items: dict[str, dict[str, object]],
) -> dict[str, tuple[str, str, dict[str, Any] | None]]:
    """Pre-compute a mapping of parent path → first direct child template info.

    Replaces the O(P²) per-path scan in the old ``_direct_child_template``
    function with a single O(P) pass that is reused across all paths.
    """
    # Collect all children keyed by parent path.
    children: dict[str, list[tuple[str, str, dict[str, Any] | None]]] = {}
    for candidate_template, candidate_item in path_items.items():
        segments = candidate_template.rsplit("/", 1)
        if len(segments) != 2:
            continue
        parent_template, suffix = segments
        if not suffix.startswith("{") or not suffix.endswith("}"):
            continue
        get_operation = candidate_item.get("get")
        if not isinstance(get_operation, dict):
            continue
        parameter_name = suffix[1:-1]
        parameter_schema = None
        for parameter in _operation_parameters(get_operation):
            if parameter.get("in") == "path" and parameter.get("name") == parameter_name:
                if isinstance(parameter.get("schema"), dict):
                    parameter_schema = deepcopy(parameter["schema"])
                break
        children.setdefault(parent_template, []).append(
            (candidate_template, parameter_name, parameter_schema)
        )
    # Keep only the lexicographically first child per parent (matches old sort).
    return {
        parent: sorted(candidates, key=lambda item: item[0])[0]
        for parent, candidates in children.items()
    }


def _direct_child_template(
    path_template: str,
    path_items: dict[str, dict[str, object]],
) -> tuple[str | None, str | None, dict[str, Any] | None]:
    """Look up the first direct child template for a path (used without a pre-built index)."""
    index = _build_direct_child_index(path_items)
    return index.get(path_template, (None, None, None))


def _parent_collection_template(
    path_template: str,
    path_items: dict[str, dict[str, object]],
) -> tuple[str | None, dict[str, Any] | None]:
    segments = path_template.split("/")
    if len(segments) < 2 or not segments[-1].startswith("{") or not segments[-1].endswith("}"):
        return None, None
    parent_template = "/".join(segments[:-1])
    parent_item = path_items.get(parent_template)
    if not isinstance(parent_item, dict):
        return None, None
    parent_get = parent_item.get("get")
    if not isinstance(parent_get, dict):
        return None, None
    schema = _response_schema(parent_get)
    resolved = resolved_schema(schema)
    if resolved.get("type") != "array":
        return None, None
    item_schema = resolved.get("items") if isinstance(resolved.get("items"), dict) else None
    return parent_template, deepcopy(item_schema) if isinstance(item_schema, dict) else None


def _response_seed(path_template: str, method: str) -> str:
    return f"{method.lower()}_{path_template.strip('/').replace('/', '_')}_response"


def _apply_path_values(
    payload: Any, path_values: dict[str, Any], concrete_path: str, method: str
) -> Any:
    if isinstance(payload, dict):
        payload = deepcopy(payload)
        for key, value in path_values.items():
            if key in payload:
                payload[key] = value
        if "path" in payload and isinstance(payload["path"], str):
            payload["path"] = concrete_path
        if "method" in payload and isinstance(payload["method"], str):
            payload["method"] = method
        return payload
    if isinstance(payload, list):
        return [
            _apply_path_values(item, path_values, concrete_path, method)
            for item in deepcopy(payload)
        ]
    return payload


def _seed_collection(
    response_schema: dict[str, Any] | None,
    *,
    concrete_path: str,
    path_values: dict[str, Any],
) -> list[Any]:
    resolved = resolved_schema(response_schema)
    item_schema = resolved.get("items") if isinstance(resolved.get("items"), dict) else {}
    sample = sample_value_for_schema(item_schema, seed=f"{concrete_path}_item_0")
    sample = _apply_path_values(sample, path_values, concrete_path, "GET")
    return [sample]


def _filter_collection(items: list[Any], query_values: dict[str, Any]) -> list[Any]:
    if not query_values:
        return items

    filtered: list[Any] = []
    for item in items:
        if not isinstance(item, dict):
            filtered.append(item)
            continue
        include = True
        for key, value in query_values.items():
            if key not in item:
                continue
            if str(item[key]) != str(value):
                include = False
                break
        if include:
            filtered.append(item)
    return filtered


def _next_member_token(collection_items: list[Any], *, schema: dict[str, Any] | None) -> Any:
    resolved = resolved_schema(schema)
    if resolved.get("type") == "integer":
        return len(collection_items) + 1
    return f"generated-{len(collection_items) + 1}"


def _derive_member_token(
    *,
    body_value: Any,
    query_values: dict[str, Any],
    parameter_name: str | None,
    parameter_schema: dict[str, Any] | None,
    collection_items: list[Any],
) -> Any:
    if parameter_name:
        if isinstance(body_value, dict) and parameter_name in body_value:
            return body_value[parameter_name]
        if parameter_name in query_values:
            return query_values[parameter_name]
        if isinstance(body_value, dict):
            for alias in ("id", "name", "vmid", "userid", "tokenid", "storage", "group", "roleid"):
                if alias in body_value:
                    return body_value[alias]
    return _next_member_token(collection_items, schema=parameter_schema)


def _build_member_path(
    direct_child_template: str | None,
    *,
    parent_path_values: dict[str, Any],
    extra_param_name: str | None,
    extra_param_value: Any,
    collection_path: str,
    collection_size: int,
) -> str:
    if direct_child_template is None or extra_param_name is None:
        return f"{collection_path}#item-{collection_size + 1}"
    values = dict(parent_path_values)
    values[extra_param_name] = extra_param_value
    return _render_path(direct_child_template, values)


def _build_collection_member_payload(
    item_schema: dict[str, Any] | None,
    *,
    body_value: Any,
    concrete_member_path: str,
    path_values: dict[str, Any],
    extra_param_name: str | None,
    extra_param_value: Any,
) -> Any:
    override = body_value if body_value is not None else {}
    payload = merge_with_schema_defaults(item_schema, seed=concrete_member_path, override=override)
    if isinstance(payload, dict) and extra_param_name and extra_param_name in payload:
        payload[extra_param_name] = extra_param_value
    return _apply_path_values(payload, path_values, concrete_member_path, "GET")


def _build_object_payload(
    schema: dict[str, Any] | None,
    *,
    current_value: Any,
    body_value: Any,
    query_values: dict[str, Any],
    path_values: dict[str, Any],
    concrete_path: str,
    method: str,
) -> Any:
    override = body_value if body_value is not None else query_values or {}
    if method == "PUT":
        payload = merge_with_schema_defaults(schema, seed=concrete_path, override=override)
    elif method == "PATCH":
        payload = deepcopy(current_value)
        if isinstance(payload, dict) and isinstance(override, dict):
            payload.update(override)
        else:
            payload = merge_with_schema_defaults(schema, seed=concrete_path, override=override)
    else:
        if current_value is None:
            payload = merge_with_schema_defaults(schema, seed=concrete_path, override=override)
        elif isinstance(current_value, dict) and isinstance(override, dict):
            payload = deepcopy(current_value)
            payload.update(override)
        else:
            payload = deepcopy(current_value)
    return _apply_path_values(payload, path_values, concrete_path, method)


def _build_operation_response(
    topology: RouteTopology,
    *,
    concrete_path: str,
    state_value: Any,
    body_value: Any,
    path_values: dict[str, Any],
    query_values: dict[str, Any],
) -> Any:
    if topology.method == "GET":
        return state_value

    response_schema = topology.response_schema
    response_kind = schema_kind(response_schema)
    if response_kind == "none":
        return None
    if response_kind != "none" and response_kind == schema_kind_from_value(state_value):
        payload = deepcopy(state_value)
    else:
        override = body_value if body_value is not None else query_values or None
        payload = merge_with_schema_defaults(
            response_schema,
            seed=_response_seed(topology.path_template, topology.method),
            override=override,
        )
    return _apply_path_values(payload, path_values, concrete_path, topology.method)


def schema_kind_from_value(value: Any) -> str:
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if value is None:
        return "none"
    return "scalar"


def _resolve_get_state(
    topology: RouteTopology,
    *,
    store,
    concrete_path: str,
    path_values: dict[str, Any],
    query_values: dict[str, Any],
) -> Any:
    if topology.same_path_get_kind == "array":
        collection = store.get_collection(concrete_path)
        if collection is None:
            collection = _seed_collection(
                topology.same_path_get_schema,
                concrete_path=concrete_path,
                path_values=path_values,
            )
            store.replace_collection(concrete_path, collection)
        return _filter_collection(collection, query_values)

    if store.is_deleted(concrete_path):
        raise HTTPException(status_code=404, detail="Mock resource not found.")

    payload = store.get_object(concrete_path)
    if payload is None:
        payload = merge_with_schema_defaults(
            topology.same_path_get_schema,
            seed=_response_seed(topology.path_template, "GET"),
        )
        payload = _apply_path_values(payload, path_values, concrete_path, "GET")
        store.set_object(concrete_path, payload)
    return payload


def _mutate_collection_state(
    topology: RouteTopology,
    *,
    store,
    concrete_path: str,
    path_values: dict[str, Any],
    body_value: Any,
    query_values: dict[str, Any],
) -> Any:
    collection = store.get_collection(concrete_path)
    if collection is None:
        collection = _seed_collection(
            topology.same_path_get_schema,
            concrete_path=concrete_path,
            path_values=path_values,
        )
        store.replace_collection(concrete_path, collection)

    item_schema = None
    resolved_get_schema = resolved_schema(topology.same_path_get_schema)
    if isinstance(resolved_get_schema.get("items"), dict):
        item_schema = resolved_get_schema["items"]

    if topology.method == "DELETE":
        store.replace_collection(concrete_path, [])
        return []

    if isinstance(body_value, list) and topology.method == "PUT":
        replacement = [
            _apply_path_values(
                merge_with_schema_defaults(
                    item_schema, seed=f"{concrete_path}_{index}", override=value
                ),
                path_values,
                concrete_path,
                "GET",
            )
            for index, value in enumerate(body_value)
        ]
        store.replace_collection(concrete_path, replacement)
        return replacement

    member_token = _derive_member_token(
        body_value=body_value,
        query_values=query_values,
        parameter_name=topology.direct_child_param,
        parameter_schema=topology.direct_child_param_schema,
        collection_items=collection,
    )
    member_key = _build_member_path(
        topology.absolute_direct_child_template,
        parent_path_values=path_values,
        extra_param_name=topology.direct_child_param,
        extra_param_value=member_token,
        collection_path=concrete_path,
        collection_size=len(collection),
    )
    payload = _build_collection_member_payload(
        item_schema,
        body_value=body_value,
        concrete_member_path=member_key,
        path_values=path_values,
        extra_param_name=topology.direct_child_param,
        extra_param_value=member_token,
    )

    if topology.method == "PATCH":
        existing = store.get_object(member_key) or payload
        payload = _build_object_payload(
            item_schema,
            current_value=existing,
            body_value=body_value,
            query_values=query_values,
            path_values=path_values,
            concrete_path=member_key,
            method="PATCH",
        )

    store.upsert_collection_member(concrete_path, member_key, payload)
    store.set_object(member_key, payload)
    return payload


def _mutate_object_state(
    topology: RouteTopology,
    *,
    store,
    concrete_path: str,
    path_values: dict[str, Any],
    body_value: Any,
    query_values: dict[str, Any],
) -> Any:
    state_schema = (
        topology.same_path_get_schema
        or topology.parent_collection_item_schema
        or topology.response_schema
    )
    current_value = store.get_object(concrete_path)
    if current_value is None and topology.same_path_get_kind != "none":
        current_value = merge_with_schema_defaults(state_schema, seed=concrete_path)

    if topology.method == "DELETE":
        store.delete_object(concrete_path)
        if topology.absolute_parent_collection_template is not None:
            parent_path_values = {
                name: value
                for name, value in path_values.items()
                if name in extract_path_params(topology.parent_collection_template)
            }
            parent_path = _render_path(
                topology.absolute_parent_collection_template,
                parent_path_values,
            )
            store.delete_collection_member(parent_path, concrete_path)
        return current_value

    payload = _build_object_payload(
        state_schema,
        current_value=current_value,
        body_value=body_value,
        query_values=query_values,
        path_values=path_values,
        concrete_path=concrete_path,
        method=topology.method,
    )
    store.set_object(concrete_path, payload)

    if topology.absolute_parent_collection_template is not None:
        parent_path_values = {
            name: value
            for name, value in path_values.items()
            if name in extract_path_params(topology.parent_collection_template)
        }
        parent_path = _render_path(
            topology.absolute_parent_collection_template,
            parent_path_values,
        )
        if store.get_collection(parent_path) is None:
            store.replace_collection(
                parent_path,
                _seed_collection(
                    {"type": "array", "items": topology.parent_collection_item_schema or {}},
                    concrete_path=parent_path,
                    path_values=parent_path_values,
                ),
            )
        store.upsert_collection_member(parent_path, concrete_path, payload)

    return payload


def _apply_mutation(
    topology: RouteTopology,
    *,
    store,
    concrete_path: str,
    path_values: dict[str, Any],
    body_value: Any,
    query_values: dict[str, Any],
) -> Any:
    if topology.same_path_get_kind == "array":
        return _mutate_collection_state(
            topology,
            store=store,
            concrete_path=concrete_path,
            path_values=path_values,
            body_value=body_value,
            query_values=query_values,
        )
    return _mutate_object_state(
        topology,
        store=store,
        concrete_path=concrete_path,
        path_values=path_values,
        body_value=body_value,
        query_values=query_values,
    )


def _build_generated_endpoint(
    *,
    path_template: str,
    method: str,
    topology: RouteTopology,
    request_model: type | None,
    request_schema: dict[str, Any] | None,
    response_model: type | None,
    schema_key: str,
    namespace: str | None,
    owner_pid: int | None,
) -> object:
    path_param_name_map = _path_parameter_name_map(topology.operation)
    path_param_map = {
        python_name: original for original, python_name in path_param_name_map.items()
    }
    query_param_map: dict[str, str] = {}
    signature_parameters: list[inspect.Parameter] = []
    used_parameter_names: set[str] = set()

    def _unique_parameter_name(base: str) -> str:
        candidate = base
        suffix = 1
        while candidate in used_parameter_names:
            candidate = f"{base}_{suffix}"
            suffix += 1
        return candidate

    for parameter in _operation_parameters(topology.operation):
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
        if python_name in used_parameter_names:
            python_name = _unique_parameter_name(f"op_{python_name}")
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
            used_parameter_names.add(python_name)
            continue

        if location == "query":
            query_param_map[python_name] = original_name
            if not required:
                annotation = annotation | None
            signature_parameters.append(
                inspect.Parameter(
                    python_name,
                    inspect.Parameter.KEYWORD_ONLY,
                    annotation=annotation,
                    default=Query(... if required else None, description=description, alias=alias),
                )
            )
            used_parameter_names.add(python_name)

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
        path_values = {
            original_name: kwargs.pop(python_name)
            for python_name, original_name in path_param_map.items()
        }
        query_values = {
            original_name: kwargs.get(python_name)
            for python_name, original_name in query_param_map.items()
            if kwargs.get(python_name) is not None
        }
        body_value = _normalize_body_value(request_body)
        concrete_path = _render_path(path_template, path_values)
        store = shared_mock_store(
            schema_key,
            namespace=namespace,
            owner_pid=owner_pid,
        )

        try:
            if method == "GET":
                result = _resolve_get_state(
                    topology,
                    store=store,
                    concrete_path=concrete_path,
                    path_values=path_values,
                    query_values=query_values,
                )
            else:
                state_value = _apply_mutation(
                    topology,
                    store=store,
                    concrete_path=concrete_path,
                    path_values=path_values,
                    body_value=body_value,
                    query_values=query_values,
                )
                result = _build_operation_response(
                    topology,
                    concrete_path=concrete_path,
                    state_value=state_value,
                    body_value=body_value,
                    path_values=path_values,
                    query_values=query_values,
                )
        except HTTPException:
            raise
        except Exception as error:  # pragma: no cover - defensive surface
            raise ProxmoxOpenAPIException(
                message=f"Generated Proxmox mock route failed for {method} {path_template}.",
                detail="Schema-driven mock execution raised an unexpected exception.",
                python_exception=str(error),
            )

        if response_model is None:
            return result

        try:
            return response_model.model_validate(result)
        except Exception as error:
            fallback = merge_with_schema_defaults(
                topology.response_schema,
                seed=_response_seed(topology.path_template, method),
            )
            try:
                return response_model.model_validate(
                    _apply_path_values(fallback, path_values, concrete_path, method)
                )
            except Exception:
                raise ProxmoxOpenAPIException(
                    message=f"Generated Proxmox mock response validation failed for {method} {path_template}.",
                    detail="The synthesized mock response does not satisfy the generated model.",
                    python_exception=str(error),
                )

    generated_endpoint.__name__ = (
        f"{_GENERATED_ROUTE_NAME_PREFIX}{method.lower()}__"
        f"{_operation_id(topology.path_template, method, topology.operation)}"
    )
    generated_endpoint.__qualname__ = generated_endpoint.__name__
    generated_endpoint.__signature__ = inspect.Signature(
        parameters=signature_parameters,
        return_annotation=response_model or dict[str, object],
    )
    return generated_endpoint


def _build_topology(
    *,
    base_prefix: str,
    path_template: str,
    method: str,
    operation: dict[str, object],
    path_items: dict[str, dict[str, object]],
    direct_child_index: dict[str, tuple[str, str, dict[str, Any] | None]] | None = None,
) -> RouteTopology:
    same_path_get = path_items.get(path_template, {}).get("get")
    same_path_get_schema = (
        _response_schema(same_path_get) if isinstance(same_path_get, dict) else None
    )
    if direct_child_index is not None:
        direct_child_template, direct_child_param, direct_child_param_schema = (
            direct_child_index.get(path_template, (None, None, None))
        )
    else:
        direct_child_template, direct_child_param, direct_child_param_schema = (
            _direct_child_template(path_template, path_items)
        )
    parent_collection_template, parent_collection_item_schema = _parent_collection_template(
        path_template,
        path_items,
    )
    return RouteTopology(
        path_template=path_template,
        absolute_path_template=f"{base_prefix}{path_template}",
        method=method,
        operation=deepcopy(operation),
        request_schema=_request_schema_without_path_params(path_template, operation),
        response_schema=_response_schema(operation),
        same_path_get_schema=same_path_get_schema,
        same_path_get_kind=schema_kind(same_path_get_schema),
        direct_child_template=direct_child_template,
        absolute_direct_child_template=(
            f"{base_prefix}{direct_child_template}" if direct_child_template else None
        ),
        direct_child_param=direct_child_param,
        direct_child_param_schema=direct_child_param_schema,
        parent_collection_template=parent_collection_template,
        absolute_parent_collection_template=(
            f"{base_prefix}{parent_collection_template}" if parent_collection_template else None
        ),
        parent_collection_item_schema=parent_collection_item_schema,
    )


def register_generated_proxmox_mock_routes(
    app: FastAPI | APIRouter,
    *,
    version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG,
    openapi_document: dict[str, object] | None = None,
    namespace: str | None = None,
    owner_pid: int | None = None,
    custom_mock_data: dict[str, object] | None = None,
) -> dict[str, object]:
    """Register standalone schema-driven Proxmox mock routes on the FastAPI app."""

    document = openapi_document or load_proxmox_generated_openapi(version_tag=version_tag)
    if not document:
        raise ProxmoxOpenAPIException(
            message="Generated Proxmox OpenAPI schema not found.",
            detail=f"Unable to load version tag '{version_tag}'.",
        )

    model_module = _load_model_module(document, version_tag)
    document_fingerprint = schema_fingerprint(document)
    base_prefix = _server_prefix(document)
    path_items = {
        path_template: path_item
        for path_template, path_item in (document.get("paths") or {}).items()
        if isinstance(path_item, dict)
    }

    # Pre-build the child index once (O(P)) instead of scanning all paths per path (O(P²)).
    direct_child_index = _build_direct_child_index(path_items)

    route_names: set[str] = set()
    route_count = 0
    method_count = 0

    for path_template, path_item in sorted(path_items.items()):
        for method, operation in sorted(path_item.items()):
            method_name = method.upper()
            if method_name not in _SUPPORTED_GENERATED_METHODS or not isinstance(operation, dict):
                continue

            topology = _build_topology(
                path_template=path_template,
                method=method_name,
                operation=operation,
                path_items=path_items,
                base_prefix=base_prefix,
                direct_child_index=direct_child_index,
            )
            operation_id = _operation_id(path_template, method_name, operation)
            request_model = _operation_request_model(
                model_module,
                path_template,
                operation,
                operation_id,
            )
            response_model = _operation_response_model(model_module, operation_id)
            endpoint = _build_generated_endpoint(
                path_template=topology.absolute_path_template,
                method=method_name,
                topology=topology,
                request_model=request_model,
                request_schema=topology.request_schema,
                response_model=response_model,
                schema_key=document_fingerprint,
                namespace=namespace,
                owner_pid=owner_pid,
            )

            if custom_mock_data and topology.absolute_path_template in custom_mock_data:
                store = shared_mock_store(
                    document_fingerprint,
                    namespace=namespace,
                    owner_pid=owner_pid,
                )
                store.set_object(
                    topology.absolute_path_template,
                    custom_mock_data[topology.absolute_path_template],
                )

            route_name = f"{_GENERATED_ROUTE_NAME_PREFIX}{method_name.lower()}__{operation_id}"
            app.add_api_route(
                path=f"{base_prefix}{_mounted_fastapi_path(path_template, operation)}",
                endpoint=endpoint,
                methods=[method_name],
                name=route_name,
                summary=operation.get("summary"),
                description=operation.get("description"),
                response_model=response_model,
                tags=["proxmox mock / generated"],
            )
            route_names.add(route_name)
            route_count += 1
            method_count += 1

    _GENERATED_ROUTE_STATE["route_names"] = route_names
    _GENERATED_ROUTE_STATE["route_count"] = route_count
    _GENERATED_ROUTE_STATE["path_count"] = len(path_items)
    _GENERATED_ROUTE_STATE["method_count"] = method_count
    _GENERATED_ROUTE_STATE["schema_version"] = document.get("info", {}).get("version", version_tag)
    app.openapi_schema = None

    return {
        "route_count": route_count,
        "path_count": len(path_items),
        "method_count": method_count,
        "schema_version": _GENERATED_ROUTE_STATE["schema_version"],
        "base_prefix": base_prefix or "/",
    }


def generated_proxmox_mock_route_state() -> dict[str, object]:
    """Return metadata about the currently mounted mock route set."""

    return {
        "route_count": _GENERATED_ROUTE_STATE["route_count"],
        "path_count": _GENERATED_ROUTE_STATE["path_count"],
        "method_count": _GENERATED_ROUTE_STATE["method_count"],
        "schema_version": _GENERATED_ROUTE_STATE["schema_version"],
    }
