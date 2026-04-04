"""HELP command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app

logger = logging.getLogger(__name__)


@app.command()
def help_cmd(
    path: Optional[str] = typer.Argument(None, help="API path to get help for"),
    search: Optional[str] = typer.Option(
        None,
        "--search",
        "-s",
        help="Search for endpoints matching pattern",
    ),
) -> None:
    """Show help for API endpoints.

    Examples:
        proxmox help
        proxmox help /nodes
        proxmox help /nodes/pve1/qemu
        proxmox help --search qemu
    """
    if not path and not search:
        typer.echo("Proxmox CLI - Available commands:")
        typer.echo()
        typer.echo("  get <path>          - Retrieve resources")
        typer.echo("  create <path>       - Create resources")
        typer.echo("  set <path>          - Update configuration")
        typer.echo("  delete <path>       - Delete resources")
        typer.echo("  ls <path>           - List child resources")
        typer.echo("  usage <path>        - Show endpoint schema")
        typer.echo("  help [path]         - Show help for endpoints")
        typer.echo()
        typer.echo("For detailed help on any command, use: proxmox <command> --help")
        typer.echo("For endpoint-specific help: proxmox help /nodes/pve1")
    elif search:
        typer.echo(f"Endpoints matching '{search}':")
        typer.echo("  [Full search not yet implemented - use help /path for specific endpoints]")
    elif path:
        typer.echo(f"Help for endpoint: {path}")
        typer.echo()
        typer.echo("This endpoint is part of the Proxmox VE API.")
        typer.echo(f"For more information about {path}, consult the API documentation:")
        typer.echo("  https://pve.proxmox.com/pve-docs/api-viewer/")
