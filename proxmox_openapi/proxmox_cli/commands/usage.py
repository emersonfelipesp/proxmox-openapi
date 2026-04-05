"""USAGE command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app
from ..output import OutputFormatter, resolve_output_format

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
    """Show API schema and usage information for an endpoint.

    Examples:
        proxmox usage /nodes/pve1/qemu/100
        proxmox usage /nodes/pve1/qemu/100 --command GET
        proxmox usage /nodes/pve1/qemu/100 --command POST --returns
    """
    ctx = typer.get_app_context()
    ctx_obj = ctx.obj or {}
    output_fmt = resolve_output_format(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
        fallback=ctx_obj.get("output_format", "human"),
    )
    formatter = OutputFormatter(format=output_fmt, colors=True)

    payload: dict[str, object] = {
        "path": path,
        "method": command or "GET",
        "returns_requested": returns,
        "verbose": verbose,
    }

    if returns:
        payload["returns"] = "Included in verbose output"
    if verbose:
        payload["details"] = "Detailed schema information would be displayed here"

    formatter.print_output(payload)
