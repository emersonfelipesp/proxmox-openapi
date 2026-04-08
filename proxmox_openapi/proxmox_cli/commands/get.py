"""GET command implementation."""

from __future__ import annotations

import logging
import time
from typing import Optional

import typer

from ..app import app
from ..exceptions import ProxmoxCLIError
from ..output import get_context_options
from ..utils import validate_api_path
from ._common import create_formatter, prepare_command

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

    Fetches data from API endpoints with optional filtering, pagination,
    watching/monitoring, and flexible output formatting.

    Examples:
        # List all nodes
        proxmox get /nodes

        # Get specific node info
        proxmox get /nodes/pve1/status

        # Get VMs on a node
        proxmox get /nodes/pve1/qemu --output json

        # Filter results
        proxmox get /nodes/pve1/qemu --filter status=running --limit 10

        # Watch resource for changes (refresh every 5 seconds)
        proxmox get /nodes/pve1/status --watch 5

        # Get storage list with YAML output
        proxmox get /storage --yaml

        # Select specific columns
        proxmox get /nodes/pve1/qemu --columns vmid,name,status --output table
    """
    from .ls import _apply_filter

    try:
        # Get context
        ctx_obj = get_context_options()

        # Validate path
        path = validate_api_path(path)

        # Load config, apply overrides, create bridge
        config_mgr, bridge = prepare_command(ctx_obj)
        formatter = create_formatter(
            config_mgr,
            output,
            json_output=json_output,
            yaml_output=yaml_output,
            markdown_output=markdown_output,
            ctx_obj=ctx_obj,
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
