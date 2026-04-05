"""Main CLI entry point."""

from __future__ import annotations

import logging
from typing import Literal, Optional

import typer

# Import new CLI modules for registration
from . import batch, commands, completion, config_commands, doc_commands, performance  # noqa: F401
from .app import app, setup_logging
from .exceptions import ProxmoxCLIError
from .output import resolve_output_format

logger = logging.getLogger(__name__)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Show version and exit",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging",
    ),
    quiet: bool = typer.Option(False, "--quiet", "-q", help="Suppress non-essential output"),
    config: Optional[str] = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to configuration file",
    ),
    backend: Optional[str] = typer.Option(
        None,
        "--backend",
        "-b",
        help="Backend to use (https, ssh_paramiko, openssh, local, mock)",
    ),
    host: Optional[str] = typer.Option(
        None,
        "--host",
        "-H",
        help="Proxmox host address",
    ),
    user: Optional[str] = typer.Option(
        None,
        "--user",
        "-U",
        help="Username or token name",
    ),
    password: Optional[str] = typer.Option(
        None,
        "--password",
        "-P",
        help="Password (insecure, prefer token)",
    ),
    token_value: Optional[str] = typer.Option(
        None,
        "--token-value",
        help="API token value",
    ),
    port: Optional[int] = typer.Option(
        None,
        "--port",
        help="API port (default: 8006)",
    ),
    service: Literal["PVE", "PMG", "PBS"] = typer.Option(
        "PVE",
        "--service",
        "-S",
        help="Proxmox service type",
    ),
    output_format: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output format (human, json, yaml, markdown, table, text, raw)",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Shortcut for --output json",
    ),
    yaml_output: bool = typer.Option(
        False,
        "--yaml",
        help="Shortcut for --output yaml",
    ),
    markdown_output: bool = typer.Option(
        False,
        "--markdown",
        help="Shortcut for --output markdown",
    ),
) -> None:
    """Proxmox CLI - A pvesh-like command-line interface for Proxmox API."""
    setup_logging(verbose=verbose, quiet=quiet)

    # Show version if requested
    if version:
        from proxmox_openapi.proxmox_cli import __version__

        typer.echo(f"proxmox-cli version {__version__}")
        raise typer.Exit()

    # No subcommand provided - show help
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()

    # Store global options in context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["quiet"] = quiet
    ctx.obj["config"] = config
    ctx.obj["backend"] = backend
    ctx.obj["host"] = host
    ctx.obj["user"] = user
    ctx.obj["password"] = password
    if password:
        logger.warning(
            "Password provided via --password flag is visible in process history. "
            "Consider using PROXMOX_CLI_PASSWORD environment variable instead for better security."
        )
    ctx.obj["token_value"] = token_value
    ctx.obj["port"] = port
    ctx.obj["service"] = service
    ctx.obj["output_format"] = resolve_output_format(
        output_format,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
        fallback="human",
    )


def cli_main() -> None:
    """Main entry point for CLI."""
    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\nInterrupted", err=True)
        raise typer.Exit(code=130)
    except Exception as e:
        if isinstance(e, ProxmoxCLIError):
            typer.echo(f"Error: {e.message}", err=True)
            raise typer.Exit(code=e.exit_code)
        raise


if __name__ == "__main__":
    cli_main()
