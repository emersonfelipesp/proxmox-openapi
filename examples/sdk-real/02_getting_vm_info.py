#!/usr/bin/env python3
"""Example 2: Getting VM Information

Demonstrates how to:
- List all nodes
- List VMs on a node
- Get detailed VM configuration
- Check VM status
- Filter VMs
- Search VMs by name

This example uses the mock backend by default (no credentials needed).
To use a real Proxmox instance, update the connection parameters.
"""

import asyncio
from proxmox_openapi import ProxmoxSDK


async def list_nodes() -> None:
    """List all nodes in the cluster."""
    print("\n[1] Listing all nodes...")
    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        print(f"    Found {len(nodes)} node(s):")
        for node in nodes:
            print(f"      • {node['node']:15} Status: {node['status']:10} Uptime: {node.get('uptime', 0):>10} sec")


async def list_vms_on_node(node: str) -> None:
    """List all VMs on a specific node."""
    print(f"\n[2] Listing VMs on node '{node}'...")
    async with ProxmoxSDK.mock() as proxmox:
        vms = await proxmox.nodes(node).qemu.get()
        print(f"    Found {len(vms)} VM(s):")
        print(f"      {'VMID':<8} {'Name':<20} {'Status':<12} {'Memory':<10} {'CPUs':<5}")
        print(f"      {'-'*55}")

        for vm in vms:
            vmid = vm.get('vmid')
            name = vm.get('name', 'N/A')
            status = vm.get('status', 'unknown')
            try:
                config = await proxmox.nodes(node).qemu(vmid).config.get()
                memory_gb = config.get('memory', 0) / 1024
                cores = config.get('cores', 0)
                print(f"      {vmid:<8} {name:<20} {status:<12} {memory_gb:>6.1f}GB   {cores:<5}")
            except Exception as e:
                print(f"      {vmid:<8} {name:<20} {status:<12} [Error getting config]")


async def get_vm_details(node: str, vmid: int) -> None:
    """Get detailed configuration of a specific VM."""
    print(f"\n[3] Getting details for VM {vmid} on node '{node}'...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            config = await proxmox.nodes(node).qemu(vmid).config.get()

            print(f"    VM Configuration:")
            print(f"      Name:        {config.get('name', 'N/A')}")
            print(f"      Memory:      {config.get('memory', 0) / 1024:.1f} GB")
            print(f"      Cores:       {config.get('cores', 0)}")
            print(f"      Sockets:     {config.get('sockets', 1)}")
            print(f"      Boot:        {config.get('boot', 'c')}")
            print(f"      Description: {config.get('description', 'N/A')}")
            print(f"      BIOS:        {config.get('bios', 'seabios')}")

            # List disks
            print(f"    Disks:")
            for key, value in config.items():
                if key.startswith('virtio') or key.startswith('scsi') or key.startswith('sata'):
                    print(f"      {key}: {value}")

            # List network interfaces
            print(f"    Networks:")
            for key, value in config.items():
                if key.startswith('net'):
                    print(f"      {key}: {value}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def get_vm_status(node: str, vmid: int) -> None:
    """Get current status of a VM."""
    print(f"\n[4] Getting status for VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            status = await proxmox.nodes(node).qemu(vmid).status.current.get()

            print(f"    VM Status:")
            print(f"      Status:      {status.get('status', 'unknown')}")
            print(f"      CPU:         {status.get('cpu', 0):.1%}")
            print(f"      Memory:      {status.get('mem', 0) / 1024 / 1024 / 1024:.2f} GB "
                  f"/ {status.get('maxmem', 0) / 1024 / 1024 / 1024:.2f} GB")
            print(f"      Uptime:      {status.get('uptime', 0)} seconds")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def filter_running_vms(node: str) -> None:
    """Filter VMs by status (e.g., only running)."""
    print(f"\n[5] Filtering running VMs on node '{node}'...")
    async with ProxmoxSDK.mock() as proxmox:
        vms = await proxmox.nodes(node).qemu.get()

        running_vms = [vm for vm in vms if vm['status'] == 'running']
        print(f"    Running VMs: {len(running_vms)}")
        for vm in running_vms:
            print(f"      • {vm['name']} (ID: {vm['vmid']})")


async def search_vm_by_name(node: str, search_name: str) -> None:
    """Search for a VM by name."""
    print(f"\n[6] Searching for VM matching '{search_name}'...")
    async with ProxmoxSDK.mock() as proxmox:
        vms = await proxmox.nodes(node).qemu.get()

        matching_vms = [vm for vm in vms if search_name.lower() in vm['name'].lower()]

        if matching_vms:
            print(f"    Found {len(matching_vms)} matching VM(s):")
            for vm in matching_vms:
                print(f"      • {vm['name']} (ID: {vm['vmid']}, Status: {vm['status']})")
        else:
            print(f"    ✗ No VMs found matching '{search_name}'")


async def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Proxmox SDK: Getting VM Information")
    print("=" * 60)

    # Run examples
    await list_nodes()

    # Use the first node we can find
    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        if nodes:
            node = nodes[0]['node']

            await list_vms_on_node(node)
            await get_vm_details(node, 100)
            await get_vm_status(node, 100)
            await filter_running_vms(node)
            await search_vm_by_name(node, "web")

    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
