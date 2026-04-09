"""Test that all modules can be imported successfully."""

import importlib

import pytest


@pytest.mark.parametrize(
    "module_path",
    [
        "proxmox_openapi.main",
        "proxmox_openapi.mock_main",
        "proxmox_openapi.schema",
        "proxmox_openapi.exception",
        "proxmox_openapi.logger",
        # proxmox/
        "proxmox_openapi.proxmox.client",
        # sdk/auth/
        "proxmox_openapi.sdk.auth.base",
        # sdk/backends/
        "proxmox_openapi.sdk.backends._cli_base",
        # proxmox_cli/
        "proxmox_openapi.proxmox_cli.app",
        "proxmox_openapi.proxmox_cli.batch",
        "proxmox_openapi.proxmox_cli.cache",
        "proxmox_openapi.proxmox_cli.completion",
        "proxmox_openapi.proxmox_cli.config_commands",
        "proxmox_openapi.proxmox_cli.doc_commands",
        "proxmox_openapi.proxmox_cli.docgen_capture",
        "proxmox_openapi.proxmox_cli.exceptions",
        "proxmox_openapi.proxmox_cli.install",
        "proxmox_openapi.proxmox_cli.output",
        "proxmox_openapi.proxmox_cli.performance",
        "proxmox_openapi.proxmox_cli.release",
        "proxmox_openapi.proxmox_cli.sdk_bridge",
        "proxmox_openapi.proxmox_cli.tui_runner",
        "proxmox_openapi.proxmox_cli.utils",
        # proxmox_cli/commands/
        "proxmox_openapi.proxmox_cli.commands._common",
        "proxmox_openapi.proxmox_cli.commands.create",
        "proxmox_openapi.proxmox_cli.commands.delete",
        "proxmox_openapi.proxmox_cli.commands.get",
        "proxmox_openapi.proxmox_cli.commands.help",
        "proxmox_openapi.proxmox_cli.commands.ls",
        "proxmox_openapi.proxmox_cli.commands.set",
        "proxmox_openapi.proxmox_cli.commands.tui",
        "proxmox_openapi.proxmox_cli.commands.usage",
        # proxmox_cli/docgen/
        "proxmox_openapi.proxmox_cli.docgen.discovery",
        "proxmox_openapi.proxmox_cli.docgen.engine",
        "proxmox_openapi.proxmox_cli.docgen.models",
        "proxmox_openapi.proxmox_cli.docgen.specs",
    ],
)
def test_import(module_path: str) -> None:
    mod = importlib.import_module(module_path)
    assert mod is not None
