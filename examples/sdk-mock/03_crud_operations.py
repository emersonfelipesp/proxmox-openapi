#!/usr/bin/env python3
"""Example 3: CRUD Operations with Mock SDK

Demonstrates:
- Create (POST)
- Read (GET)
- Update (PUT / PATCH)
- Delete (DELETE)
"""

import asyncio

from proxmox_openapi.sdk import ProxmoxSDK


async def main() -> None:
    """Run example."""
    print("=" * 60)
    print("Example 3: CRUD Operations")
    print("=" * 60)

    async with ProxmoxSDK.mock() as proxmox:
        print("\n[CREATE] Creating multiple VMs...")
        vms = []
        for i in range(3):
            vm = await proxmox.nodes("pve").qemu.post(
                vmid=200 + i,
                name=f"crud-vm-{i}",
                memory=2048,
                cores=2,
            )
            vms.append(vm)
            print(f"    ✓ Created: {vm.get('name')} (ID: {vm.get('vmid')})")

        print("\n[READ] Retrieving all created VMs...")
        all_vms = await proxmox.nodes("pve").qemu.get()
        print(f"    Total VMs: {len(all_vms)}")
        for vm in all_vms:
            print(
                f"      - {vm.get('name')} (ID: {vm.get('vmid')}, Memory: {vm.get('memory')} bytes)"
            )

        print("\n[UPDATE] Updating VM properties...")
        updated = (
            await proxmox.nodes("pve")
            .qemu(200)
            .put(
                name="crud-vm-0-updated",
                memory=4096,
                cores=4,
            )
        )
        print(f"    ✓ Updated: {updated.get('name')}")
        print(f"      Memory: {updated.get('memory')} bytes")
        print(f"      Cores: {updated.get('cores')}")

        print("\n[PATCH] Patching VM name only...")
        patched = (
            await proxmox.nodes("pve")
            .qemu(201)
            .patch(
                name="crud-vm-1-patched",
            )
        )
        print(f"    ✓ Patched: {patched.get('name')}")

        print("\n[DELETE] Deleting VMs...")
        for vm_id in [200, 201, 202]:
            result = await proxmox.nodes("pve").qemu(vm_id).delete()
            print(f"    ✓ Deleted VM {vm_id}: {result}")

        print("\n[READ] Verifying deletion...")
        remaining = await proxmox.nodes("pve").qemu.get()
        print(f"    Remaining VMs: {len(remaining)}")

    print("\n" + "=" * 60)
    print("✅ Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
