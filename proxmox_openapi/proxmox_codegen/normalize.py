"""Normalization layer from Proxmox API Viewer captures into OpenAPI-ready operations."""

from __future__ import annotations

from proxmox_openapi.proxmox_codegen.models import (
    HTTP_METHODS,
    EndpointCapture,
    NormalizedOperation,
)


def normalize_captured_endpoints(
    endpoint_map: dict[str, dict[str, object]],
) -> list[NormalizedOperation]:
    """Convert capture endpoint map into normalized operation list."""

    operations: list[NormalizedOperation] = []

    for path in sorted(endpoint_map):
        endpoint = EndpointCapture.model_validate(endpoint_map[path])
        methods = endpoint.methods

        for method in HTTP_METHODS:
            method_data = methods.get(method)
            if not method_data:
                continue

            operations.append(
                NormalizedOperation.from_capture(path=path, method=method, method_data=method_data)
            )

    return operations
