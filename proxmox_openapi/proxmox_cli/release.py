#!/usr/bin/env python3
"""Release and packaging script for proxmox CLI."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def get_current_version() -> str:
    """Get current version from pyproject.toml.

    Returns:
        Version string
    """
    pyproject = Path("pyproject.toml")
    with open(pyproject) as f:
        for line in f:
            if line.startswith("version"):
                match = re.search(r'version\s*=\s*"([^"]+)"', line)
                if match:
                    return match.group(1)
    raise ValueError("Could not find version in pyproject.toml")


def run_command(cmd: list[str]) -> bool:
    """Run a command.

    Args:
        cmd: Command as list

    Returns:
        True if successful
    """
    print(f"  > {' '.join(cmd)}")
    return subprocess.run(cmd, check=False).returncode == 0


def main() -> None:
    """Run release steps."""
    print("[*] Proxmox CLI Release Script")
    print("=" * 50)

    current_version = get_current_version()
    print(f"Current version: {current_version}")

    # Pre-release checks
    print("\n[*] Running pre-release checks...")
    checks = [
        ([sys.executable, "-m", "pytest", "tests/cli", "-v"], "Tests"),
        (["python", "-m", "ruff", "check", "proxmox_openapi/proxmox_cli"], "Linting"),
        ([sys.executable, "-m", "mypy", "proxmox_openapi/proxmox_cli"], "Type checking"),
    ]

    all_passed = True
    for cmd, name in checks:
        print(f"\n  Checking {name}...")
        if not run_command(cmd):
            print(f"[!] {name} failed!")
            all_passed = False

    if not all_passed:
        print("\n[!] Pre-release checks failed!")
        sys.exit(1)

    print("\n[+] Pre-release checks passed!")

    # Build instructions
    print("\n[*] Build instructions:")
    print("  1. Update version in pyproject.toml")
    print("  2. Update CHANGELOG.md")
    print("  3. Commit changes")
    print("  4. Create git tag: git tag v{version}")
    print("  5. Build: python -m build")
    print("  6. Upload: python -m twine upload dist/*")


if __name__ == "__main__":
    main()
