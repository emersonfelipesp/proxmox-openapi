"""Configuration profile management commands."""

from __future__ import annotations

from typing import Optional

import typer

from proxmox_openapi.proxmox_cli.app import app
from proxmox_openapi.proxmox_cli.config import BackendConfig, ConfigManager


@app.command()
def config_list() -> None:
    """List all available configuration profiles.

    Example:
        proxmox config-list
    """
    mgr = ConfigManager()
    profiles = mgr.list_profiles()

    if not profiles:
        typer.echo("No profiles configured")
        return

    typer.echo("Available profiles:")
    for profile in profiles:
        backend_type = profile.backend or "https"
        host = profile.host or "localhost"
        user = profile.user or "unknown"
        typer.echo(f"  {profile.name:<15} {backend_type:<12} {user}@{host}")


@app.command()
def config_show(profile: str = typer.Argument("default", help="Profile name")) -> None:
    """Show configuration for a specific profile.

    Example:
        proxmox config-show default
        proxmox config-show staging
    """
    mgr = ConfigManager()
    config = mgr.get_profile(profile)

    if not config:
        typer.echo(f"Profile not found: {profile}", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Profile: {profile}")
    typer.echo(f"  Backend: {config.backend or 'https'}")
    typer.echo(f"  Host: {config.host or 'localhost'}")
    typer.echo(f"  Port: {config.port or 8006}")
    typer.echo(f"  User: {config.user or '(not set)'}")
    typer.echo(f"  Token Name: {config.token_name or '(not set)'}")
    typer.echo(f"  Service: {config.service or 'PVE'}")
    typer.echo(f"  Verify SSL: {config.verify_ssl if hasattr(config, 'verify_ssl') else True}")
    typer.echo(f"  Timeout: {config.timeout if hasattr(config, 'timeout') else 60}s")


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

    typer.echo(f"✓ Profile '{name}' added successfully")
    typer.echo(f"  Backend: {backend}")
    typer.echo(f"  Host: {host}:{port}")
    if user:
        typer.echo(f"  User: {user}")


@app.command()
def config_remove(
    name: str = typer.Argument(..., help="Profile name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
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

    typer.echo(f"✓ Profile '{name}' removed")


@app.command()
def config_set_default(
    name: str = typer.Argument(..., help="Profile name to set as default"),
) -> None:
    """Set the default profile.

    Example:
        proxmox config-set-default staging
    """
    mgr = ConfigManager()
    mgr.set_default_profile(name)
    mgr.save_config()

    typer.echo(f"✓ Default profile set to '{name}'")
