#!/usr/bin/env python3
"""Example 8: PBS (Proxmox Backup Server) Mock SDK

Demonstrates:
- Using PBSSDK convenience class for PBS-specific mock operations
- Async and sync usage patterns
- CRUD operations against PBS endpoints
- Direct ProxmoxSDK.mock(service="PBS") alternative
"""

import asyncio

from proxmox_openapi.sdk import ProxmoxSDK
from proxmox_openapi.sdk.pbs import PBSSDK


async def async_example() -> None:
    """Async PBS mock usage via PBSSDK."""
    print("\n[PBSSDK Async Mock]")

    async with PBSSDK.mock() as pbs:
        print("\n  [1] Access index (authentication endpoints)...")
        access = await pbs.access.get()
        print(f"      access: {access}")

        print("\n  [2] List datastores...")
        stores = await pbs.admin.datastore.get()
        print(f"      stores: {stores}")

        print("\n  [3] Create a datastore...")
        created = await pbs.admin.datastore.post(
            name="backup-store",
            path="/mnt/backup",
        )
        print(f"      created: {created}")

        print("\n  [4] List users...")
        users = await pbs.access.users.get()
        print(f"      users: {users}")

        print("\n  [5] Get node info...")
        nodes = await pbs.nodes.get()
        print(f"      nodes: {nodes}")


def sync_example() -> None:
    """Sync PBS mock usage via PBSSDK."""
    print("\n[PBSSDK Sync Mock]")

    with PBSSDK.sync_mock() as pbs:
        print("\n  [1] List datastores (sync)...")
        stores = pbs.admin.datastore.get()
        print(f"      stores: {stores}")

        print("\n  [2] Create then fetch a datastore...")
        pbs.admin.datastore.post(name="sync-store", path="/mnt/sync")
        fetched = pbs.admin.datastore.get()
        print(f"      after create: {fetched}")

        print("\n  [3] Delete a datastore...")
        result = pbs.admin.datastore("sync-store").delete()
        print(f"      deleted: {result}")


def generic_sdk_example() -> None:
    """Alternative: use ProxmoxSDK.mock(service='PBS') directly."""
    print("\n[ProxmoxSDK.mock(service='PBS')]")

    with ProxmoxSDK.sync_mock(service="PBS") as pbs:
        stores = pbs.admin.datastore.get()
        print(f"      datastores: {stores}")
        access = pbs.access.get()
        print(f"      access: {access}")


def main() -> None:
    print("=" * 60)
    print("Example 8: PBS Mock SDK")
    print("=" * 60)

    asyncio.run(async_example())
    sync_example()
    generic_sdk_example()

    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
