#!/usr/bin/env python3
"""Example 1: Session Setup and Authentication

Demonstrates different ways to authenticate and set up a Proxmox SDK session:
- API token authentication (recommended)
- Password authentication
- SSH key authentication
- Local backend
- Mock backend (for testing)

Configure credentials before running:
  export PROXMOX_HOST="pve.example.com"
  export PROXMOX_USER="automation@pve"
  export PROXMOX_TOKEN_NAME="api-token"
  export PROXMOX_TOKEN_VALUE="12345678-abcd-1234-abcd-1234567890ab"

Or edit the example values below.
"""

import asyncio
import os
from proxmox_openapi import ProxmoxSDK


async def example_api_token_auth() -> None:
    """Example 1: API Token Authentication (Recommended for Automation)"""
    print("\n" + "=" * 60)
    print("Example 1: API Token Authentication")
    print("=" * 60)

    async with ProxmoxSDK(
        host=os.getenv("PROXMOX_HOST") or "pve.example.com",
        user=os.getenv("PROXMOX_USER") or "automation@pve",
        token_name=os.getenv("PROXMOX_TOKEN_NAME") or "api-token",
        token_value=os.getenv("PROXMOX_TOKEN_VALUE") or "12345678-abcd-...",
    ) as proxmox:
        try:
            nodes = await proxmox.nodes.get()
            print(f"✓ Connected successfully!")
            print(f"  Found {len(nodes)} node(s)")
        except Exception as e:
            print(f"✗ Connection failed (check credentials): {e}")


async def example_password_auth() -> None:
    """Example 2: Password Authentication (Simple but less secure)"""
    print("\n" + "=" * 60)
    print("Example 2: Password Authentication")
    print("=" * 60)

    async with ProxmoxSDK(
        host="pve.example.com",
        user="admin@pam",
        password="my-password",  # Use env var in production!
    ) as proxmox:
        try:
            nodes = await proxmox.nodes.get()
            print(f"✓ Connected successfully!")
        except Exception as e:
            print(f"✗ Connection failed: {e}")


async def example_ssh_key_auth() -> None:
    """Example 3: SSH Key Authentication"""
    print("\n" + "=" * 60)
    print("Example 3: SSH Key Authentication")
    print("=" * 60)

    async with ProxmoxSDK(
        host="pve.example.com",
        user="root",
        private_key_file="/home/user/.ssh/id_rsa",
        backend="ssh_paramiko",
    ) as proxmox:
        try:
            nodes = await proxmox.nodes.get()
            print(f"✓ Connected successfully via SSH!")
        except Exception as e:
            print(f"✗ Connection failed: {e}")


def example_sync_wrapper() -> None:
    """Example 4: Synchronous Wrapper (Blocking Calls)"""
    print("\n" + "=" * 60)
    print("Example 4: Synchronous Wrapper (Blocking)")
    print("=" * 60)

    with ProxmoxSDK.sync(
        host="pve.example.com",
        user="automation@pve",
        token_name="api-token",
        token_value="12345678-abcd-...",
    ) as proxmox:
        try:
            nodes = proxmox.nodes.get()
            print(f"✓ Connected successfully (sync)!")
            print(f"  Found {len(nodes)} node(s)")
        except Exception as e:
            print(f"✗ Connection failed: {e}")


async def example_mock_backend() -> None:
    """Example 5: Mock Backend (for testing, no credentials needed)"""
    print("\n" + "=" * 60)
    print("Example 5: Mock Backend (Testing)")
    print("=" * 60)

    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        print(f"✓ Mock connection successful!")
        print(f"  Mock nodes: {[n['node'] for n in nodes]}")


async def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Proxmox SDK: Authentication Examples")
    print("=" * 60)

    # Example 1: Mock (always works)
    await example_mock_backend()

    # Example 2: API Token (comment out or set env vars)
    # await example_api_token_auth()

    # Example 3: Password (comment out to test)
    # await example_password_auth()

    # Example 4: SSH Key (comment out to test)
    # await example_ssh_key_auth()

    # Example 5: Sync wrapper (comment out to test)
    # example_sync_wrapper()

    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
