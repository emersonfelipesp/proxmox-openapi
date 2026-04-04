"""Performance monitoring and benchmarking tools."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from statistics import mean, median
from typing import Any, Callable, Optional

import typer

from proxmox_openapi.proxmox_cli.app import app
from proxmox_openapi.proxmox_cli.config import ConfigManager
from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge


@dataclass
class PerformanceMetrics:
    """Performance metrics for operations."""

    operation: str
    total_time: float
    min_time: float = field(default_factory=float)
    max_time: float = field(default_factory=float)
    avg_time: float = field(default_factory=float)
    median_time: float = field(default_factory=float)
    iterations: int = 1

    def __str__(self) -> str:
        """Format as readable string."""
        if self.iterations == 1:
            return f"{self.operation}: {self.total_time * 1000:.2f}ms ({self.total_time:.4f}s)"
        return (
            f"{self.operation}:\n"
            f"  Total: {self.total_time:.2f}s\n"
            f"  Min: {self.min_time * 1000:.2f}ms\n"
            f"  Max: {self.max_time * 1000:.2f}ms\n"
            f"  Avg: {self.avg_time * 1000:.2f}ms\n"
            f"  Median: {self.median_time * 1000:.2f}ms\n"
            f"  Iterations: {self.iterations}"
        )


class Benchmark:
    """Benchmarking utility for performance testing."""

    def __init__(self, name: str):
        """Initialize benchmark.

        Args:
            name: Benchmark name
        """
        self.name = name
        self.start_time: Optional[float] = None
        self.times: list[float] = []

    def __enter__(self) -> Benchmark:
        """Start timing."""
        self.start_time = time.time()
        return self

    def __exit__(self, *args: Any) -> None:
        """Stop timing and record."""
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            self.times.append(elapsed)

    def run(self, func: Callable[[], Any], iterations: int = 1) -> PerformanceMetrics:
        """Run function and measure performance.

        Args:
            func: Function to benchmark
            iterations: Number of iterations

        Returns:
            Performance metrics
        """
        for _ in range(iterations):
            with self:
                func()

        total = sum(self.times)
        return PerformanceMetrics(
            operation=self.name,
            total_time=total,
            min_time=min(self.times),
            max_time=max(self.times),
            avg_time=mean(self.times),
            median_time=median(self.times),
            iterations=iterations,
        )


@app.command()
def benchmark(
    iterations: int = typer.Option(5, help="Number of iterations to run"),
    path: str = typer.Option("/nodes", help="API path to benchmark"),
    backend: Optional[str] = typer.Option(None, help="Backend to use"),
) -> None:
    """Benchmark API performance.

    Example:
        proxmox benchmark --path /nodes
        proxmox benchmark --path /nodes --iterations 10
        proxmox benchmark --backend https --path /nodes/pve1/qemu
    """
    try:
        config_mgr = ConfigManager()
        config = config_mgr.get_profile("default")
        if backend:
            config.backend = backend

        bridge = ProxmoxSDKBridge.create(config)

        typer.echo(f"Benchmarking GET {path} ({iterations} iterations)...")

        def get_operation() -> None:
            bridge.get(path)

        bench = Benchmark(f"GET {path}")
        metrics = bench.run(get_operation, iterations)

        typer.echo(str(metrics))
        typer.echo("\nBenchmark complete!")

    except Exception as e:
        typer.echo(f"Benchmark failed: {e}", err=True)
        raise typer.Exit(code=1)


@app.command()
def perf_test(
    operation: str = typer.Argument("get", help="Operation type (get/create/list)"),
    iterations: int = typer.Option(10, help="Number of iterations"),
) -> None:
    """Run performance tests.

    Example:
        proxmox perf-test get --iterations 20
        proxmox perf-test list
    """
    if operation == "get":
        typer.invoke(
            benchmark,
            [
                "--path",
                "/nodes",
                "--iterations",
                str(iterations),
            ],
        )
    else:
        typer.echo(f"Performance test for '{operation}' not yet implemented")
        raise typer.Exit(code=1)
