"""CREATE command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app
from ..config import ConfigManager
from ..exceptions import ProxmoxCLIError
from ..output import OutputFormatter
from ..sdk_bridge import ProxmoxSDKBridge
from ..utils import parse_parameter_data, validate_api_path

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
        help="Output format (json, yaml, table, text, auto)",
    ),
) -> None:
    """Create resources in the Proxmox API.

    Examples:
        proxmox create /nodes/pve1/qemu/100 --vmid 100 --name test-vm
        proxmox create /nodes/pve1/qemu/100 -d vmid=100 -d name=test-vm
        proxmox create /nodes/pve1/qemu/100 -f params.json
    """
    try:
        # Get context
        ctx = typer.get_app_context()
        ctx_obj = ctx.obj or {}

        # Validate path
        path = validate_api_path(path)

        # Parse parameters
        params = parse_parameter_data(
            short_params=data,
            json_file=json_file,
        )

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
        result = bridge.post(path, params)

        # Format and output
        output_fmt = output or ctx_obj.get("output_format", "auto")
        formatter = OutputFormatter(
            format=output_fmt,
            colors=config_mgr.global_config.colors,
        )

        formatter.print_success(f"Created {path}")
        if result:
            formatter.print_output(result)
        bridge.close()

    except ProxmoxCLIError as e:
        typer.echo(f"Error: {e.message}", err=True)
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)

