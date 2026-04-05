"""Batch operations support for CLI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import typer

from proxmox_openapi.proxmox_cli.app import app
from proxmox_openapi.proxmox_cli.config import ConfigManager
from proxmox_openapi.proxmox_cli.exceptions import ParameterError
from proxmox_openapi.proxmox_cli.output import (
    OutputFormatter,
    get_context_options,
    resolve_output_format,
)
from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge


@app.command()
def batch(
    file: str = typer.Argument(..., help="JSON file with batch operations"),
    dry_run: bool = typer.Option(False, help="Show what would be executed"),
    continue_on_error: bool = typer.Option(False, help="Continue if operation fails"),
    backend: Optional[str] = typer.Option(None, help="Backend to use"),
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
    """Execute batch operations from a JSON file.

    Batch file format:
    ```json
    {
      "operations": [
        {"action": "get", "path": "/nodes"},
        {"action": "create", "path": "/nodes/pve1/qemu/100", "params": {"vmid": 100}},
        {"action": "set", "path": "/nodes/pve1/qemu/100", "params": {"cores": 4}}
      ]
    }
    ```

    Example:
        proxmox batch operations.json
        proxmox batch operations.json --dry-run
        proxmox batch operations.json --continue-on-error
    """
    try:
        batch_file = Path(file)
        if not batch_file.exists():
            typer.echo(f"Batch file not found: {file}", err=True)
            raise typer.Exit(code=1)

        with open(batch_file) as f:
            batch_data = json.load(f)

        operations = batch_data.get("operations", [])
        if not operations:
            typer.echo("No operations found in batch file", err=True)
            raise typer.Exit(code=1)

        # Initialize SDK bridge
        ctx_obj = get_context_options()
        output_fmt = resolve_output_format(
            output,
            json_output=json_output,
            yaml_output=yaml_output,
            markdown_output=markdown_output,
            fallback=ctx_obj.get("output_format", "human"),
        )
        formatter = OutputFormatter(format=output_fmt, colors=True)

        config_mgr = ConfigManager()
        config = config_mgr.get_profile("default")
        if backend:
            config.backend = backend

        bridge = ProxmoxSDKBridge.create(config)

        results: list[dict[str, Any]] = []

        for i, op in enumerate(operations, 1):
            action = op.get("action")
            path = op.get("path")
            params = op.get("params", {})

            if dry_run:
                results.append({"op": i, "action": action, "status": "dry-run"})
                continue

            try:
                if action == "get":
                    result = bridge.get(path)
                elif action == "create":
                    result = bridge.post(path, params)
                elif action == "set":
                    result = bridge.put(path, params)
                elif action == "delete":
                    result = bridge.delete(path)
                else:
                    raise ParameterError(f"Unknown action: {action}")
                results.append(
                    {
                        "op": i,
                        "action": action,
                        "path": path,
                        "status": "success",
                        "result": result,
                    }
                )
            except Exception as e:
                if not continue_on_error:
                    raise typer.Exit(code=1)
                results.append(
                    {
                        "op": i,
                        "action": action,
                        "path": path,
                        "status": "error",
                        "error": str(e),
                    }
                )

        # Summary
        success_count = sum(1 for r in results if r.get("status") == "success")
        error_count = sum(1 for r in results if r.get("status") == "error")
        dry_run_count = sum(1 for r in results if r.get("status") == "dry-run")

        payload = {
            "file": str(batch_file),
            "dry_run": dry_run,
            "continue_on_error": continue_on_error,
            "operations_total": len(operations),
            "summary": {
                "succeeded": success_count,
                "failed": error_count,
                "dry_run": dry_run_count,
            },
            "results": results,
        }
        formatter.print_output(payload)

    except Exception as e:
        typer.echo(f"Batch operation failed: {e}", err=True)
        raise typer.Exit(code=1)
