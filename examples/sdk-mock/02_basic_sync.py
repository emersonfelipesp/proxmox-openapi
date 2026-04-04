#!/usr/bin/env python3
"""Example 2: SDK Mock Usage (Sync / Blocking)

Demonstrates:
- Creating a mock SDK instance with sync wrapper
- No async/await required
- Same API as async version but blocks
"""

from proxmox_openapi.sdk import ProxmoxSDK


def main() -> None:
    """Run example."""
    print("=" * 60)
    print("Example 2: Basic Mock SDK Usage (Sync)")
    print("=" * 60)

    # Create a mock SDK instance with sync wrapper
    with ProxmoxSDK.sync_mock() as proxmox:
        print("\n[1] Listing nodes...")
        nodes = proxmox.nodes.get()
        print(f"    Found {len(nodes)} node(s)")
        for node in nodes:
            print(f"      - {node.get('node')}: {node.get('status')}")

        print("\n[2] Creating a VM...")
        vm = proxmox.nodes("pve").qemu.post(
            vmid=101,
            name="sync-example-vm",
            memory=4096,
            cores=4,
        )
        print(f"    Created: VM {vm.get('vmid')} ({vm.get('name')})")

        print("\n[3] Retrieving the VM list...")
        vm_list = proxmox.nodes("pve").qemu.get()
        print(f"    Found {len(vm_list)} VM(s) in mock data")

        print("\n[4] Updating the VM...")
        updated = (
            proxmox.nodes("pve")
            .qemu(101)
            .put(
                name="sync-example-vm-updated",
                memory=8192,
            )
        )
        print(f"    Updated: {updated}")

        print("\n[5] Deleting the VM...")
        result = proxmox.nodes("pve").qemu(101).delete()
        print(f"    Deleted: {result}")

    print("\n" + "=" * 60)
    print("✅ Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
