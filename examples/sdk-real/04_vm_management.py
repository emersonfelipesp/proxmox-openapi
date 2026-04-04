#!/usr/bin/env python3
"""Example 4: VM Power Management and Operations

Demonstrates how to:
- Start a VM
- Stop a VM (clean shutdown)
- Force stop (immediate power off)
- Reboot a VM
- Suspend a VM
- Update VM configuration
- Delete a VM

This example uses the mock backend by default.
To use a real Proxmox instance, update the connection parameters.
"""

import asyncio
from proxmox_openapi import ProxmoxSDK


async def start_vm(node: str, vmid: int) -> None:
    """Start a VM."""
    print(f"\n[1] Starting VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).status.start.post()
            print(f"    ✓ Start command sent")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")
        except Exception as e:
            print(f"    ✗ Error: {e}")


async def stop_vm_graceful(node: str, vmid: int) -> None:
    """Stop VM with clean shutdown (ACPI)."""
    print(f"\n[2] Stopping VM {vmid} (graceful shutdown)...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).status.shutdown.post()
            print(f"    ✓ Shutdown signal sent (will wait for OS to shut down)")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")
        except Exception as e:
            print(f"    ✗ Error: {e}")


async def stop_vm_force(node: str, vmid: int) -> None:
    """Force stop VM (immediate power off)."""
    print(f"\n[3] Forcing stop of VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).status.stop.post()
            print(f"    ✓ Force stop command sent (immediate power off)")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")
        except Exception as e:
            print(f"    ✗ Error: {e}")


async def reboot_vm(node: str, vmid: int) -> None:
    """Reboot a VM."""
    print(f"\n[4] Rebooting VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).status.reboot.post()
            print(f"    ✓ Reboot command sent")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")
        except Exception as e:
            print(f"    ✗ Error: {e}")


async def suspend_vm(node: str, vmid: int) -> None:
    """Suspend a VM (freeze without power off)."""
    print(f"\n[5] Suspending VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).status.suspend.post()
            print(f"    ✓ Suspend command sent")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")
        except Exception as e:
            print(f"    ✗ Error: {e}")


async def update_vm_config(node: str, vmid: int) -> None:
    """Update VM configuration (e.g., memory, cores)."""
    print(f"\n[6] Updating VM {vmid} configuration...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            # Note: Some changes require VM to be stopped
            result = await proxmox.nodes(node).qemu(vmid).config.put(
                memory=4096,  # Increase to 4GB
                cores=4,  # Increase to 4 cores
                description="Updated configuration",
            )

            print(f"    ✓ Configuration updated")
            print(f"      New Memory: 4096 MB")
            print(f"      New Cores: 4")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def resize_vm_disk(node: str, vmid: int) -> None:
    """Resize a VM's disk."""
    print(f"\n[7] Resizing VM {vmid} disk...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).resize.post(
                disk="virtio0",
                size="+40G",  # Add 40GB
            )

            print(f"    ✓ Resize command sent")
            print(f"      Adding 40GB to virtio0")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def delete_vm(node: str, vmid: int) -> None:
    """Delete/destroy a VM."""
    print(f"\n[8] Deleting VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).delete()
            print(f"    ✓ VM deleted successfully")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")
        except Exception as e:
            print(f"    ✗ Error: {e}")


async def vm_lifecycle_demo(node: str) -> None:
    """Demonstrate a complete VM lifecycle."""
    print("\n[9] Complete VM lifecycle demo...")
    vmid = 999

    async with ProxmoxSDK.mock() as proxmox:
        try:
            # Create
            print("     • Creating VM...")
            vm_result = await proxmox.nodes(node).qemu.post(
                vmid=vmid,
                name="lifecycle-demo",
                memory=1024,
                cores=1,
                virtio0="local:30",
            )
            print(f"       ✓ Created VM {vmid}")

            # Get status
            print("     • Checking status...")
            status = await proxmox.nodes(node).qemu(vmid).status.current.get()
            print(f"       Status: {status.get('status')}")

            # Get config
            print("     • Getting configuration...")
            config = await proxmox.nodes(node).qemu(vmid).config.get()
            print(f"       Memory: {config.get('memory')} MB")

            # Delete
            print("     • Deleting VM...")
            await proxmox.nodes(node).qemu(vmid).delete()
            print(f"       ✓ VM deleted")

            print("     ✓ Lifecycle demo complete")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Proxmox SDK: VM Power Management")
    print("=" * 60)

    # Get first available node
    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        if nodes:
            node = nodes[0]['node']
            vms = await proxmox.nodes(node).qemu.get()

            print(f"\nUsing node: {node}")

            if vms:
                vmid = vms[0]['vmid']
                print(f"Using VM: {vms[0]['name']} (ID: {vmid})")

                # Run examples (non-destructive operations)
                await start_vm(node, vmid)
                await reboot_vm(node, vmid)
                await stop_vm_graceful(node, vmid)
                await update_vm_config(node, vmid)

            # Demo operations
            await vm_lifecycle_demo(node)

    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
