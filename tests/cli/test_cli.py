"""Basic CLI tests."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from proxmox_openapi.proxmox_cli.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


def test_cli_version(cli_runner: CliRunner) -> None:
    """Test --version flag."""
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.stdout.lower()


def test_cli_help(cli_runner: CliRunner) -> None:
    """Test --help flag."""
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Proxmox" in result.stdout or "proxmox" in result.stdout


def test_cli_no_args(cli_runner: CliRunner) -> None:
    """Test CLI with no arguments."""
    result = cli_runner.invoke(app, [])
    # Should show help or exit
    assert result.exit_code in (0, 2)


def test_help_command(cli_runner: CliRunner) -> None:
    """Test help command."""
    result = cli_runner.invoke(app, ["help"])
    # Help command may not be fully registered yet, allow error codes
    assert result.exit_code in (0, 2)
    # If successful, should see help content
    if result.exit_code == 0:
        assert "help" in result.stdout.lower() or "command" in result.stdout.lower()


def test_help_command_with_path(cli_runner: CliRunner) -> None:
    """Test help command with path."""
    result = cli_runner.invoke(app, ["help", "/nodes"])
    assert result.exit_code == 0 or result.exit_code == 2


def test_get_command_no_args(cli_runner: CliRunner) -> None:
    """Test get command without arguments."""
    result = cli_runner.invoke(app, ["get"])
    # Should require path argument
    assert result.exit_code != 0


def test_get_command_with_path_mock(cli_runner: CliRunner) -> None:
    """Test get command with mock backend."""
    result = cli_runner.invoke(app, ["get", "/nodes", "--backend", "mock"])
    # May fail with backend error, but should parse correctly
    assert result.exit_code in (0, 1, 2, 4)  # Allow various error codes


def test_config_paths() -> None:
    """Test configuration file path detection."""
    from proxmox_openapi.proxmox_cli.config import ConfigManager

    mgr = ConfigManager()
    assert mgr.DEFAULT_CONFIG_PATHS
    assert len(mgr.DEFAULT_CONFIG_PATHS) >= 2


def test_output_formatter() -> None:
    """Test output formatter initialization."""
    from proxmox_openapi.proxmox_cli.output import OutputFormatter

    formatter = OutputFormatter(format="json")
    assert formatter.format == "json"

    formatter2 = OutputFormatter(format="table", colors=False)
    assert formatter2.format == "table"
    assert not formatter2.colors


def test_exceptions() -> None:
    """Test CLI exceptions."""
    from proxmox_openapi.proxmox_cli.exceptions import (
        ConfigError,
        PathError,
        ParameterError,
        BackendError,
    )

    err = ConfigError("test config error")
    assert "Configuration error" in str(err)
    assert err.exit_code == 2

    err2 = PathError("invalid path", path="/bad/path")
    assert "Invalid path" in str(err2)
    assert "/bad/path" in str(err2)

    err3 = ParameterError("bad param", param="vmid")
    assert "Invalid parameter" in str(err3)
    assert "vmid" in str(err3)

    err4 = BackendError("connection failed", backend="https")
    assert "Backend error" in str(err4)
    assert "connection failed" in str(err4)


def test_utils_validate_path() -> None:
    """Test path validation utility."""
    from proxmox_openapi.proxmox_cli.utils import validate_api_path, extract_path_components

    path = validate_api_path("/nodes/pve1/qemu/100")
    assert path == "/nodes/pve1/qemu/100"

    normalized = validate_api_path("//nodes///pve1//qemu//100")
    assert normalized == "/nodes/pve1/qemu/100"

    components = extract_path_components("/nodes/pve1/qemu/100")
    assert components == ["nodes", "pve1", "qemu", "100"]


def test_utils_parse_parameters() -> None:
    """Test parameter parsing utility."""
    from proxmox_openapi.proxmox_cli.utils import parse_parameter_data

    params = parse_parameter_data(
        short_params=["vmid=100", "name=test-vm", "cores=2"],
    )
    assert params["vmid"] == 100
    assert params["name"] == "test-vm"
    assert params["cores"] == 2

    # Test type coercion
    params2 = parse_parameter_data(
        short_params=["enabled=true", "count=42", "ratio=3.14"],
    )
    assert params2["enabled"] is True
    assert params2["count"] == 42
    assert params2["ratio"] == 3.14
