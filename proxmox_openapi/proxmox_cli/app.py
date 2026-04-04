"""CLI application setup and command registration."""

from __future__ import annotations

import logging

import typer

logger = logging.getLogger(__name__)

# Create Typer app
app = typer.Typer(
    name="proxmox",
    help="Proxmox VE, PMG, and PBS CLI - A pvesh-like interface for Proxmox API",
    no_args_is_help=True,
    add_completion=True,
)


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure logging for the CLI.

    Args:
        verbose: Enable verbose logging
        quiet: Suppress non-essential output
    """
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


__all__ = ["app", "setup_logging"]
