"""USAGE command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app

logger = logging.getLogger(__name__)


@app.command()
def usage(
    path: str = typer.Argument(..., help="API path to get usage for"),
    command: Optional[str] = typer.Option(
        None,
        "--command",
        help="HTTP method to inspect (GET, POST, PUT, DELETE)",
    ),
    returns: bool = typer.Option(
        False,
        "--returns",
        help="Include return schema",
    ),
    verbose: bool = typer.Option(
        False,
        "-v",
        "--verbose",
        help="Verbose output",
    ),
) -> None:
    """Show API schema and usage information for an endpoint.

    Examples:
        proxmox usage /nodes/pve1/qemu/100
        proxmox usage /nodes/pve1/qemu/100 --command GET
        proxmox usage /nodes/pve1/qemu/100 --command POST --returns
    """
    typer.echo(f"API Schema for {path}")
    typer.echo(f"Method: {command or 'GET'}")
    if returns:
        typer.echo("Returns: [included in verbose output]")
    if verbose:
        typer.echo("\nDetailed schema information would be displayed here")
