#!/usr/bin/env python3
"""Example 4: Testing with Mock SDK

Demonstrates:
- Using mock SDK in unit tests
- Testing API responses
- Testing error conditions
"""

import asyncio

from proxmox_openapi.sdk import ProxmoxSDK


async def test_node_listing() -> None:
    """Test listing nodes."""
    print("\n[TEST 1] Node Listing")
    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        assert isinstance(nodes, list), "Nodes should be a list"
        assert len(nodes) > 0, "Should have at least one node"
        assert nodes[0].get("node"), "Node should have 'node' field"
        print("    ✓ PASS: Nodes listing works correctly")


async def test_vm_creation_and_retrieval() -> None:
    """Test creating and retrieving a VM."""
    print("\n[TEST 2] VM Creation and Retrieval")
    async with ProxmoxSDK.mock() as proxmox:
        # Create
        created = await proxmox.nodes("pve").qemu.post(
            vmid=300,
            name="test-vm",
            memory=2048,
            cores=2,
        )
        assert created.get("vmid") == 300, "Created VM should have correct vmid"
        assert created.get("name") == "test-vm", "Created VM should have correct name"

        # Retrieve list
        retrieved_list = await proxmox.nodes("pve").qemu.get()
        assert retrieved_list is not None, "Retrieved result should not be None"
        print("    ✓ PASS: VM creation and retrieval works correctly")


async def test_vm_update() -> None:
    """Test updating a VM."""
    print("\n[TEST 3] VM Update")
    async with ProxmoxSDK.mock() as proxmox:
        # Create
        await proxmox.nodes("pve").qemu.post(vmid=301, name="update-test")

        # Update (mock returns None for updates)
        await (
            proxmox.nodes("pve")
            .qemu(301)
            .put(
                name="updated-name",
                memory=4096,
            )
        )
        print("    ✓ PASS: VM update works correctly")


async def test_vm_deletion() -> None:
    """Test deleting a VM."""
    print("\n[TEST 4] VM Deletion")
    async with ProxmoxSDK.mock() as proxmox:
        # Create
        await proxmox.nodes("pve").qemu.post(vmid=302, name="delete-test")

        # Verify creation (by listing)
        vms = await proxmox.nodes("pve").qemu.get()
        assert vms is not None, "VM list should exist"

        # Delete
        await proxmox.nodes("pve").qemu(302).delete()
        print("    ✓ PASS: VM deletion works correctly")


async def main() -> None:
    """Run all tests."""
    print("=" * 60)
    print("Example 4: Testing with Mock SDK")
    print("=" * 60)

    try:
        await test_node_listing()
        await test_vm_creation_and_retrieval()
        await test_vm_update()
        await test_vm_deletion()

        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
