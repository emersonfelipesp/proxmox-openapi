"""Docs command group for generating CLI capture documentation."""

from __future__ import annotations

from pathlib import Path

import typer

from .app import app

docs_app = typer.Typer(
    no_args_is_help=True,
    help="Generate CLI documentation artifacts for MkDocs.",
)


@docs_app.command("generate-capture")
def docs_generate_capture(
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Markdown output path (default: <repo>/docs/generated/proxmox-command-capture.md).",
    ),
    raw_dir: Path | None = typer.Option(
        None,
        "--raw-dir",
        help="JSON artifact directory (default: <repo>/docs/generated/raw).",
    ),
    max_lines: int = typer.Option(
        200,
        "--max-lines",
        help="Max lines per output block in the generated Markdown.",
    ),
    max_chars: int = typer.Option(
        120_000,
        "--max-chars",
        help="Max characters per output block in the generated Markdown.",
    ),
) -> None:
    """Capture proxmox CLI command input/output recursively from the command tree."""
    try:
        from .docgen_capture import generate_command_capture_docs, resolve_capture_paths

        out, raw = resolve_capture_paths(output, raw_dir)
    except FileNotFoundError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    code = generate_command_capture_docs(
        output=out,
        raw_dir=raw,
        max_lines=max_lines,
        max_chars=max_chars,
    )
    raise typer.Exit(code=code)


app.add_typer(docs_app, name="docs")
