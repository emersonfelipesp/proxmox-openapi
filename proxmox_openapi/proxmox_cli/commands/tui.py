"""TUI command for proxmox CLI."""

from __future__ import annotations

from typing import Any, Literal

import typer

from proxmox_openapi.proxmox_cli.app import app
from proxmox_openapi.proxmox_cli.config import BackendConfig, ConfigManager
from proxmox_openapi.proxmox_cli.exceptions import ProxmoxCLIError
from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_openapi.proxmox_cli.tui_runner import launch_tui
from proxmox_openapi.proxmox_cli.utils import validate_api_path

from ._common import apply_cli_overrides


def _build_backend_config(ctx_obj: dict[str, Any], *, use_mock: bool) -> BackendConfig:
    """Build a backend config from profile and CLI global flags."""
    config_mgr = ConfigManager()
    config_mgr.load_config(ctx_obj.get("config"))
    backend_cfg = config_mgr.get_profile()
    apply_cli_overrides(backend_cfg, ctx_obj)

    if use_mock:
        backend_cfg.backend = "mock"
    elif backend_cfg.backend == "mock":
        # pbx/proxmox tui must target production by default.
        backend_cfg.backend = "https"

    return backend_cfg


@app.command("tui")
def tui(
    ctx: typer.Context,
    mode: Literal["mock"] | None = typer.Argument(
        None,
        help="Optional mode. Use 'mock' to run TUI against in-memory mock backend.",
    ),
    path: str = typer.Option(
        "/nodes",
        "--path",
        "-p",
        help="Initial API path to load in the TUI.",
    ),
) -> None:
    """Launch interactive Proxmox TUI for resource navigation and management.

    Opens a full-screen terminal UI for browsing Proxmox API resources
    hierarchically and performing operations. Supports both real backends
    (HTTPS, SSH, local) and mock mode for testing/learning.

    MODE:
        - Omit or use 'mock' to connect to in-memory mock backend
        - Otherwise connects using configured backend credentials

    Key controls:
        - Arrow keys: Navigate resources
        - Enter: Drill into path or edit
        - q: Quit
        - j/k: Jump between entries
        - s: Search
        - /: Filter

    Examples:
        # Launch with configured Proxmox backend
        proxmox tui

        # Launch against mock backend (no credentials needed)
        proxmox tui mock

        # Start at specific path
        proxmox tui -p /nodes/pve1/qemu

        # For PMG/PBS:
        pbx tui          # Proxmox Mail Gateway
        pbs tui          # Proxmox Backup Server
    """
    bridge: ProxmoxSDKBridge | None = None

    try:
        ctx_obj = ctx.obj or {}
        initial_path = validate_api_path(path)
        use_mock = mode == "mock"

        backend_cfg = _build_backend_config(ctx_obj, use_mock=use_mock)
        bridge = ProxmoxSDKBridge.create(backend_cfg)

        launch_tui(
            bridge=bridge,
            mode="mock" if use_mock else "production",
            initial_path=initial_path,
        )
    except RuntimeError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=2)
    except ProxmoxCLIError as exc:
        typer.echo(f"Error: {exc.message}", err=True)
        raise typer.Exit(code=exc.exit_code)
    except Exception as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1)
    finally:
        if bridge is not None:
            bridge.close()
