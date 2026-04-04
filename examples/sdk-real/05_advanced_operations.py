#!/usr/bin/env python3
"""Example 5: Advanced Operations

Demonstrates:
- Listing storage
- VM backups
- Snapshots
- Monitoring resources
- Task tracking
- Error handling with retries

This example uses the mock backend by default.
"""

import asyncio
from proxmox_openapi import ProxmoxSDK


async def list_storage() -> None:
    """List available storage pools."""
    print("\n[1] Listing storage pools...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            storage = await proxmox.storage.get(enabled=1)
            print(f"    Available storage: {len(storage)} pool(s)")
            for store in storage:
                content_types = store.get('content', '').split(',')
                enabled = "✓" if store.get('enabled') else "✗"
                print(f"      [{enabled}] {store['storage']:20} Type: {store['type']:10} "
                      f"Content: {','.join(content_types[:2])}")
        except Exception as e:
            print(f"    ✗ Error: {e}")


async def create_backup(node: str, vmid: int) -> None:
    """Create a backup of a VM."""
    print(f"\n[2] Creating backup of VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            result = await proxmox.nodes(node).qemu(vmid).backup.post(
                storage="local",
                mode="snapshot",
                compress="zstd",
                notes="API backup",
            )

            print(f"    ✓ Backup initiated")
            if result.get('upid'):
                print(f"      Task ID: {result['upid']}")
                print(f"      Storage: local")
                print(f"      Compression: zstd")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def create_snapshot(node: str, vmid: int) -> None:
    """Create a snapshot of a VM."""
    print(f"\n[3] Creating snapshot of VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            snapshot_name = "pre-update-snapshot"
            result = await proxmox.nodes(node).qemu(vmid).snapshot.post(
                snapname=snapshot_name,
                description="Pre-update snapshot",
                vmstate=1,  # Include memory state
            )

            print(f"    ✓ Snapshot created")
            print(f"      Name: {snapshot_name}")
            print(f"      Include VM State: yes")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def list_snapshots(node: str, vmid: int) -> None:
    """List all snapshots of a VM."""
    print(f"\n[4] Listing snapshots for VM {vmid}...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            snapshots = await proxmox.nodes(node).qemu(vmid).snapshot.get()
            print(f"    Found {len(snapshots)} snapshot(s)")
            for snapshot in snapshots:
                print(f"      • {snapshot.get('name')}")
                if snapshot.get('description'):
                    print(f"        Description: {snapshot['description']}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def monitor_node_resources(node: str) -> None:
    """Monitor node resource usage."""
    print(f"\n[5] Monitoring node '{node}' resources...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            status = await proxmox.nodes(node).status.get()

            print(f"    Node Status:")
            print(f"      Status:        {status.get('status', 'unknown')}")
            print(f"      Uptime:        {status.get('uptime', 0) / 3600 / 24:.1f} days")
            print(f"      CPU:           {status.get('cpu', 0):.1%}")
            print(f"      Memory Used:   {status.get('memory', 0) / 1024 / 1024 / 1024:.2f} GB "
                  f"/ {status.get('maxmem', 0) / 1024 / 1024 / 1024:.2f} GB")
            print(f"      Disk Used:     {status.get('disk', 0) / 1024 / 1024 / 1024:.2f} GB "
                  f"/ {status.get('maxdisk', 0) / 1024 / 1024 / 1024:.2f} GB")

            load = status.get('loadavg', [0, 0, 0])
            print(f"      Load Average:  {load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def get_cluster_info() -> None:
    """Get cluster information."""
    print("\n[6] Getting cluster information...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            cluster_status = await proxmox.cluster.status.get()

            nodes = [c for c in cluster_status if c.get('type') == 'node']
            print(f"    Cluster Nodes: {len(nodes)}")
            for node in nodes:
                status = "online" if node.get('online') else "offline"
                print(f"      • {node['name']:15} {status:10} IP: {node.get('ip', 'N/A')}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def find_resource_heavy_vms(node: str) -> None:
    """Find VMs using most resources."""
    print(f"\n[7] Finding resource-heavy VMs on '{node}'...")
    async with ProxmoxSDK.mock() as proxmox:
        try:
            vms = await proxmox.nodes(node).qemu.get()

            vm_resources = []
            for vm in vms:
                config = await proxmox.nodes(node).qemu(vm['vmid']).config.get()
                vm_resources.append({
                    'name': vm['name'],
                    'vmid': vm['vmid'],
                    'memory_gb': config.get('memory', 0) / 1024,
                    'cores': config.get('cores', 0),
                })

            # Sort by memory
            vm_resources.sort(key=lambda x: x['memory_gb'], reverse=True)

            print(f"    Top resource-consuming VMs:")
            print(f"      {'Name':<20} {'Memory (GB)':<12} {'Cores':<8}")
            print(f"      {'-'*40}")
            for vm in vm_resources[:5]:
                print(f"      {vm['name']:<20} {vm['memory_gb']:>10.1f}  {vm['cores']:>6}")

        except Exception as e:
            print(f"    ✗ Error: {e}")


async def create_vm_with_retry(node: str, max_retries: int = 3) -> None:
    """Create a VM with retry logic on failure."""
    print(f"\n[8] Creating VM with retry logic...")

    for attempt in range(1, max_retries + 1):
        try:
            async with ProxmoxSDK.mock() as proxmox:
                result = await proxmox.nodes(node).qemu.post(
                    vmid=999,
                    name="retry-test-vm",
                    memory=1024,
                    cores=1,
                )

                print(f"    ✓ VM created on attempt {attempt}")
                return

        except Exception as e:
            if attempt < max_retries:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"    ✗ Attempt {attempt} failed: {str(e)[:50]}...")
                print(f"      Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
            else:
                print(f"    ✗ Failed after {max_retries} attempts")


async def main() -> None:
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Proxmox SDK: Advanced Operations")
    print("=" * 60)

    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        if nodes:
            node = nodes[0]['node']
            vms = await proxmox.nodes(node).qemu.get()

            print(f"\nUsing node: {node}")

            # Run examples
            await list_storage()
            await get_cluster_info()
            await monitor_node_resources(node)

            if vms:
                vmid = vms[0]['vmid']
                print(f"Using VM: {vms[0]['name']} (ID: {vmid})")

                await create_backup(node, vmid)
                await create_snapshot(node, vmid)
                await list_snapshots(node, vmid)
                await find_resource_heavy_vms(node)

            await create_vm_with_retry(node)

    print("\n" + "=" * 60)
    print("✅ Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
