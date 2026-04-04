#!/usr/bin/env python3
"""Installation and distribution script for proxmox CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run a shell command.

    Args:
        cmd: Command and arguments as list
        description: Description of command for logging

    Returns:
        True if successful, False otherwise
    """
    print(f"[*] {description}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] {description} failed:", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        return False


def main() -> None:
    """Run installation steps."""
    print("[*] Proxmox CLI Installation Script")
    print("=" * 50)

    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent

    # Change to project root
    import os

    os.chdir(project_root)

    steps = [
        (
            [sys.executable, "-m", "pip", "install", "-e", "."],
            "Installing proxmox-openapi in development mode",
        ),
        (
            [sys.executable, "-m", "pip", "install", "-e", ".[cli]"],
            "Installing CLI dependencies",
        ),
        (
            [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
            "Installing development dependencies",
        ),
        (
            [sys.executable, "-m", "pytest", "tests/cli", "-v"],
            "Running CLI tests",
        ),
    ]

    for cmd, description in steps:
        if not run_command(cmd, description):
            print(f"[!] Installation failed at: {description}")
            sys.exit(1)

    print("\n[+] Installation completed successfully!")
    print("\nNext steps:")
    print("  1. Configure profile: proxmox config-add myprofile --host proxmox.example.com")
    print("  2. Test connection: proxmox --backend https ls /nodes")
    print("  3. View help: proxmox --help")


if __name__ == "__main__":
    main()
