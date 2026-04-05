"""Configuration profile management commands."""

from __future__ import annotations

from typing import Optional

import typer

from proxmox_openapi.proxmox_cli.app import app
from proxmox_openapi.proxmox_cli.config import BackendConfig, ConfigManager
from proxmox_openapi.proxmox_cli.output import (
    OutputFormatter,
    get_context_options,
    resolve_output_format,
)


def _build_formatter(
    output: str | None,
    *,
    json_output: bool,
    yaml_output: bool,
    markdown_output: bool,
) -> OutputFormatter:
    """Build formatter from command options and inherited global CLI output settings."""
    ctx_obj = get_context_options()
    output_fmt = resolve_output_format(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
        fallback=ctx_obj.get("output_format", "human"),
    )
    return OutputFormatter(format=output_fmt, colors=True)


@app.command()
def config_list(
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
    """List all available configuration profiles.

    Example:
        proxmox config-list
    """
    mgr = ConfigManager()
    profiles = mgr.list_profiles()
    formatter = _build_formatter(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )

    if not profiles:
        formatter.print_output({"profiles": []})
        return

    payload = [
        {
            "name": profile.name,
            "backend": profile.backend or "https",
            "host": profile.host or "localhost",
            "user": profile.user or "unknown",
            "service": profile.service,
        }
        for profile in profiles
    ]
    formatter.print_output(payload)


@app.command()
def config_show(
    profile: str = typer.Argument("default", help="Profile name"),
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
    """Show configuration for a specific profile.

    Example:
        proxmox config-show default
        proxmox config-show staging
    """
    mgr = ConfigManager()
    formatter = _build_formatter(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )
    config = mgr.get_profile(profile)

    if not config:
        typer.echo(f"Profile not found: {profile}", err=True)
        raise typer.Exit(code=1)

    payload = {
        "profile": profile,
        "backend": config.backend or "https",
        "host": config.host or "localhost",
        "port": config.port or 8006,
        "user": config.user or "(not set)",
        "token_name": config.token_name or "(not set)",
        "service": config.service or "PVE",
        "verify_ssl": config.verify_ssl if hasattr(config, "verify_ssl") else True,
        "timeout_seconds": config.timeout if hasattr(config, "timeout") else 60,
    }
    formatter.print_output(payload)


@app.command()
def config_add(
    name: str = typer.Argument(..., help="Profile name"),
    backend: str = typer.Option("https", help="Backend type"),
    host: str = typer.Option(..., prompt=True, help="Host address"),
    port: int = typer.Option(8006, help="Port number"),
    user: Optional[str] = typer.Option(None, help="Username"),
    token_name: Optional[str] = typer.Option(None, help="Token name"),
    token_value: Optional[str] = typer.Option(None, help="Token value"),
    service: str = typer.Option("PVE", help="Service type (PVE/PMG/PBS)"),
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
    """Add a new configuration profile.

    Example:
        proxmox config-add staging --host proxmox-staging.example.com --user admin@pam
        proxmox config-add prod --backend https --host proxmox.example.com --token-name api-token
    """
    mgr = ConfigManager()

    config = BackendConfig(
        name=name,
        backend=backend,
        host=host,
        port=port,
        user=user,
        token_name=token_name,
        token_value=token_value,
        service=service,
    )

    mgr.add_profile(name, config)
    mgr.save_config()

    formatter = _build_formatter(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )
    payload = {
        "status": "success",
        "action": "config-add",
        "profile": name,
        "backend": backend,
        "host": host,
        "port": port,
        "user": user,
    }
    formatter.print_output(payload)


@app.command()
def config_remove(
    name: str = typer.Argument(..., help="Profile name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
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
    """Remove a configuration profile.

    Example:
        proxmox config-remove staging
        proxmox config-remove staging --force
    """
    if not force:
        if not typer.confirm(f"Remove profile '{name}'?"):
            typer.echo("Cancelled")
            return

    mgr = ConfigManager()
    mgr.remove_profile(name)
    mgr.save_config()

    formatter = _build_formatter(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )
    formatter.print_output({"status": "success", "action": "config-remove", "profile": name})


@app.command()
def config_set_default(
    name: str = typer.Argument(..., help="Profile name to set as default"),
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
    """Set the default profile.

    Example:
        proxmox config-set-default staging
    """
    mgr = ConfigManager()
    mgr.set_default_profile(name)
    mgr.save_config()

    formatter = _build_formatter(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )
    formatter.print_output({"status": "success", "action": "config-set-default", "profile": name})
