"""Schema helpers for generated mock routes."""

from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from typing import Any

from proxmox_openapi.schema import GeneratedOpenAPIDocument, ProxmoxSchemaValue


def schema_fingerprint(openapi_document: dict[str, object]) -> str:
    """Return a stable fingerprint for the loaded OpenAPI document."""
    return GeneratedOpenAPIDocument.model_validate(openapi_document).fingerprint()


def resolved_schema(schema: dict[str, Any] | None) -> dict[str, Any]:
    """Resolve the most useful inline schema representation for mock generation."""
    return ProxmoxSchemaValue.model_validate(schema).resolved()


def schema_kind(schema: dict[str, Any] | None) -> str:
    """Classify the resolved schema into a small set of storage kinds."""
    return ProxmoxSchemaValue.model_validate(schema).kind()


def _seed_int(seed: str, *, modulus: int, offset: int = 0) -> int:
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
    return (int(digest[:8], 16) % modulus) + offset


def _field_hint(field_name: str | None) -> str:
    return (field_name or "").strip().lower()


def _select_enum_value(enum: list[Any], *, field_name: str | None) -> Any:
    if not enum:
        return None

    hint = _field_hint(field_name)
    preferred_values = {
        "status": ("running", "online", "ok", "enabled", "active"),
        "type": ("qemu", "lxc", "node", "storage", "dir", "lvmthin"),
    }
    if hint in preferred_values:
        for preferred in preferred_values[hint]:
            if preferred in enum:
                return deepcopy(preferred)

    return deepcopy(enum[0])


def _semantic_string_value(*, field_name: str | None, seed: str) -> str | None:  # noqa: C901
    hint = _field_hint(field_name)
    if not hint:
        return None

    host_idx = _seed_int(seed, modulus=8, offset=1)
    vm_idx = _seed_int(seed, modulus=49, offset=1)
    ip_octet = _seed_int(seed, modulus=200, offset=20)

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
        "id": f"qemu/{100 + _seed_int(seed, modulus=800)}",
    }
    if hint in exact_map:
        return exact_map[hint]

    if hint in {"ip", "ipaddr", "address", "clientip", "serverip"}:
        return f"10.20.{host_idx}.{ip_octet}"
    if hint in {"cidr", "subnet"}:
        return f"10.20.{host_idx}.0/24"
    if hint in {"mac", "macaddr", "hwaddr"}:
        first = 0x52
        b2 = _seed_int(seed + "m2", modulus=256)
        b3 = _seed_int(seed + "m3", modulus=256)
        b4 = _seed_int(seed + "m4", modulus=256)
        b5 = _seed_int(seed + "m5", modulus=256)
        b6 = _seed_int(seed + "m6", modulus=256)
        return f"{first:02X}:{b2:02X}:{b3:02X}:{b4:02X}:{b5:02X}:{b6:02X}"
    if hint in {"net0", "net1", "net2", "net3"}:
        mac = _semantic_string_value(field_name="mac", seed=seed) or "52:54:00:00:00:01"
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


def _semantic_integer_value(*, field_name: str | None, seed: str) -> int | None:
    hint = _field_hint(field_name)
    if not hint:
        return None

    exact_map = {
        "vmid": 100 + _seed_int(seed, modulus=800),
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
        "uptime": 86400 * 13 + _seed_int(seed, modulus=5000),
        "pid": 1000 + _seed_int(seed, modulus=50000),
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
        return _seed_int(seed, modulus=10_000_000, offset=500_000)

    return None


def _semantic_number_value(*, field_name: str | None, seed: str) -> float | None:
    hint = _field_hint(field_name)
    if not hint:
        return None

    if hint == "cpu":
        return round((_seed_int(seed, modulus=40, offset=10)) / 100.0, 2)
    if hint in {"loadavg", "iowait"}:
        return round((_seed_int(seed, modulus=30, offset=5)) / 100.0, 2)

    return None


def _semantic_boolean_value(*, field_name: str | None) -> bool | None:
    hint = _field_hint(field_name)
    if not hint:
        return None

    if hint in {"template", "suspended", "paused", "stopped"}:
        return False
    if hint in {"active", "enabled", "online", "running"}:
        return True

    return None


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
