"""Utility functions for CLI operations."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

from .exceptions import ParameterError, PathError


def validate_api_path(path: str) -> str:
    """Validate and normalize an API path.

    Args:
        path: API path (e.g., "/nodes", "/nodes/pve1/qemu/100")

    Returns:
        Normalized path

    Raises:
        PathError: If path is invalid
    """
    if not path:
        raise PathError("Path cannot be empty")

    if not path.startswith("/"):
        raise PathError("Path must start with /", path=path)

    # Normalize multiple slashes
    normalized = "/".join(part for part in path.split("/") if part)
    normalized = "/" + normalized

    # Reject path traversal attempts
    components = normalized.split("/")
    if ".." in components or "." in components:
        raise PathError("Path must not contain '.' or '..' segments", path=path)

    return normalized


def parse_parameter_data(
    *,
    short_params: list[str] | None = None,
    cli_params: dict[str, Any] | None = None,
    json_file: str | None = None,
) -> dict[str, Any]:
    """Parse and merge multiple parameter formats.

    Args:
        short_params: List of "key=value" strings from -d option
        cli_params: Dictionary of CLI argument parameters
        json_file: Path to JSON file with parameters

    Returns:
        Merged dictionary of all parameters

    Raises:
        ParameterError: If parameters are invalid
    """
    result: dict[str, Any] = {}

    # Load from JSON file if provided
    if json_file:
        try:
            from pathlib import Path

            content = Path(json_file).read_text()
            file_params = json.loads(content)
            if isinstance(file_params, dict):
                result.update(file_params)
            else:
                raise ParameterError(
                    f"JSON file must contain object, got {type(file_params).__name__}",
                    param="json_file",
                )
        except FileNotFoundError:
            raise ParameterError(f"JSON file not found: {json_file}", param="json_file")
        except json.JSONDecodeError as e:
            raise ParameterError(f"Invalid JSON in file: {e}", param="json_file")

    # Parse short-form parameters (-d "key=value")
    if short_params:
        for param in short_params:
            if "=" not in param:
                raise ParameterError(f"Parameter must be key=value format: {param}")

            key, value = param.split("=", 1)
            result[key.strip()] = _coerce_value(value.strip())

    # Merge CLI parameters
    if cli_params:
        for key, value in cli_params.items():
            result[key] = _coerce_value(value) if isinstance(value, str) else value

    return result


def _coerce_value(value: str) -> Any:
    """Coerce a string value to appropriate type.

    Args:
        value: String value to coerce

    Returns:
        Coerced value (bool, int, float, or str)
    """
    # Boolean values
    if value.lower() in ("true", "yes", "on"):
        return True
    if value.lower() in ("false", "no", "off"):
        return False

    # Integer values
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        return int(value)

    # Float values
    try:
        float_val = float(value)
        if "." in value or "e" in value.lower():
            return float_val
    except ValueError:
        pass

    # Default to string
    return value


def extract_path_components(path: str) -> list[str]:
    """Extract clean components from API path.

    Args:
        path: API path (e.g., "/nodes/pve1/qemu/100")

    Returns:
        List of path components (["nodes", "pve1", "qemu", "100"])
    """
    return [part for part in path.split("/") if part]


def build_help_text(command_name: str, description: str, examples: list[str] | None = None) -> str:
    """Build formatted help text for a command.

    Args:
        command_name: Name of the command
        description: Command description
        examples: Optional list of example commands

    Returns:
        Formatted help text
    """
    text = f"{command_name}\n{description}"

    if examples:
        text += "\n\nExamples:"
        for example in examples:
            text += f"\n  $ proxmox {example}"

    return text
