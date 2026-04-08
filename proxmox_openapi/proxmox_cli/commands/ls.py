"""LS command implementation."""

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
