"""Tests for Typer command tree discovery used by docgen."""

from __future__ import annotations

from proxmox_openapi.proxmox_cli.docgen.discovery import iter_discovered_help_specs


def test_discovery_returns_help_specs() -> None:
    specs = iter_discovered_help_specs()
    assert len(specs) >= 15
    for spec in specs:
        assert spec.argv
        assert spec.argv[-1] == "--help"


def test_root_help_present_once() -> None:
    specs = iter_discovered_help_specs()
    roots = [spec for spec in specs if spec.argv == ["--help"]]
    assert len(roots) == 1


def test_docs_group_is_discoverable() -> None:
    specs = iter_discovered_help_specs()
    argv_rows = {tuple(spec.argv) for spec in specs}
    assert ("docs", "--help") in argv_rows
    assert ("docs", "generate-capture", "--help") in argv_rows
