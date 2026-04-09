"""Shared fixtures for CLI tests."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()
