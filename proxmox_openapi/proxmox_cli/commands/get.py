"""GET command implementation."""

from __future__ import annotations

import logging
import time
from typing import Optional

import typer

from ..app import app
from ..config import ConfigManager
from ..exceptions import ProxmoxCLIError
from ..output import OutputFormatter, get_context_options, resolve_output_format
from ..sdk_bridge import ProxmoxSDKBridge
from ..utils import validate_api_path

logger = logging.getLogger(__name__)


@app.command()
def get(
    path: str = typer.Argument(..., help="API path to retrieve"),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        "-c",
        help="Comma-separated columns to display",
    ),
    limit: Optional[int] = typer.Option(
        None,
        "--limit",
        "-l",
        help="Maximum number of results to return",
    ),
    offset: Optional[int] = typer.Option(
        None,
        "--offset",
        help="Number of results to skip (for pagination)",
    ),
    filter: Optional[str] = typer.Option(
        None,
        "--filter",
        "-f",
        help="Filter results (field=value or field~substring)",
    ),
    watch: Optional[int] = typer.Option(
        None,
        "--watch",
        "-w",
        help="Refresh every N seconds (Ctrl+C to stop)",
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
    """Retrieve resources from the Proxmox API.

    Examples:
        proxmox get /nodes
        proxmox get /nodes/pve1/status
        proxmox get /nodes/pve1/qemu --output json
        proxmox get /nodes/pve1/qemu --filter status=running --limit 10
        proxmox get /nodes --watch 5
    """
    from .ls import _apply_filter

    try:
        # Get context
        ctx_obj = get_context_options()

        # Validate path
        path = validate_api_path(path)

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

        # Determine output format
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

        cols = columns.split(",") if columns else None

        def execute_and_print():
            result = bridge.get(path)

            # Filter if requested (only works for list results)
            if filter and isinstance(result, list):
                result = _apply_filter(result, filter)

            # Apply pagination (only works for list results)
            if isinstance(result, list):
                if offset:
                    result = result[offset:]
                if limit:
                    result = result[:limit]

            formatter.print_output(result, columns=cols)

        # Watch mode - loop until Ctrl+C
        if watch:
            try:
                while True:
                    execute_and_print()
                    typer.echo(f"\n--- Refreshed every {watch}s (Ctrl+C to stop) ---", err=True)
                    time.sleep(watch)
            except KeyboardInterrupt:
                typer.echo("\nWatch mode stopped.", err=True)
        else:
            execute_and_print()

        bridge.close()

    except ProxmoxCLIError as e:
        typer.echo(f"Error: {e.message}", err=True)
        raise typer.Exit(code=e.exit_code)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1)
