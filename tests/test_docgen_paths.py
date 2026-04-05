"""Tests for docgen output path resolution."""

from __future__ import annotations

from pathlib import Path

from proxmox_openapi.proxmox_cli import docgen_capture


def test_default_paths_under_docs() -> None:
    output, raw = docgen_capture.resolve_capture_paths(None, None)
    assert output.name == "proxmox-command-capture.md"
    assert raw.name == "raw"
    assert raw.parent == output.parent


def test_custom_output_infers_raw_sibling() -> None:
    custom_output = Path("/tmp/proxmox-docs/capture.md")
    output, raw = docgen_capture.resolve_capture_paths(custom_output, None)
    assert output == custom_output
    assert raw == Path("/tmp/proxmox-docs/raw")
