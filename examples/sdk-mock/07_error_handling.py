#!/usr/bin/env python3
"""Example 7: Error Handling

Demonstrates:
- Catching ResourceException
- Handling errors gracefully
- Error recovery
"""

import asyncio

from proxmox_openapi.sdk import ProxmoxSDK
from proxmox_openapi.sdk.exceptions import ResourceException


async def main() -> None:
    """Run example."""
    print("=" * 60)
    print("Example 7: Error Handling")
    print("=" * 60)

    async with ProxmoxSDK.mock() as proxmox:
        print("\n[Attempt 1] Creating a valid VM...")
        try:
            vm = await proxmox.nodes("pve").qemu.post(
                vmid=400,
                name="valid-vm",
            )
            print(f"    ✓ Success: {vm.get('name')}")
        except ResourceException as e:
            print(f"    ✗ Failed: {e.status_message}")

        print("\n[Attempt 2] Creating duplicate VM (error)...")
        try:
            vm = await proxmox.nodes("pve").qemu.post(
                vmid=400,  # Same ID as above
                name="duplicate-vm",
            )
            print(f"    ✓ Success: {vm.get('name')}")
        except ResourceException as e:
            print(f"    ✗ Expected error: {e.status_message}")

        print("\n[Attempt 3] Accessing non-existent node...")
        try:
            result = await proxmox.nodes("nonexistent").status.get()
            print(f"    ✓ Success: {result}")
        except ResourceException as e:
            print(f"    ✗ Expected error: {e.status_code} - {e.status_message}")

        print("\n[Attempt 4] Graceful error recovery...")
        for vmid in range(401, 404):
            try:
                vm = await proxmox.nodes("pve").qemu.post(
                    vmid=vmid,
                    name=f"vm-{vmid}",
                )
                print(f"    ✓ Created VM {vmid}")
            except ResourceException as e:
                print(f"    ✗ Failed to create VM {vmid}: {e.status_message}")
                # Continue with next iteration
                continue

    print("\n" + "=" * 60)
    print("✅ Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
