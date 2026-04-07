"""Shared helpers for CLI command implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from proxmox_openapi.proxmox_cli.config import BackendConfig

from proxmox_openapi.proxmox_cli.config import ConfigManager
from proxmox_openapi.proxmox_cli.output import (
    OutputFormatter,
    get_context_options,
    resolve_output_format,
)
from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge

# Fields that can be overridden from the CLI context object.
_OVERRIDE_KEYS = ("backend", "host", "user", "password", "token_value", "port", "service")


def apply_cli_overrides(backend_cfg: BackendConfig, ctx_obj: dict[str, Any]) -> None:
    """Apply CLI global-flag overrides to *backend_cfg* in-place."""
    for key in _OVERRIDE_KEYS:
        if ctx_obj.get(key):
            setattr(backend_cfg, key, ctx_obj[key])


def prepare_command(
    ctx_obj: dict[str, Any] | None = None,
) -> tuple[ConfigManager, ProxmoxSDKBridge]:
    """Load config, apply CLI overrides, and create an SDK bridge.

    Returns:
        A ``(config_mgr, bridge)`` tuple.  The caller is responsible for
        calling ``bridge.close()`` when done.
    """
    if ctx_obj is None:
        ctx_obj = get_context_options()
    config_mgr = ConfigManager()
    config_mgr.load_config(ctx_obj.get("config"))
    backend_cfg = config_mgr.get_profile()
    apply_cli_overrides(backend_cfg, ctx_obj)
    bridge = ProxmoxSDKBridge.create(backend_cfg)
    return config_mgr, bridge


def create_formatter(
    config_mgr: ConfigManager,
    output: str | None,
    *,
    json_output: bool = False,
    yaml_output: bool = False,
    markdown_output: bool = False,
    ctx_obj: dict[str, Any] | None = None,
) -> OutputFormatter:
    """Build an :class:`OutputFormatter` from CLI context and format flags."""
    if ctx_obj is None:
        ctx_obj = get_context_options()
    fmt = resolve_output_format(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
        fallback=ctx_obj.get("output_format", "human"),
    )
    return OutputFormatter(format=fmt, colors=config_mgr.global_config.colors)
