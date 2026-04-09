"""Custom mock data loader for Proxmox OpenAPI.

Loads user-provided mock data from JSON or YAML files.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

DEFAULT_MOCK_DATA_PATH = "/etc/proxmox-openapi/mock-data.json"

ENV_VAR_NAME = "PROXMOX_MOCK_DATA_PATH"


def get_mock_data_path() -> str | None:
    """Get mock data path from environment variable or default."""
    return os.environ.get(ENV_VAR_NAME, DEFAULT_MOCK_DATA_PATH)


def load_mock_data(file_path: str | Path | None = None) -> dict[str, Any] | None:
    """Load custom mock data from a JSON or YAML file.

    Args:
        file_path: Path to the mock data file. If None, uses environment variable
                   or default path.

    Returns:
        Dictionary of mock data keyed by endpoint path, or None if not found.
    """
    path = file_path or get_mock_data_path()
    if not path:
        return None

    file_path_obj = Path(path)
    try:
        content = file_path_obj.read_text(encoding="utf-8")
    except OSError:
        return None

    suffix = file_path_obj.suffix.lower()
    if suffix in (".yaml", ".yml"):
        return _load_yaml(content)
    if suffix == ".json":
        return _load_json(content)

    return None


def _load_json(content: str) -> dict[str, Any] | None:
    """Load JSON content."""
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return None

    if not isinstance(data, dict):
        return None

    return data


def _load_yaml(content: str) -> dict[str, Any] | None:
    """Load YAML content."""
    try:
        import yaml

        data = yaml.safe_load(content)
    except ImportError:
        return None
    except yaml.YAMLError:
        return None

    if not isinstance(data, dict):
        return None

    return data


__all__ = [
    "DEFAULT_MOCK_DATA_PATH",
    "ENV_VAR_NAME",
    "get_mock_data_path",
    "load_mock_data",
]
