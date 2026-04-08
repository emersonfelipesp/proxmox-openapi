"""SET command implementation."""

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
def set_cmd(
    path: str = typer.Argument(..., help="API path to update"),
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
    """Update (PUT/PATCH) resources in the Proxmox API.

    Sends a PUT request to modify an existing resource. Parameters can be
    passed via -d/--data flags or a JSON file. Some fields can be unset
    using empty values or delete prefixes.

    Examples:
        # Update node description
        proxmox set /nodes/pve1 -d description="Production Node 1"

        # Update with multiple parameters
        proxmox set /nodes/pve1 -d features=snapshot,nesting -d cpu=host

        # Update from JSON file
        proxmox set /nodes/pve1 -f node-update.json

        # Update VM configuration
        proxmox set /nodes/pve/qemu/100 -d memory=8192 -d cores=4

        # Update user profile
        proxmox set /access/users/user@pam -d firstname="John" -d lastname="Doe"
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

        if not params:
            typer.echo("Error: No parameters provided", err=True)
            raise typer.Exit(code=1)

        # Load config, apply overrides, create bridge
        config_mgr, bridge = prepare_command(ctx_obj)
        result = bridge.put(path, params)

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
            "action": "set",
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
