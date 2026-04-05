"""Typed models used by the Proxmox API Viewer code generation pipeline."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, field_validator

from proxmox_openapi.schema import ProxmoxSchemaValue

HTTP_METHODS = ("GET", "POST", "PUT", "DELETE")


class RawMethodCapture(BaseModel):
    """Captured method payload from the API Viewer UI and apidoc tree."""

    model_config = ConfigDict(extra="allow")

    method: str
    path: str
    method_name: str | None = None
    description: str | None = None
    viewer_description: str | None = None
    viewer_usage: str | None = None
    parameters: dict[str, object] | None = None
    returns: dict[str, object] | None = None
    permissions: dict[str, object] | None = None
    allowtoken: int | str | None = None
    protected: int | str | None = None
    unstable: int | str | None = None
    raw_sections: list[str] = Field(default_factory=list)
    source: str = "viewer"

    @field_validator("raw_sections", mode="before")
    @classmethod
    def _coerce_raw_sections(cls, value: object) -> list[str]:
        if isinstance(value, list):
            return [item for item in value if isinstance(item, str)]
        return []

    @field_validator("method")
    @classmethod
    def _normalize_method(cls, value: str) -> str:
        return value.upper()


class EndpointCapture(BaseModel):
    """Captured endpoint node from API Viewer traversal."""

    model_config = ConfigDict(extra="allow")

    path: str
    text: str | None = None
    leaf: int | bool | None = None
    methods: dict[str, RawMethodCapture] = Field(default_factory=dict)

    @field_validator("methods", mode="before")
    @classmethod
    def _coerce_methods(cls, value: object) -> dict[str, object]:
        if isinstance(value, dict):
            return value
        return {}


class NormalizedOperation(BaseModel):
    """Normalized operation model ready for OpenAPI conversion."""

    model_config = ConfigDict(extra="allow")

    method: str
    path: str
    operation_id: str
    summary: str | None = None
    description: str | None = None
    path_params: list[dict[str, object]] = Field(default_factory=list)
    query_params: list[dict[str, object]] = Field(default_factory=list)
    request_body_schema: dict[str, object] | None = None
    response_schema: dict[str, object] | None = None
    extra: dict[str, object] = Field(default_factory=dict)

    @field_validator("method")
    @classmethod
    def _normalize_method(cls, value: str) -> str:
        return value.upper()

    @field_validator("path")
    @classmethod
    def _normalize_path(cls, value: str) -> str:
        return value if value.startswith("/") else f"/{value}"

    @field_validator("path_params", "query_params", mode="before")
    @classmethod
    def _coerce_param_list(cls, value: object) -> list[dict[str, object]]:
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        return []

    @field_validator("extra", mode="before")
    @classmethod
    def _coerce_extra(cls, value: object) -> dict[str, object]:
        if isinstance(value, dict):
            return value
        return {}

    @classmethod
    def from_capture(
        cls,
        *,
        path: str,
        method: str,
        method_data: RawMethodCapture,
    ) -> Self:
        """Build a normalized operation from a validated raw method capture."""

        parameters = ProxmoxSchemaValue.model_validate(
            method_data.parameters or {"type": "object"}
        ).normalize_proxmox_schema() or {"type": "object"}
        returns = ProxmoxSchemaValue.model_validate(
            method_data.returns or {"type": "object"}
        ).normalize_proxmox_schema() or {"type": "object"}

        path_params = cls._build_path_params(path=path, parameters=parameters)
        query_params = cls._build_query_params(path=path, parameters=parameters)
        return cls(
            method=method,
            path=path,
            operation_id=cls._operation_id(path=path, method=method),
            summary=method_data.method_name,
            description=cls._compose_description(method_data),
            path_params=path_params,
            query_params=query_params,
            request_body_schema=(
                parameters
                if method in {"POST", "PUT", "DELETE"} and bool(parameters.get("properties"))
                else None
            ),
            response_schema=returns,
            extra={
                "permissions": method_data.permissions,
                "allowtoken": method_data.allowtoken,
                "protected": method_data.protected,
                "unstable": method_data.unstable,
                "raw_sections": method_data.raw_sections,
                "source": method_data.source,
                "viewer_sections": {
                    "description": method_data.viewer_description,
                    "usage": method_data.viewer_usage,
                    "short_description": method_data.description,
                },
            },
        )

    @staticmethod
    def _operation_id(path: str, method: str) -> str:
        from proxmox_openapi.proxmox_codegen.utils import slugify_identifier

        path_token = path.strip("/").replace("{", "").replace("}", "") or "root"
        return slugify_identifier(f"{method.lower()}_{path_token}")

    @staticmethod
    def _compose_description(method_data: RawMethodCapture) -> str | None:
        parts: list[str] = []
        if (
            isinstance(method_data.viewer_description, str)
            and method_data.viewer_description.strip()
        ):
            parts.append(method_data.viewer_description.strip())
        elif isinstance(method_data.description, str) and method_data.description.strip():
            parts.append(method_data.description.strip())

        if isinstance(method_data.viewer_usage, str) and method_data.viewer_usage.strip():
            usage = method_data.viewer_usage.strip()
            parts.append(f"## Usage\n{usage}")

        if not parts:
            return None
        return "\n\n".join(parts)

    @staticmethod
    def _build_path_params(
        *,
        path: str,
        parameters: dict[str, object],
    ) -> list[dict[str, object]]:
        from proxmox_openapi.proxmox_codegen.utils import extract_path_params

        out: list[dict[str, object]] = []
        for param in extract_path_params(path):
            pdef = {}
            if isinstance(parameters.get("properties"), dict):
                pdef = parameters["properties"].get(param, {}) or {}
            base = pdef if isinstance(pdef, dict) else {}
            out.append(
                {
                    "name": param,
                    "in": "path",
                    "required": True,
                    "description": base.get("description"),
                    "schema": {
                        "type": base.get("type", "string"),
                        **({"enum": base["enum"]} if "enum" in base else {}),
                        **({"pattern": base["pattern"]} if "pattern" in base else {}),
                        **(
                            {"format": base["format"]}
                            if isinstance(base.get("format"), str)
                            else {}
                        ),
                    },
                    "x-proxmox": {
                        "raw": ProxmoxSchemaValue.model_validate(
                            {"type": "object", "properties": {param: pdef}}
                        ).normalize_proxmox_schema()
                    },
                }
            )
        return out

    @staticmethod
    def _build_query_params(
        *,
        path: str,
        parameters: dict[str, object],
    ) -> list[dict[str, object]]:
        from proxmox_openapi.proxmox_codegen.utils import extract_path_params

        path_param_names = set(extract_path_params(path))
        out: list[dict[str, object]] = []
        properties = parameters.get("properties", {}) if isinstance(parameters, dict) else {}
        if not isinstance(properties, dict):
            return out

        for name, pdef in sorted(properties.items()):
            if name in path_param_names:
                continue
            if not isinstance(pdef, dict):
                continue
            out.append(
                {
                    "name": name,
                    "in": "query",
                    "required": not ProxmoxSchemaValue._is_optional(pdef.get("optional")),
                    "description": pdef.get("description"),
                    "schema": {
                        "type": pdef.get("type", "string"),
                        **({"enum": pdef["enum"]} if "enum" in pdef else {}),
                        **({"pattern": pdef["pattern"]} if "pattern" in pdef else {}),
                        **({"default": pdef["default"]} if "default" in pdef else {}),
                        **({"minimum": pdef["minimum"]} if "minimum" in pdef else {}),
                        **({"maximum": pdef["maximum"]} if "maximum" in pdef else {}),
                    },
                    "x-proxmox": {"raw": pdef},
                }
            )
        return out


class GenerationBundle(BaseModel):
    """Final bundle returned by the Proxmox generation pipeline."""

    model_config = ConfigDict(extra="allow")

    source_url: str
    version_tag: str
    generated_at: str
    endpoint_count: int
    operation_count: int
    capture: dict[str, object]
    openapi: dict[str, object]
    pydantic_models_code: str


__all__ = [
    "RawMethodCapture",
    "EndpointCapture",
    "NormalizedOperation",
    "GenerationBundle",
    "HTTP_METHODS",
]
