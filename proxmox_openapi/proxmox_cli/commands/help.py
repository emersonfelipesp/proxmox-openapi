"""HELP command implementation."""

from __future__ import annotations

import logging
from typing import Optional

import typer

from ..app import app
from ..output import OutputFormatter, get_context_options, resolve_output_format

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
    """Show help for API endpoints.

    Examples:
        proxmox help
        proxmox help /nodes
        proxmox help /nodes/pve1/qemu
        proxmox help --search qemu
    """
    ctx_obj = get_context_options()
    output_fmt = resolve_output_format(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
        fallback=ctx_obj.get("output_format", "human"),
    )
    formatter = OutputFormatter(format=output_fmt, colors=True)

    if not path and not search:
        payload = {
            "title": "Proxmox CLI - Available commands",
            "commands": [
                {"name": "get", "usage": "get <path>", "description": "Retrieve resources"},
                {"name": "create", "usage": "create <path>", "description": "Create resources"},
                {"name": "set", "usage": "set <path>", "description": "Update configuration"},
                {"name": "delete", "usage": "delete <path>", "description": "Delete resources"},
                {"name": "ls", "usage": "ls <path>", "description": "List child resources"},
                {"name": "usage", "usage": "usage <path>", "description": "Show endpoint schema"},
                {"name": "help", "usage": "help [path]", "description": "Show help for endpoints"},
            ],
            "hints": [
                "For detailed help on any command, use: proxmox <command> --help",
                "For endpoint-specific help: proxmox help /nodes/pve1",
            ],
        }
        formatter.print_output(payload)
    elif search:
        payload = {
            "search": search,
            "note": "Full search not yet implemented; use 'help /path' for specific endpoints.",
            "matches": [],
        }
        formatter.print_output(payload)
    elif path:
        payload = {
            "endpoint": path,
            "description": "This endpoint is part of the Proxmox VE API.",
            "documentation": "https://pve.proxmox.com/pve-docs/api-viewer/",
        }
        formatter.print_output(payload)
