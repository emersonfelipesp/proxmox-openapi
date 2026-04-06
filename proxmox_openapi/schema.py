"""Schema management for Proxmox OpenAPI."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, RootModel, ValidationError, field_validator

from proxmox_openapi.proxmox_codegen.security import validate_version_tag

DEFAULT_PROXMOX_OPENAPI_TAG = "latest"


class GeneratedOpenAPIDocument(BaseModel):
    """Validated OpenAPI document loaded from generated artifacts."""

    model_config = ConfigDict(extra="allow")

    openapi: str = "3.1.0"
    info: dict[str, Any]
    servers: list[dict[str, Any]] = Field(default_factory=list)
    paths: dict[str, dict[str, Any]] = Field(default_factory=dict)

    @field_validator("servers", mode="before")
    @classmethod
    def _validate_servers(cls, value: Any) -> list[dict[str, Any]]:
        if not isinstance(value, list):
            return []
        return [item for item in value if isinstance(item, dict)]

    @field_validator("paths", mode="before")
    @classmethod
    def _validate_paths(cls, value: Any) -> dict[str, dict[str, Any]]:
        if not isinstance(value, dict):
            return {}
        return {path: item for path, item in value.items() if isinstance(item, dict)}

    @classmethod
    def load_from_version(
        cls,
        version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG,
    ) -> Self | None:
        """Load and validate a generated OpenAPI document for a version tag."""
        try:
            version_tag = validate_version_tag(version_tag)
        except ValueError:
            return None

        openapi_path = _generated_dir() / version_tag / "openapi.json"
        if not openapi_path.exists():
            return None

        try:
            payload = openapi_path.read_text(encoding="utf-8")
        except OSError:
            return None

        try:
            return cls.model_validate_json(payload)
        except ValidationError:
            return None

    def fingerprint(self) -> str:
        """Return a stable fingerprint for the document."""
        payload = self.model_dump(mode="python", exclude_none=False)
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def server_prefix(self) -> str:
        """Return the first server URL prefix, if present."""
        if not self.servers:
            return ""
        first = self.servers[0]
        url = first.get("url")
        if isinstance(url, str):
            return url.rstrip("/")
        return ""


class MockDataDocument(RootModel[dict[str, Any]]):
    """Validated custom mock-data mapping."""

    @classmethod
    def load_from_path(cls, file_path: str | Path | None = None) -> Self | None:
        """Load and validate mock data from a JSON or YAML file."""
        if file_path is None:
            return None
        path = Path(file_path)
        if not path.exists():
            return None

        try:
            content = path.read_text(encoding="utf-8")
        except OSError:
            return None

        suffix = path.suffix.lower()
        if suffix in {".yaml", ".yml"}:
            try:
                import yaml

                data = yaml.safe_load(content)
            except ImportError:
                return None
            except yaml.YAMLError:
                return None
        elif suffix == ".json":
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                return None
        else:
            return None

        try:
            return cls.model_validate(data)
        except ValidationError:
            return None


class ProxmoxSchemaValue(RootModel[Any]):
    """Pydantic wrapper around a JSON Schema value used by the codegen pipeline."""

    @field_validator("root", mode="before")
    @classmethod
    def _validate_root(cls, value: Any) -> Any:
        return value

    @staticmethod
    def _seed_int(seed: str, *, modulus: int, offset: int = 0) -> int:
        digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
        return (int(digest[:8], 16) % modulus) + offset

    @staticmethod
    def _field_hint(field_name: str | None) -> str:
        return (field_name or "").strip().lower()

    @staticmethod
    def _select_enum_value(enum: list[Any], *, field_name: str | None) -> Any:
        if not enum:
            return None

        hint = ProxmoxSchemaValue._field_hint(field_name)
        preferred_values = {
            "status": ("running", "online", "ok", "enabled", "active"),
            "type": ("qemu", "lxc", "node", "storage", "dir", "lvmthin"),
        }
        if hint in preferred_values:
            for preferred in preferred_values[hint]:
                if preferred in enum:
                    return deepcopy(preferred)

        return deepcopy(enum[0])

    @staticmethod
    def _semantic_string_value(*, field_name: str | None, seed: str) -> str | None:  # noqa: C901
        hint = ProxmoxSchemaValue._field_hint(field_name)
        if not hint:
            return None

        host_idx = ProxmoxSchemaValue._seed_int(seed, modulus=8, offset=1)
        vm_idx = ProxmoxSchemaValue._seed_int(seed, modulus=49, offset=1)
        ip_octet = ProxmoxSchemaValue._seed_int(seed, modulus=200, offset=20)

        exact_map = {
            "node": f"pve-node-{host_idx:02d}",
            "nodename": f"pve-node-{host_idx:02d}",
            "hostname": f"pve-node-{host_idx:02d}.example.local",
            "name": f"vm-app-{vm_idx:02d}",
            "vmname": f"vm-app-{vm_idx:02d}",
            "storage": "local-lvm",
            "pool": "production",
            "status": "running",
            "type": "qemu",
            "ostype": "l26",
            "bridge": "vmbr0",
            "gateway": "10.20.30.1",
            "userid": "root@pam",
            "tokenid": "automation-token",
            "roleid": "PVEAdmin",
            "group": "admins",
            "realm": "pam",
            "id": f"qemu/{100 + ProxmoxSchemaValue._seed_int(seed, modulus=800)}",
        }
        if hint in exact_map:
            return exact_map[hint]

        if hint in {"ip", "ipaddr", "address", "clientip", "serverip"}:
            return f"10.20.{host_idx}.{ip_octet}"
        if hint in {"cidr", "subnet"}:
            return f"10.20.{host_idx}.0/24"
        if hint in {"mac", "macaddr", "hwaddr"}:
            first = 0x52
            b2 = ProxmoxSchemaValue._seed_int(seed + "m2", modulus=256)
            b3 = ProxmoxSchemaValue._seed_int(seed + "m3", modulus=256)
            b4 = ProxmoxSchemaValue._seed_int(seed + "m4", modulus=256)
            b5 = ProxmoxSchemaValue._seed_int(seed + "m5", modulus=256)
            b6 = ProxmoxSchemaValue._seed_int(seed + "m6", modulus=256)
            return f"{first:02X}:{b2:02X}:{b3:02X}:{b4:02X}:{b5:02X}:{b6:02X}"
        if hint in {"net0", "net1", "net2", "net3"}:
            mac = (
                ProxmoxSchemaValue._semantic_string_value(field_name="mac", seed=seed)
                or "52:54:00:00:00:01"
            )
            return f"virtio={mac},bridge=vmbr0,firewall=1"
        if hint in {"interface", "iface"}:
            return "eno1"
        if hint == "digest":
            return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:40]
        if hint.endswith("url"):
            return "https://pve.example.local:8006"

        if re.search(r"(^|_)name$", hint):
            return f"resource-{vm_idx:02d}"

        return None

    @staticmethod
    def _semantic_integer_value(*, field_name: str | None, seed: str) -> int | None:
        hint = ProxmoxSchemaValue._field_hint(field_name)
        if not hint:
            return None

        exact_map = {
            "vmid": 100 + ProxmoxSchemaValue._seed_int(seed, modulus=800),
            "maxcpu": 8,
            "cpus": 8,
            "cores": 4,
            "sockets": 1,
            "vcpus": 4,
            "maxmem": 16 * 1024**3,
            "mem": 6 * 1024**3,
            "memory": 6 * 1024**3,
            "maxdisk": 120 * 1024**3,
            "disk": 48 * 1024**3,
            "uptime": 86400 * 13 + ProxmoxSchemaValue._seed_int(seed, modulus=5000),
            "pid": 1000 + ProxmoxSchemaValue._seed_int(seed, modulus=50000),
            "port": 8006,
            "starttime": 1767225600,
            "endtime": 1767229200,
            "ctime": 1767000000,
        }
        if hint in exact_map:
            return exact_map[hint]

        if hint in {"used", "usedbytes"}:
            return 48 * 1024**3
        if hint in {"avail", "available", "free"}:
            return 72 * 1024**3
        if hint in {"total", "size"}:
            return 120 * 1024**3
        if hint in {"netin", "netout", "diskread", "diskwrite"}:
            return ProxmoxSchemaValue._seed_int(seed, modulus=10_000_000, offset=500_000)

        return None

    @staticmethod
    def _semantic_number_value(*, field_name: str | None, seed: str) -> float | None:
        hint = ProxmoxSchemaValue._field_hint(field_name)
        if not hint:
            return None

        if hint == "cpu":
            return round((ProxmoxSchemaValue._seed_int(seed, modulus=40, offset=10)) / 100.0, 2)
        if hint in {"loadavg", "iowait"}:
            return round((ProxmoxSchemaValue._seed_int(seed, modulus=30, offset=5)) / 100.0, 2)

        return None

    @staticmethod
    def _semantic_boolean_value(*, field_name: str | None) -> bool | None:
        hint = ProxmoxSchemaValue._field_hint(field_name)
        if not hint:
            return None

        if hint in {"template", "suspended", "paused", "stopped"}:
            return False
        if hint in {"active", "enabled", "online", "running"}:
            return True

        return None

    @staticmethod
    def _is_optional(value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes"}
        return False

    @staticmethod
    def _to_bool(value: object) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            v = value.strip().lower()
            if v in {"1", "true", "yes", "on"}:
                return True
            if v in {"0", "false", "no", "off", ""}:
                return False
        return bool(value)

    @staticmethod
    def _deep_merge(base: Any, override: Any) -> Any:
        if isinstance(base, dict) and isinstance(override, dict):
            merged = deepcopy(base)
            for key, value in override.items():
                if key in merged:
                    merged[key] = ProxmoxSchemaValue._deep_merge(merged[key], value)
                else:
                    merged[key] = deepcopy(value)
            return merged
        return deepcopy(override)

    def resolved(self) -> dict[str, Any]:
        """Resolve the most useful inline schema representation."""
        schema = self.root
        if not isinstance(schema, dict):
            return {}
        if isinstance(schema.get("allOf"), list) and schema["allOf"]:
            merged: dict[str, Any] = {}
            for branch in schema["allOf"]:
                branch_schema = ProxmoxSchemaValue.model_validate(
                    branch if isinstance(branch, dict) else {}
                ).resolved()
                merged = self._deep_merge(merged, branch_schema)
            return merged
        for keyword in ("oneOf", "anyOf"):
            branches = schema.get(keyword)
            if isinstance(branches, list):
                for branch in branches:
                    branch_schema = ProxmoxSchemaValue.model_validate(
                        branch if isinstance(branch, dict) else {}
                    ).resolved()
                    if branch_schema.get("type") != "null":
                        return branch_schema
        return schema

    def kind(self) -> str:
        """Classify the schema into a small set of storage kinds."""
        resolved = self.resolved()
        if not resolved:
            return "none"
        schema_type = resolved.get("type")
        if schema_type == "array":
            return "array"
        if schema_type == "object":
            return "object"
        if schema_type is None and isinstance(resolved.get("properties"), dict):
            return "object"
        return "scalar"

    def normalize_proxmox_schema(self) -> dict[str, Any] | None:  # noqa: C901
        """Normalize Proxmox capture schemas into JSON Schema-compatible form."""
        schema = self.root
        if schema is None:
            return None

        obj = deepcopy(schema)
        if not isinstance(obj, dict):
            return {"type": "string", "x-proxmox-original": obj}

        additional = obj.get("additionalProperties")
        if isinstance(additional, (int, str, bool)):
            obj["additionalProperties"] = self._to_bool(additional)

        if "properties" in obj and isinstance(obj["properties"], dict):
            required = []
            for name, pdef in obj["properties"].items():
                if not isinstance(pdef, dict):
                    continue
                optional = pdef.get("optional")
                if not self._is_optional(optional):
                    required.append(name)
                if isinstance(pdef.get("additionalProperties"), (int, str, bool)):
                    pdef["additionalProperties"] = self._to_bool(pdef["additionalProperties"])

            if required:
                obj["required"] = sorted(set(required))

        schema_type = obj.get("type")
        if not schema_type:
            if "items" in obj:
                obj["type"] = "array"
            elif "properties" in obj:
                obj["type"] = "object"

        return obj

    def sample_value(self, seed: str, field_name: str | None = None) -> Any:  # noqa: C901
        """Build a deterministic mock value for the schema."""
        schema = self.resolved()
        if not schema:
            return {}

        if "const" in schema:
            return deepcopy(schema["const"])

        if "default" in schema:
            return deepcopy(schema["default"])

        enum = schema.get("enum")
        if isinstance(enum, list) and enum:
            return self._select_enum_value(enum, field_name=field_name)

        schema_type = schema.get("type")
        if schema_type == "null":
            return None
        if schema_type == "string":
            pattern = schema.get("pattern")
            if pattern == "[0-9a-fA-F]{8,64}":
                return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
            if schema.get("format") == "date-time":
                return "2026-01-01T00:00:00Z"
            if schema.get("format") == "date":
                return "2026-01-01"
            semantic_string = self._semantic_string_value(field_name=field_name, seed=seed)
            if semantic_string is not None:
                return semantic_string
            return seed
        if schema_type == "integer":
            semantic_int = self._semantic_integer_value(field_name=field_name, seed=seed)
            if semantic_int is not None:
                return semantic_int
            digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
            return int(digest[:6], 16) % 10_000 or 1
        if schema_type == "number":
            semantic_number = self._semantic_number_value(field_name=field_name, seed=seed)
            if semantic_number is not None:
                return semantic_number
            digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
            return float((int(digest[:6], 16) % 10_000) / 100)
        if schema_type == "boolean":
            semantic_bool = self._semantic_boolean_value(field_name=field_name)
            if semantic_bool is not None:
                return semantic_bool
            return True
        if schema_type == "array":
            item_schema = schema.get("items") if isinstance(schema.get("items"), dict) else {}
            return [
                ProxmoxSchemaValue.model_validate(item_schema).sample_value(
                    seed=f"{seed}_item_0",
                    field_name=field_name,
                )
            ]

        properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
        if properties:
            payload: dict[str, Any] = {}
            for name, property_schema in sorted(properties.items()):
                payload[name] = ProxmoxSchemaValue.model_validate(
                    property_schema if isinstance(property_schema, dict) else {}
                ).sample_value(seed=f"{seed}_{name}", field_name=name)
            return payload

        additional_properties = schema.get("additionalProperties")
        if isinstance(additional_properties, dict):
            return {
                "key": ProxmoxSchemaValue.model_validate(additional_properties).sample_value(
                    seed=f"{seed}_value",
                    field_name="value",
                ),
            }

        return {}

    def merge_defaults(self, seed: str, override: Any | None = None) -> Any:
        """Merge an override into a deterministic schema-backed seed value."""
        seeded_value = self.sample_value(seed=seed)
        if override is None:
            return seeded_value
        if isinstance(seeded_value, dict) and isinstance(override, dict):
            return self._deep_merge(seeded_value, override)
        if isinstance(seeded_value, list) and isinstance(override, list):
            return deepcopy(override)
        if override == {} and isinstance(seeded_value, (dict, list)):
            return seeded_value
        return deepcopy(override)


def _generated_dir() -> Path:
    """Return the generated artifacts directory."""
    return Path(__file__).resolve().parent / "generated" / "proxmox"


def available_proxmox_openapi_versions() -> list[str]:
    """Return list of available Proxmox OpenAPI version tags."""
    generated = _generated_dir()
    if not generated.exists():
        return []

    versions = []
    for item in generated.iterdir():
        if item.is_dir() and (item / "openapi.json").exists():
            versions.append(item.name)

    return sorted(versions, key=lambda v: (0 if v == DEFAULT_PROXMOX_OPENAPI_TAG else 1, v))


def load_proxmox_generated_openapi(
    version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG,
) -> dict[str, Any] | None:
    """Load generated OpenAPI schema for a specific version tag."""
    document = GeneratedOpenAPIDocument.load_from_version(version_tag=version_tag)
    if document is None:
        return None
    return document.model_dump(mode="python")


def load_pydantic_models(version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG) -> str | None:
    """Load generated Pydantic models for a specific version tag."""
    try:
        version_tag = validate_version_tag(version_tag)
    except ValueError:
        return None

    models_path = _generated_dir() / version_tag / "pydantic_models.py"
    if not models_path.exists():
        return None

    try:
        return models_path.read_text(encoding="utf-8")
    except OSError:
        return None


__all__ = [
    "DEFAULT_PROXMOX_OPENAPI_TAG",
    "GeneratedOpenAPIDocument",
    "available_proxmox_openapi_versions",
    "MockDataDocument",
    "ProxmoxSchemaValue",
    "load_proxmox_generated_openapi",
    "load_pydantic_models",
]
