#!/usr/bin/env python3
"""Example 3: Creating Virtual Machines

Demonstrates how to:
- Create a minimal VM
- Create a standard VM with full configuration
- Create a VM with cloud-init support
- Create a VM with multiple disks
- Create a VM with multiple network interfaces
- Handle task IDs for long-running operations

This example uses the mock backend by default (no real VMs created).
To use a real Proxmox instance, update the connection parameters.
"""

import asyncio

from proxmox_openapi import ProxmoxSDK


async def create_minimal_vm(node: str) -> None:
    """Create the simplest possible VM (1 core, 512MB RAM)."""
    print("\n[1] Creating minimal VM...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu.post(
                vmid=100,
                name="minimal-vm",
                memory=512,
                cores=1,
            )

            print("    ✓ VM created successfully!")
            print(f"      VMID: {result.get('vmid')}")
            print(f"      Name: {result.get('name')}")
            print(f"      Memory: {result.get('memory')} MB")
            print(f"      Cores: {result.get('cores')}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def create_standard_vm(node: str) -> None:
    """Create a standard VM with recommended configuration."""
    print("\n[2] Creating standard VM...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu.post(
                vmid=101,
                name="web-server",
                # Hardware
                memory=2048,  # 2GB RAM
                cores=2,  # 2 CPU cores
                sockets=1,
                # Disk
                virtio0="local:60",  # 60GB disk
                # Boot
                boot="c",  # Boot from disk
                # Network
                net0="virtio,bridge=vmbr0",
                # Other
                bios="seabios",
                description="Production web server",
            )

            print("    ✓ VM created successfully!")
            print(f"      VMID: {result.get('vmid')}")
            print(f"      Name: {result.get('name')}")
            print(f"      Memory: {result.get('memory')} MB")
            print(f"      Cores: {result.get('cores')}")
            print(f"      Primary Disk: {result.get('virtio0')}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def create_cloud_init_vm(node: str) -> None:
    """Create a VM with cloud-init support for automated provisioning."""
    print("\n[3] Creating cloud-init VM...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu.post(
                vmid=102,
                name="cloud-vm",
                # Hardware (cloud-init optimized)
                memory=1024,
                cores=2,
                agent=1,  # Enable QEMU guest agent
                # Storage
                scsi0="local:50",  # Cloud-init compatible disk
                ide2="local:cloudinit",
                # Boot
                boot="order=scsi0;ide2",
                # Network
                net0="virtio,bridge=vmbr0",
                # Cloud-init
                citype="nocloud",
                ciuser="ubuntu",
                cipassword="changeme",  # Should use SSH keys in production
                description="Cloud-init enabled VM",
            )

            print("    ✓ Cloud-init VM created successfully!")
            print(f"      VMID: {result.get('vmid')}")
            print(f"      Name: {result.get('name')}")
            print("      CI User: ubuntu")
            print("      CI Type: nocloud")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def create_multi_disk_vm(node: str) -> None:
    """Create a VM with multiple disks from different storages."""
    print("\n[4] Creating multi-disk VM...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu.post(
                vmid=103,
                name="data-vm",
                # Hardware
                memory=4096,
                cores=4,
                # Primary OS disk
                virtio0="local:100",
                # Data disks (different storage)
                virtio1="local-lvm:100",  # Second disk
                virtio2="local-lvm:200",  # Third disk
                # Boot
                boot="c",
                # Network
                net0="virtio,bridge=vmbr0",
                description="Multi-disk data VM",
            )

            print("    ✓ Multi-disk VM created successfully!")
            print(f"      VMID: {result.get('vmid')}")
            print(f"      Name: {result.get('name')}")
            print(f"      Primary Disk: {result.get('virtio0')}")
            print(f"      Data Disk 1: {result.get('virtio1')}")
            print(f"      Data Disk 2: {result.get('virtio2')}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def create_multi_network_vm(node: str) -> None:
    """Create a VM with multiple network interfaces."""
    print("\n[5] Creating multi-network VM...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu.post(
                vmid=104,
                name="multi-net-vm",
                # Hardware
                memory=2048,
                cores=2,
                virtio0="local:50",
                # Multiple networks
                net0="virtio,bridge=vmbr0",  # Management
                net1="virtio,bridge=vmbr1",  # Data
                net2="virtio,bridge=vmbr2",  # Storage
                boot="c",
                description="Multi-network VM",
            )

            print("    ✓ Multi-network VM created successfully!")
            print(f"      VMID: {result.get('vmid')}")
            print(f"      Name: {result.get('name')}")
            print(f"      Management Network: {result.get('net0')}")
            print(f"      Data Network: {result.get('net1')}")
            print(f"      Storage Network: {result.get('net2')}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def batch_create_vms(node: str) -> None:
    """Create multiple VMs in sequence."""
    print("\n[6] Batch creating VMs...")

    vm_configs = [
        {"vmid": 200, "name": "web-01", "cores": 2},
        {"vmid": 201, "name": "web-02", "cores": 2},
        {"vmid": 202, "name": "app-01", "cores": 4},
    ]

    async with ProxmoxSDK.mock() as proxmox:
        created = 0
        failed = 0

        for config in vm_configs:
            try:
                await proxmox.nodes(node).qemu.post(
                    vmid=config["vmid"],
                    name=config["name"],
                    memory=2048,
                    cores=config["cores"],
                    virtio0="local:100",
                    boot="c",
                    net0="virtio,bridge=vmbr0",
                )
                print(f"    ✓ Created {config['name']} (ID: {config['vmid']})")
                created += 1

            except Exception as e:
                print(f"    ✗ Failed to create {config['name']}: {e}")
                failed += 1

        print(f"\n    Summary: {created} created, {failed} failed")


async def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Proxmox SDK: Creating Virtual Machines")
    print("=" * 60)

    # Get first available node
    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        if nodes:
            node = nodes[0]["node"]
            print(f"\nUsing node: {node}")

            # Run examples
            await create_minimal_vm(node)
            await create_standard_vm(node)
            await create_cloud_init_vm(node)
            await create_multi_disk_vm(node)
            await create_multi_network_vm(node)
            await batch_create_vms(node)

    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
