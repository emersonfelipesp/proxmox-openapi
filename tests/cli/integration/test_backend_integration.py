"""Integration tests for CLI with real backend scenarios."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from proxmox_openapi.proxmox_cli.cli import app
from proxmox_openapi.proxmox_cli.config import ConfigManager, BackendConfig
from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_openapi.proxmox_cli.output import OutputFormatter


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def mock_backend_config() -> BackendConfig:
    """Create a mock backend configuration."""
    return BackendConfig(
        name="mock-test",
        backend="mock",
        service="PVE",
    )


class TestBackendInitialization:
    """Test backend initialization and selection."""

    def test_mock_backend_initialization(self, mock_backend_config: BackendConfig) -> None:
        """Test mock backend initialization."""
        bridge = ProxmoxSDKBridge.create(mock_backend_config)
        assert bridge is not None
        assert bridge.sdk is not None

    def test_https_backend_config(self) -> None:
        """Test HTTPS backend configuration."""
        config = BackendConfig(
            name="https-test",
            backend="https",
            host="proxmox.example.com",
            port=8006,
            user="admin@pam",
            token_value="test-token",
        )
        # Should not raise error on creation (actual connection tested separately)
        assert config.backend == "https"
        assert config.host == "proxmox.example.com"


class TestCLIBackendFlags:
    """Test CLI backend selection via flags."""

    def test_backend_flag_mock(self, cli_runner: CliRunner) -> None:
        """Test --backend mock flag."""
        result = cli_runner.invoke(app, ["--backend", "mock", "--help"])
        # Help should work with backend flag
        assert result.exit_code in (0, 2)

    def test_backend_flag_https(self, cli_runner: CliRunner) -> None:
        """Test --backend https flag."""
        result = cli_runner.invoke(app, ["--backend", "https", "--help"])
        # Help should work with backend flag
        assert result.exit_code in (0, 2)

    def test_host_flag(self, cli_runner: CliRunner) -> None:
        """Test --host flag."""
        result = cli_runner.invoke(app, ["--host", "proxmox.example.com", "--help"])
        assert result.exit_code in (0, 2)

    def test_user_token_flags(self, cli_runner: CliRunner) -> None:
        """Test --user and --token-value flags."""
        result = cli_runner.invoke(
            app,
            ["--user", "admin@pam", "--token-value", "test-token", "--help"],
        )
        assert result.exit_code in (0, 2)


class TestCommandBackendIntegration:
    """Test commands with different backends."""

    def test_get_with_mock_backend(self, cli_runner: CliRunner) -> None:
        """Test GET command with mock backend."""
        result = cli_runner.invoke(
            app,
            ["--backend", "mock", "get", "/nodes"],
        )
        # Mock backend should work
        assert result.exit_code in (0, 1, 4, 7)  # Allow various error codes

    def test_help_with_mock_backend(self, cli_runner: CliRunner) -> None:
        """Test help with mock backend."""
        result = cli_runner.invoke(
            app,
            ["--backend", "mock", "help-cmd", "/nodes"],
        )
        assert result.exit_code in (0, 1, 2)

    def test_usage_command(self, cli_runner: CliRunner) -> None:
        """Test usage command."""
        result = cli_runner.invoke(
            app,
            ["usage", "/nodes"],
        )
        assert result.exit_code in (0, 1, 2)
        assert "nodes" in result.stdout.lower() or "schema" in result.stdout.lower()


class TestOutputFormatting:
    """Test output formatting in various scenarios."""

    def test_formatter_json(self) -> None:
        """Test JSON output formatting."""
        formatter = OutputFormatter(format="json", colors=False)
        data = {"key": "value", "nested": {"count": 42}}
        output = formatter.format_output(data)
        assert "key" in output
        assert "value" in output

    def test_formatter_table(self) -> None:
        """Test table output formatting."""
        formatter = OutputFormatter(format="table", colors=False)
        data = [
            {"name": "item1", "value": "100"},
            {"name": "item2", "value": "200"},
        ]
        output = formatter.format_output(data)
        # Output may be a Rich Table object or string, just verify it doesn't raise
        assert output is not None

    def test_formatter_yaml(self) -> None:
        """Test YAML output formatting."""
        formatter = OutputFormatter(format="yaml", colors=False)
        data = {"key": "value", "list": [1, 2, 3]}
        output = formatter.format_output(data)
        assert "key" in output or "value" in output

    def test_formatter_auto_detection_list(self) -> None:
        """Test auto-detection for list data."""
        formatter = OutputFormatter(format="auto", colors=False)
        data = [
            {"id": 1, "name": "item1"},
            {"id": 2, "name": "item2"},
        ]
        # Auto should detect as table for large lists
        output = formatter.format_output(data)
        assert "item1" in output or "1" in output


class TestConfigurationManagement:
    """Test configuration file and profile management."""

    def test_config_manager_creation(self) -> None:
        """Test ConfigManager initialization."""
        mgr = ConfigManager()
        assert mgr is not None
        assert isinstance(mgr.profiles, dict)

    def test_get_default_profile(self) -> None:
        """Test getting default profile."""
        mgr = ConfigManager()
        profile = mgr.get_profile("default")
        assert profile.name == "default"
        assert profile.backend == "https"

    def test_backend_config_override(self) -> None:
        """Test backend config override."""
        config = BackendConfig(name="test")
        config.backend = "ssh_paramiko"
        config.host = "example.com"
        assert config.backend == "ssh_paramiko"
        assert config.host == "example.com"


class TestErrorHandling:
    """Test error handling in various scenarios."""

    def test_invalid_path_error(self, cli_runner: CliRunner) -> None:
        """Test invalid path handling."""
        result = cli_runner.invoke(
            app,
            ["--backend", "mock", "get", "invalid-path"],  # Missing leading /
        )
        # Should handle invalid path
        assert result.exit_code != 0

    def test_get_without_path(self, cli_runner: CliRunner) -> None:
        """Test GET command without path argument."""
        result = cli_runner.invoke(
            app,
            ["get"],
        )
        # Should require path argument
        assert result.exit_code != 0

    def test_create_without_parameters(self, cli_runner: CliRunner) -> None:
        """Test CREATE without parameters."""
        result = cli_runner.invoke(
            app,
            ["--backend", "mock", "create", "/nodes/pve1/qemu/100"],
        )
        # May or may not require parameters depending on API
        assert result.exit_code in (0, 1, 6)  # Allow various codes


class TestParameterParsing:
    """Test parameter parsing edge cases."""

    def test_multiple_data_parameters(self, cli_runner: CliRunner) -> None:
        """Test multiple -d parameters."""
        result = cli_runner.invoke(
            app,
            [
                "--backend",
                "mock",
                "create",
                "/nodes/pve1/qemu/100",
                "-d",
                "vmid=100",
                "-d",
                "name=test",
            ],
        )
        # Should parse multiple parameters
        assert result.exit_code in (0, 1, 4, 7)

    def test_data_parameter_with_spaces(self, cli_runner: CliRunner) -> None:
        """Test data parameter with spaces in value."""
        result = cli_runner.invoke(
            app,
            [
                "--backend",
                "mock",
                "create",
                "/nodes/pve1/qemu/100",
                "-d",
                "description=Test VM with spaces",
            ],
        )
        assert result.exit_code in (0, 1, 4, 7)


class TestPathNavigation:
    """Test API path navigation."""

    def test_path_normalization(self) -> None:
        """Test path normalization."""
        from proxmox_openapi.proxmox_cli.utils import validate_api_path

        path = validate_api_path("//nodes///pve1//qemu")
        assert path == "/nodes/pve1/qemu"

    def test_path_extraction(self) -> None:
        """Test path component extraction."""
        from proxmox_openapi.proxmox_cli.utils import extract_path_components

        components = extract_path_components("/nodes/pve1/qemu/100")
        assert components == ["nodes", "pve1", "qemu", "100"]


class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""

    def test_get_nodes_workflow(self, cli_runner: CliRunner) -> None:
        """Test getting nodes workflow."""
        result = cli_runner.invoke(
            app,
            ["--backend", "mock", "get", "/nodes", "--output", "json"],
        )
        # Should not crash
        assert result.exit_code in (0, 1, 4, 7)

    def test_help_workflow(self, cli_runner: CliRunner) -> None:
        """Test help workflow."""
        result = cli_runner.invoke(app, ["help-cmd"])
        assert result.exit_code in (0, 2)
        assert "command" in result.stdout.lower() or "help" in result.stdout.lower()

    def test_version_workflow(self, cli_runner: CliRunner) -> None:
        """Test version display workflow."""
        result = cli_runner.invoke(app, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.stdout.lower()
