"""LS command implementation."""

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


def _apply_filter(result: list[dict], filter_expr: str) -> list[dict]:
    """Apply client-side filter to results.

    Filter format: "field=value" or "field~contains" for substring match
    """
    if not filter_expr or not result:
        return result

    try:
        if "~" in filter_expr:
            field, pattern = filter_expr.split("~", 1)
            return [
                r for r in result if field in r and pattern.lower() in str(r.get(field, "")).lower()
            ]
        elif "=" in filter_expr:
            field, value = filter_expr.split("=", 1)
            return [r for r in result if r.get(field) == value]
        else:
            return result
    except (ValueError, KeyError):
        return result


@app.command()
def ls(
    path: str = typer.Argument(..., help="API path to list"),
    columns: Optional[str] = typer.Option(
        None,
        "--columns",
        "-c",
        help="Comma-separated columns to display",
    ),
    sort: Optional[str] = typer.Option(
        None,
        "--sort",
        help="Field to sort by",
    ),
    reverse: bool = typer.Option(
        False,
        "--reverse",
        "-r",
        help="Sort in reverse order",
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
    """List child resources at a given API path.

    Fetches a collection from the API endpoint and displays the results
    with optional sorting, filtering, pagination, and format selection.
    
    Filtering syntax:
        - field=value      : Exact match
        - field~substring  : Case-insensitive substring match
    
    Examples:
        # List all nodes
        proxmox ls /nodes
        
        # List VMs on a node
        proxmox ls /nodes/pve1/qemu
        
        # List with specific columns
        proxmox ls /nodes/pve1/qemu --columns vmid,name,status
        
        # Sort and limit results
        proxmox ls /nodes/pve1/qemu --sort name --reverse --limit 10
        
        # Filter running VMs and display as table
        proxmox ls /nodes/pve1/qemu --filter status=running --output table
        
        # Pagination (skip first 20, get 10)
        proxmox ls /nodes/pve1/qemu --offset 20 --limit 10
        
        # Watch mode (refresh every 5 seconds)
        proxmox ls /nodes/pve1/qemu --watch 5
        
        # Get storage list as JSON
        proxmox ls /storage --json
    """
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
            result = bridge.list_children(path)

            # Filter if requested
            if filter:
                result = _apply_filter(result, filter)

            # Sort if requested
            if sort and isinstance(result, list) and result and isinstance(result[0], dict):
                result = sorted(result, key=lambda x: str(x.get(sort, "")), reverse=reverse)

            # Apply pagination
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
