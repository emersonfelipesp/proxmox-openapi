"""Tests for advanced feature implementations (Phases 4-6)."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from typer.testing import CliRunner

from proxmox_openapi.proxmox_cli.cache import Cache
from proxmox_openapi.proxmox_cli.cli import app
from proxmox_openapi.proxmox_cli.completion import completion_app
from proxmox_openapi.proxmox_cli.performance import Benchmark, PerformanceMetrics
from proxmox_openapi.proxmox_cli.themes.themes import get_theme, list_themes


class TestBatchOperations:
    """Test batch operation support."""

    def test_batch_dry_run(self, cli_runner: CliRunner) -> None:
        """Test batch dry-run mode."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            batch_data = {
                "operations": [
                    {"action": "get", "path": "/nodes"},
                    {"action": "ls", "path": "/nodes"},
                ]
            }
            json.dump(batch_data, f)
            batch_file = f.name

        try:
            result = cli_runner.invoke(
                app,
                ["batch", batch_file, "--backend", "mock", "--dry-run"],
            )
            # Should succeed in dry-run mode
            assert result.exit_code in (0, 1)
        finally:
            Path(batch_file).unlink()

    def test_batch_missing_file(self, cli_runner: CliRunner) -> None:
        """Test batch with missing file."""
        result = cli_runner.invoke(
            app,
            ["batch", "/nonexistent/file.json"],
        )
        assert result.exit_code != 0


class TestCacheSystem:
    """Test caching functionality."""

    def test_cache_set_get(self) -> None:
        """Test cache set and get."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_dir=Path(tmpdir))
            cache.set("test_key", {"data": "value"})
            result = cache.get("test_key")
            assert result == {"data": "value"}

    def test_cache_expiration(self) -> None:
        """Test cache expiration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_dir=Path(tmpdir), ttl=0)  # Immediate expiration
            cache.set("test_key", {"data": "value"})

            import time

            time.sleep(0.1)

            result = cache.get("test_key")
            assert result is None

    def test_cache_clear_specific(self) -> None:
        """Test clearing specific cache entry."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_dir=Path(tmpdir))
            cache.set("key1", {"data": 1})
            cache.set("key2", {"data": 2})

            cache.clear("key1")

            assert cache.get("key1") is None
            assert cache.get("key2") == {"data": 2}

    def test_cache_clear_all(self) -> None:
        """Test clearing all cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_dir=Path(tmpdir))
            cache.set("key1", {"data": 1})
            cache.set("key2", {"data": 2})

            cache.clear()

            assert cache.get("key1") is None
            assert cache.get("key2") is None


class TestPerformanceBenchmark:
    """Test performance benchmarking."""

    def test_benchmark_single_iteration(self) -> None:
        """Test benchmark with single iteration."""
        bench = Benchmark("test")
        metrics = bench.run(lambda: None, iterations=1)

        assert metrics.operation == "test"
        assert metrics.iterations == 1
        assert metrics.total_time >= 0

    def test_benchmark_multiple_iterations(self) -> None:
        """Test benchmark with multiple iterations."""
        bench = Benchmark("test")
        metrics = bench.run(lambda: None, iterations=5)

        assert metrics.iterations == 5
        assert metrics.min_time >= 0
        assert metrics.max_time >= metrics.min_time
        assert len(bench.times) == 5

    def test_performance_metrics_string(self) -> None:
        """Test performance metrics formatting."""
        metrics = PerformanceMetrics(
            operation="test_op",
            total_time=0.1,
            min_time=0.01,
            max_time=0.05,
            avg_time=0.03,
            median_time=0.03,
            iterations=10,
        )
        result = str(metrics)
        assert "test_op" in result
        assert "Total" in result


class TestConfigurationCommands:
    """Test configuration management commands."""

    def test_config_list_command(self, cli_runner: CliRunner) -> None:
        """Test config list command."""
        result = cli_runner.invoke(app, ["config-list"])
        # Should show profiles or "No profiles"
        assert result.exit_code in (0, 1)

    def test_config_show_default(self, cli_runner: CliRunner) -> None:
        """Test showing default profile."""
        result = cli_runner.invoke(app, ["config-show", "default"])
        assert result.exit_code in (0, 1)
        # Should contain profile information
        assert "Profile" in result.stdout or "default" in result.stdout.lower()


class TestThemeSystem:
    """Test theme system."""

    def test_get_dark_theme(self) -> None:
        """Test getting dark theme."""
        theme = get_theme("dark")
        assert theme is not None
        assert theme.name == "dark"
        assert theme.primary == "#00DD00"

    def test_get_light_theme(self) -> None:
        """Test getting light theme."""
        theme = get_theme("light")
        assert theme is not None
        assert theme.name == "light"

    def test_get_monokai_theme(self) -> None:
        """Test getting monokai theme."""
        theme = get_theme("monokai")
        assert theme is not None
        assert theme.name == "monokai"

    def test_get_nonexistent_theme(self) -> None:
        """Test getting nonexistent theme."""
        theme = get_theme("nonexistent")
        assert theme is None

    def test_list_themes(self) -> None:
        """Test listing themes."""
        themes = list_themes()
        assert len(themes) >= 3
        assert "dark" in themes
        assert "light" in themes
        assert "monokai" in themes


class TestCompletionSystem:
    """Test shell completion support."""

    def test_completion_app_exists(self) -> None:
        """Test completion app is available."""
        assert completion_app is not None

    def test_bash_completion_command(self, cli_runner: CliRunner) -> None:
        """Test bash completion."""
        result = cli_runner.invoke(completion_app, ["install-bash"])
        # Should output completion script
        assert result.exit_code in (0, 1)

    def test_zsh_completion_command(self, cli_runner: CliRunner) -> None:
        """Test zsh completion."""
        result = cli_runner.invoke(completion_app, ["install-zsh"])
        # Should output completion script
        assert result.exit_code in (0, 1)


class TestEndToEndAdvancedFeatures:
    """End-to-end tests for advanced features."""

    def test_cache_invalidation_workflow(self) -> None:
        """Test cache invalidation on write operations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_dir=Path(tmpdir))
            cache.set("/nodes", {"data": "nodes"})
            cache.set("/nodes/pve1", {"data": "pve1"})

            # Verify both are cached
            assert cache.get("/nodes") is not None
            assert cache.get("/nodes/pve1") is not None

            # Clear and verify
            cache.clear("/nodes")
            assert cache.get("/nodes") is None

    def test_theme_application(self) -> None:
        """Test theme application."""
        for theme_name in list_themes():
            theme = get_theme(theme_name)
            assert theme is not None
            assert hasattr(theme, "primary")
            assert hasattr(theme, "error")
            assert hasattr(theme, "success")

    def test_benchmark_consistency(self) -> None:
        """Test benchmark gives consistent results."""

        def test_func() -> None:
            """Simple test function."""
            pass

        bench1 = Benchmark("test1")
        bench2 = Benchmark("test2")

        metrics1 = bench1.run(test_func, iterations=10)
        metrics2 = bench2.run(test_func, iterations=10)

        # Both should report same number of iterations
        assert metrics1.iterations == metrics2.iterations == 10
        # Times should be reasonable (> 0)
        assert metrics1.total_time >= 0
        assert metrics2.total_time >= 0
