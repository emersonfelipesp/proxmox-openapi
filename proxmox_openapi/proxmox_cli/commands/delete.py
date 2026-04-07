"""DELETE command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app
from ..exceptions import ProxmoxCLIError
from ..output import get_context_options
from ..utils import validate_api_path
from ._common import create_formatter, prepare_command

logger = logging.getLogger(__name__)


@app.command()
def delete(
    path: str = typer.Argument(..., help="API path to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Force deletion without confirmation"),
    output: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output format (human, json, yaml, markdown, table, text, raw)",
    ),
    json_output: bool = typer.Option(False, "--json", help="Shortcut for --output json"),
    yaml_output: bool = typer.Option(False, "--yaml", help="Shortcut for --output yaml"),
    markdown_output: bool = typer.Option(
        False,
        "--markdown",
        help="Shortcut for --output markdown",
    ),
) -> None:
    """Delete resources from the Proxmox API.

    Sends a DELETE request to remove a resource. By default, prompts for
    confirmation unless --force is used.

    Examples:
        # Delete with confirmation prompt
        proxmox delete /nodes/pve/qemu/100

        # Delete without confirmation (useful in scripts/automation)
        proxmox delete /nodes/pve/qemu/100 --force

        # Delete with JSON output
        proxmox delete /nodes/pve/qemu/100 --force --json

        # Delete storage resource
        proxmox delete /storage/backup-nfs --force

        # Silently delete in automation (exit code indicates success)
        proxmox delete /nodes/pve/qemu/100 --force 2>/dev/null
    """
    try:
        # Confirm deletion unless forced
        if not force:
            confirm = typer.confirm(f"Delete {path}?")
            if not confirm:
                typer.echo("Cancelled")
                raise typer.Exit()

        # Get context
        ctx_obj = get_context_options()

        # Validate path
        path = validate_api_path(path)

        # Load config, apply overrides, create bridge
        config_mgr, bridge = prepare_command(ctx_obj)
        result = bridge.delete(path)

        formatter = create_formatter(
            config_mgr,
            output,
            json_output=json_output,
            yaml_output=yaml_output,
            markdown_output=markdown_output,
            ctx_obj=ctx_obj,
        )

        payload = {
            "status": "success",
            "action": "delete",
            "path": path,
            "data": result,
        }
        formatter.print_output(payload)
        bridge.close()

    except ProxmoxCLIError as e:
        typer.echo(f"Error: {e.message}", err=True)
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
