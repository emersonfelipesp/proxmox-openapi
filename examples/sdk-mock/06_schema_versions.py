#!/usr/bin/env python3
"""Example 6: Schema Version Selection

Demonstrates:
- Using different Proxmox schema versions
- Latest vs specific version
"""

import asyncio

from proxmox_openapi.sdk import ProxmoxSDK


async def main() -> None:
    """Run example."""
    print("=" * 60)
    print("Example 6: Schema Version Selection")
    print("=" * 60)

    print("\n[Latest] Using latest schema version (default)...")
    async with ProxmoxSDK.mock(schema_version="latest") as proxmox:
        nodes = await proxmox.nodes.get()
        print(f"    ✓ Latest version: {len(nodes)} nodes")

    print("\n[Specific] Using specific schema version (if available)...")
    try:
        async with ProxmoxSDK.mock(schema_version="8.1") as proxmox:
            nodes = await proxmox.nodes.get()
            print(f"    ✓ Version 8.1: {len(nodes)} nodes")
    except Exception as e:
        print(f"    ⚠️  Version 8.1 not available: {e}")

    print("\n" + "=" * 60)
    print("✅ Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
