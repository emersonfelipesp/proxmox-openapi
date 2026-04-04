#!/usr/bin/env python3
"""Example 1: Basic SDK Mock Usage (Async)

Demonstrates:
- Creating a mock SDK instance
- Listing nodes
- Creating a VM
- Retrieving a specific VM
"""

import asyncio

from proxmox_openapi.sdk import ProxmoxSDK


async def main() -> None:
    """Run example."""
    print("=" * 60)
    print("Example 1: Basic Mock SDK Usage (Async)")
    print("=" * 60)

    # Create a mock SDK instance
    async with ProxmoxSDK.mock() as proxmox:
        print("\n[1] Listing nodes...")
        nodes = await proxmox.nodes.get()
        print(f"    Found {len(nodes)} node(s)")
        for node in nodes:
            print(f"      - {node.get('node')}: {node.get('status')}")

        print("\n[2] Creating a VM...")
        vm = await proxmox.nodes("pve").qemu.post(
            vmid=100,
            name="example-vm",
            memory=2048,
            cores=2,
        )
        print(f"    Created: VM {vm.get('vmid')} ({vm.get('name')})")

        print("\n[3] Retrieving the VM...")
        # GET /nodes/{node}/qemu/{vmid} returns a list of resources
        # To get the VM config, use /nodes/{node}/qemu/{vmid}/config
        vm_list = await proxmox.nodes("pve").qemu(100).get()
        print(f"    Retrieved: {vm_list}")

        print("\n[4] Listing all VMs on 'pve' node...")
        vms = await proxmox.nodes("pve").qemu.get()
        print(f"    Found {len(vms)} VM(s)")
        for vm in vms:
            # Each VM in the list has vmid and name
            if isinstance(vm, dict):
                print(f"      - {vm.get('name', 'N/A')} (ID: {vm.get('vmid', 'N/A')})")

    print("\n" + "=" * 60)
    print("✅ Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
