#!/usr/bin/env python3
"""Example 5: Multi-Service Support

Demonstrates:
- Using different Proxmox services (PVE, PMG, PBS)
- Service-specific endpoints
"""

import asyncio

from proxmox_openapi.sdk import ProxmoxSDK


async def main() -> None:
    """Run example."""
    print("=" * 60)
    print("Example 5: Multi-Service Support")
    print("=" * 60)

    print("\n[PVE] Proxmox VE (Virtual Environment)")
    async with ProxmoxSDK.mock(service="PVE") as proxmox:
        nodes = await proxmox.nodes.get()
        print(f"    ✓ PVE Nodes: {len(nodes)}")

    print("\n[PMG] Proxmox Mail Gateway")
    async with ProxmoxSDK.mock(service="PMG") as proxmox:
        # PMG has different endpoints
        print("    ✓ PMG mock instance created")

    print("\n[PBS] Proxmox Backup Server")
    async with ProxmoxSDK.mock(service="PBS") as proxmox:
        # PBS has different endpoints
        print("    ✓ PBS mock instance created")

    print("\n" + "=" * 60)
    print("✅ Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
