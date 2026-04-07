"""SET command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app
from ..config import ConfigManager
from ..exceptions import ProxmoxCLIError
from ..output import OutputFormatter, get_context_options, resolve_output_format
from ..sdk_bridge import ProxmoxSDKBridge
from ..utils import parse_parameter_data, validate_api_path

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

        # Load configuration
        config_mgr = ConfigManager()
        config_mgr.load_config(ctx_obj.get("config"))
        backend_cfg = config_mgr.get_profile()

        # Override with CLI options
        if ctx_obj.get("backend"):
            backend_cfg.backend = ctx_obj["backend"]
        if ctx_obj.get("host"):
            backend_cfg.host = ctx_obj["host"]
        if ctx_obj.get("user"):
            backend_cfg.user = ctx_obj["user"]
        if ctx_obj.get("password"):
            backend_cfg.password = ctx_obj["password"]
        if ctx_obj.get("token_value"):
            backend_cfg.token_value = ctx_obj["token_value"]
        if ctx_obj.get("port"):
            backend_cfg.port = ctx_obj["port"]
        if ctx_obj.get("service"):
            backend_cfg.service = ctx_obj["service"]

        # Create SDK bridge and execute
        bridge = ProxmoxSDKBridge.create(backend_cfg)
        result = bridge.put(path, params)

        # Format and output
        output_fmt = resolve_output_format(
            output,
            json_output=json_output,
            yaml_output=yaml_output,
            markdown_output=markdown_output,
            fallback=ctx_obj.get("output_format", "human"),
        )
        formatter = OutputFormatter(
            format=output_fmt,
            colors=config_mgr.global_config.colors,
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
