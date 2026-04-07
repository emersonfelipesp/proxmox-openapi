"""CREATE command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app
from ..exceptions import ProxmoxCLIError
from ..output import get_context_options
from ..utils import parse_parameter_data, validate_api_path
from ._common import create_formatter, prepare_command

logger = logging.getLogger(__name__)


@app.command()
def create(
    path: str = typer.Argument(..., help="API path where to create"),
    data: Optional[list[str]] = typer.Option(
        None,
        "-d",
        "--data",
        help="Data parameter (key=value, can be repeated)",
    ),
    json_file: Optional[str] = typer.Option(
        None,
        "-f",
        "--json-file",
        help="JSON file with parameters",
    ),
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
    """Create new resources in the Proxmox API.

    Sends a POST request to create a resource. Parameters can be passed via:
    - -d/--data flags: repeatable key=value pairs
    - -f/--json-file: JSON file with bulk parameters

    Examples:
        # Create VM via individual parameters
        proxmox create /nodes/pve/qemu -d vmid=100 -d name=web-vm

        # Create VM from JSON file
        proxmox create /nodes/pve/qemu -f vm.json

        # Create with JSON output
        proxmox create /nodes/pve/qemu -d vmid=100 -d name=web-vm --json

        # Create storage with multiple parameters
        proxmox create /nodes/pve/storage \\
            -d storage=nfs-backup -d type=nfs \\
            -d server=10.0.0.5 -d path=/mnt/backup
    """
    try:
        # Get context
        ctx_obj = get_context_options()

        # Validate path
        path = validate_api_path(path)

        # Parse parameters
        params = parse_parameter_data(
            short_params=data,
            json_file=json_file,
        )

        # Load config, apply overrides, create bridge
        config_mgr, bridge = prepare_command(ctx_obj)
        result = bridge.post(path, params)

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
            "action": "create",
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
