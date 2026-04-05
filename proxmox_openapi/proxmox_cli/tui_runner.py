"""Runtime launcher for Textual TUI."""

from __future__ import annotations

from typing import Literal

from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge

TuiMode = Literal["production", "mock"]


def launch_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_path: str = "/nodes",
) -> None:
    """Launch the Textual TUI and surface dependency errors with clear guidance."""
    try:
        from proxmox_openapi.proxmox_cli.tui_app import run_proxmox_tui
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "Textual dependency is missing. Install CLI extras: pip install proxmox-openapi[cli]"
            ) from exc
        raise

    run_proxmox_tui(bridge=bridge, mode=mode, initial_path=initial_path)
