# SDK Examples: Common Operations

Real-world examples for common Proxmox operations including backups, clustering, and monitoring.

---

## Backup & Snapshot Operations

### List Backup Storage

=== "Async"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK

    async def list_backup_storage():
        async with ProxmoxSDK(...) as proxmox:
            storage = await proxmox.storage.get(enabled=1)

            for store in storage:
                if "backup" in store.get("content", "").split(","):
                    print(f"Storage: {store['storage']}")
                    print(f"  Type: {store['type']}")
                    print(f"  Path: {store.get('path', 'N/A')}")
                    print()

    asyncio.run(list_backup_storage())
    ```

### Create a VM Backup

=== "Async"

    ```python
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks

    async def backup_vm(node, vmid, storage="local"):
        async with ProxmoxSDK(...) as proxmox:
            print(f"Starting backup of VM {vmid}...")

            result = await proxmox.nodes(node).qemu(vmid).backup.post(
                storage=storage,
                mode="snapshot",  # snapshot, stop, or suspend
                compress="zstd",  # zstd, gzip, lz4
                notes="Daily backup",
            )

            task_id = result.get("upid")
            if task_id:
                tasks = Tasks(proxmox)
                status = await tasks.wait_task(task_id, timeout=3600)
                print(f"✓ Backup completed: {status}")
            else:
                print(f"✗ Backup failed: {result}")
    ```

### List VM Snapshots

=== "Async"

    ```python
    async def list_vm_snapshots(node, vmid):
        async with ProxmoxSDK(...) as proxmox:
            snapshots = await proxmox.nodes(node).qemu(vmid).snapshot.get()

            for snapshot in snapshots:
                print(f"Snapshot: {snapshot['name']}")
                print(f"  Created: {snapshot.get('snaptime', 'N/A')}")
                print(f"  Description: {snapshot.get('description', 'N/A')}")
    ```

### Create VM Snapshot

=== "Async"

    ```python
    async def snapshot_vm(node, vmid, snapshot_name):
        async with ProxmoxSDK(...) as proxmox:
            result = await proxmox.nodes(node).qemu(vmid).snapshot.post(
                snapname=snapshot_name,
                description="Daily snapshot",
                vmstate=1,  # Include memory state
            )

            print(f"Snapshot created: {snapshot_name}")
    ```

### Restore from Backup

=== "Async"

    ```python
    async def restore_backup(node, storage, backup_file):
        """Restore a backup to create a new VM."""
        async with ProxmoxSDK(...) as proxmox:
            # List available backups
            backups = await proxmox.nodes(node).storage(storage).content.get()

            print("Available backups:")
            for backup in backups:
                if backup['content'] == 'backup':
                    print(f"  {backup['volid']}")
    ```

---

## Node & Cluster Operations

### List Cluster Information

=== "Async"

    ```python
    async def show_cluster_info():
        async with ProxmoxSDK(...) as proxmox:
            # Cluster status
            cluster_status = await proxmox.cluster.status.get()

            print("Cluster Status:")
            for node in cluster_status:
                if node.get('type') == 'node':
                    print(f"  {node['name']}: {node['status']}")
                    print(f"    IP: {node.get('ip', 'N/A')}")
                    print(f"    Offline: {node.get('online', False)}")
    ```

### Node Resource Monitoring

=== "Async"

    ```python
    async def monitor_node_resources(node):
        async with ProxmoxSDK(...) as proxmox:
            status = await proxmox.nodes(node).status.get()

            print(f"\nNode: {node}")
            print(f"  Status: {status.get('status', 'unknown')}")
            print(f"  Uptime: {status.get('uptime', 0) / 3600:.1f} hours")
            print(f"  CPU: {status.get('cpu', 0):.1%}")
            print(f"  Memory: {status.get('memory', 0)} / {status.get('maxmem', 0)} bytes")
            print(f"  Disk: {status.get('disk', 0)} / {status.get('maxdisk', 0)} bytes")
            print(f"  Load: {status.get('loadavg', [0, 0, 0])}")
    ```

### Node Tasks

=== "Async"

    ```python
    async def list_node_tasks(node):
        async with ProxmoxSDK(...) as proxmox:
            tasks = await proxmox.nodes(node).tasks.get()

            print(f"\nRecent tasks on {node}:")
            for task in tasks[:5]:  # Last 5
                print(f"  {task['id']}: {task['type']}")
                print(f"    Status: {task.get('status', 'unknown')}")
                print(f"    Start: {task.get('starttime', 'N/A')}")
    ```

---

## Storage Operations

### List Storage

=== "Async"

    ```python
    async def list_all_storage():
        async with ProxmoxSDK(...) as proxmox:
            storage = await proxmox.storage.get()

            print("\nAvailable Storage:")
            for store in storage:
                if store.get('enabled'):
                    print(f"  {store['storage']} ({store['type']})")
                    print(f"    Content: {store.get('content', 'N/A')}")
                    print(f"    Used: {store.get('used', 0) / 1024 / 1024 / 1024:.2f} GB")
                    print(f"    Available: {store.get('avail', 0) / 1024 / 1024 / 1024:.2f} GB")
    ```

### Storage Content (ISOs, Backups, etc.)

=== "Async"

    ```python
    async def list_storage_content(storage):
        async with ProxmoxSDK(...) as proxmox:
            content = await proxmox.storage(storage).content.get()

            print(f"\n{storage} content:")
            for item in content:
                print(f"  {item['volid']}")
                print(f"    Type: {item['content']}")
                print(f"    Size: {item.get('size', 0) / 1024 / 1024 / 1024:.2f} GB")
    ```

---

## Network Operations

### List Network Interfaces

=== "Async"

    ```python
    async def list_network_interfaces(node):
        async with ProxmoxSDK(...) as proxmox:
            net = await proxmox.nodes(node).network.get()

            print(f"\nNetwork interfaces on {node}:")
            for interface in net:
                print(f"  {interface['iface']}")
                print(f"    Type: {interface.get('type', 'unknown')}")
                print(f"    Active: {interface.get('active', False)}")
                if interface.get('address'):
                    print(f"    Address: {interface['address']}")
                if interface.get('netmask'):
                    print(f"    Netmask: {interface['netmask']}")
    ```

### VM Network Configuration

=== "Async"

    ```python
    async def get_vm_network_config(node, vmid):
        async with ProxmoxSDK(...) as proxmox:
            config = await proxmox.nodes(node).qemu(vmid).config.get()

            print(f"\nVM {vmid} network config:")
            for i in range(10):
                net_key = f"net{i}"
                if net_key in config:
                    print(f"  {net_key}: {config[net_key]}")
    ```

---

## Firewall Rules

### List Firewall Rules

=== "Async"

    ```python
    async def list_firewall_rules():
        async with ProxmoxSDK(...) as proxmox:
            rules = await proxmox.cluster.firewall.rules.get()

            print("\nFirewall Rules:")
            for rule in rules:
                enabled = "✓" if rule.get('enable', 0) else "✗"
                print(f"  [{enabled}] {rule.get('rule', 'N/A')}")
    ```

### Create Firewall Rule

=== "Async"

    ```python
    async def add_firewall_rule():
        async with ProxmoxSDK(...) as proxmox:
            result = await proxmox.cluster.firewall.rules.post(
                rule="IN ACCEPT -p tcp -dport 443",
                enable=1,
                comment="Allow HTTPS inbound",
            )

            print("Firewall rule added")
    ```

---

## User & Permission Management

### List Users

=== "Async"

    ```python
    async def list_users():
        async with ProxmoxSDK(...) as proxmox:
            users = await proxmox.access.users.get()

            print("\nProxmox Users:")
            for user in users:
                print(f"  {user['userid']}")
                if user.get('comment'):
                    print(f"    {user['comment']}")
    ```

### List API Tokens

=== "Async"

    ```python
    async def list_api_tokens(user):
        async with ProxmoxSDK(...) as proxmox:
            tokens = await proxmox.access.users(user).tokens.get()

            print(f"\nAPI tokens for {user}:")
            for token in tokens:
                print(f"  {token['tokenid']}")
                if token.get('comment'):
                    print(f"    {token['comment']}")
    ```

### Update User Permissions

=== "Async"

    ```python
    async def grant_backup_permission(user):
        async with ProxmoxSDK(...) as proxmox:
            # Grant "Backup Operator" role to user
            result = await proxmox.access.acl.put(
                path="/storage",
                roles="PVEBackupOperator",
                users=user,
                propagate=1,
            )

            print(f"Permissions updated for {user}")
    ```

---

## Monitoring & Alerting

### Real-Time VM Monitoring

=== "Async"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK

    async def monitor_vm_health(node, vmid, interval=5, duration=60):
        """Monitor a VM's health for a duration."""
        async with ProxmoxSDK(...) as proxmox:
            print(f"Monitoring VM {vmid} for {duration}s (interval: {interval}s)")

            elapsed = 0
            while elapsed < duration:
                try:
                    status = await proxmox.nodes(node).qemu(vmid).status.current.get()

                    print(f"\n[{elapsed}s] {status['status'].upper()}")
                    print(f"  CPU: {status.get('cpu', 0):.1%}")
                    print(f"  Memory: {status.get('mem', 0) / 1024 / 1024:.0f} MB "
                          f"/ {status.get('maxmem', 0) / 1024 / 1024:.0f} MB")

                    # Alert if CPU high
                    if status.get('cpu', 0) > 0.8:
                        print("  ⚠ CPU high!")

                    await asyncio.sleep(interval)
                    elapsed += interval

                except Exception as e:
                    print(f"Error: {e}")
                    break
    ```

### Alert on VM Issues

=== "Async"

    ```python
    async def health_check_all_vms(alert_to_webhook):
        """Check health of all VMs and send alerts."""
        import aiohttp

        async with ProxmoxSDK(...) as proxmox:
            nodes = await proxmox.nodes.get()

            for node_info in nodes:
                node = node_info["node"]
                vms = await proxmox.nodes(node).qemu.get()

                for vm in vms:
                    try:
                        status = await proxmox.nodes(node).qemu(vm['vmid']).status.current.get()

                        # Check issues
                        if status['status'] == 'stopped':
                            alert = {
                                "alert_type": "VM_DOWN",
                                "vm_name": vm['name'],
                                "vmid": vm['vmid'],
                                "node": node,
                            }

                            async with aiohttp.ClientSession() as session:
                                await session.post(alert_to_webhook, json=alert)

                    except Exception as e:
                        print(f"Error checking {vm['name']}: {e}")
    ```

---

## Disaster Recovery

### List All VM Configurations

=== "Async"

    ```python
    import json
    from proxmox_openapi import ProxmoxSDK

    async def export_vm_configs():
        """Export all VM configs to JSON for disaster recovery."""
        async with ProxmoxSDK(...) as proxmox:
            backup = {
                "timestamp": __import__("datetime").datetime.now().isoformat(),
                "vms": {}
            }

            nodes = await proxmox.nodes.get()

            for node_info in nodes:
                node = node_info["node"]
                vms = await proxmox.nodes(node).qemu.get()

                for vm in vms:
                    config = await proxmox.nodes(node).qemu(vm['vmid']).config.get()
                    backup["vms"][str(vm['vmid'])] = {
                        "node": node,
                        "name": vm['name'],
                        "config": config
                    }

            # Save to file
            with open("vm-backup-configs.json", "w") as f:
                json.dump(backup, f, indent=2)

            print("✓ VM configs exported to vm-backup-configs.json")
    ```

### Quick VM Recovery

=== "Async"

    ```python
    import json
    from proxmox_openapi import ProxmoxSDK

    async def restore_vms_from_config(config_file):
        """Recreate VMs from saved configuration."""
        async with ProxmoxSDK(...) as proxmox:
            with open(config_file) as f:
                backup = json.load(f)

            for vmid, vm_data in backup["vms"].items():
                config = vm_data["config"]

                print(f"Restoring VM {vm_data['name']} (ID: {vmid})...")

                try:
                    # Recreate VM with original config
                    await proxmox.nodes(vm_data["node"]).qemu.post(
                        vmid=int(vmid),
                        name=vm_data["name"],
                        memory=config.get('memory', 2048),
                        cores=config.get('cores', 2),
                        **{k: v for k, v in config.items()
                           if k not in ['memory', 'cores', 'name', 'vmid']}
                    )
                    print(f"  ✓ {vm_data['name']} recreated")
                except Exception as e:
                    print(f"  ✗ Failed: {e}")
    ```

---

## Performance Tuning

### Find Heavy VMs

=== "Async"

    ```python
    async def find_heavy_resource_vms():
        """Find VMs consuming most resources."""
        async with ProxmoxSDK(...) as proxmox:
            nodes = await proxmox.nodes.get()
            vms_by_resource = []

            for node_info in nodes:
                node = node_info["node"]
                vms = await proxmox.nodes(node).qemu.get()

                for vm in vms:
                    config = await proxmox.nodes(node).qemu(vm['vmid']).config.get()

                    vms_by_resource.append({
                        "name": vm['name'],
                        "memory_gb": config.get('memory', 0) / 1024,
                        "cores": config.get('cores', 0),
                        "node": node,
                    })

            # Sort by memory
            vms_by_resource.sort(key=lambda x: x['memory_gb'], reverse=True)

            print("\nTop VMs by memory allocation:")
            for vm in vms_by_resource[:5]:
                print(f"  {vm['name']}: {vm['memory_gb']:.1f}GB, {vm['cores']} cores")
    ```

---

## Batch Operations

### Batch Start VMs

=== "Async"

    ```python
    async def batch_start_vms(node, vm_names):
        """Start multiple VMs."""
        async with ProxmoxSDK(...) as proxmox:
            vms = await proxmox.nodes(node).qemu.get()

            for vm_name in vm_names:
                vm = next((v for v in vms if v['name'] == vm_name), None)
                if vm:
                    print(f"Starting {vm_name}...")
                    await proxmox.nodes(node).qemu(vm['vmid']).status.start.post()
                else:
                    print(f"VM not found: {vm_name}")
    ```

### Batch Delete VMs

=== "Async"

    ```python
    async def batch_delete_vms(node, vm_ids, confirm=False):
        """Delete multiple VMs (dangerous!)."""
        if not confirm:
            print("This will DELETE VMs. Run with confirm=True to proceed.")
            return

        async with ProxmoxSDK(...) as proxmox:
            for vmid in vm_ids:
                print(f"Deleting VM {vmid}...")
                try:
                    await proxmox.nodes(node).qemu(vmid).delete()
                    print(f"  ✓ Deleted")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
    ```

---

## Error Handling & Retries

### Robust Operation with Retries

=== "Async"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK, ResourceException

    async def create_vm_with_retries(node, vmid, name, max_retries=3):
        """Create VM with automatic retry on failure."""

        for attempt in range(1, max_retries + 1):
            try:
                async with ProxmoxSDK(...) as proxmox:
                    result = await proxmox.nodes(node).qemu.post(
                        vmid=vmid,
                        name=name,
                        memory=2048,
                        cores=2,
                        virtio0="local:50",
                    )
                    print(f"✓ VM created on attempt {attempt}")
                    return result

            except ResourceException as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"✗ Attempt {attempt} failed: {e.status_message}")
                    print(f"  Retrying in {wait_time}s...")
                    await asyncio.sleep(wait_time)
                else:
                    print(f"✗ Failed after {max_retries} attempts")
                    raise
    ```

---

## See Also

- [SDK Guide](./sdk-guide.md) — Overview and core concepts
- [Authentication Guide](./sdk-authentication.md) — Credential setup
- [Virtual Machines Guide](./sdk-virtual-machines.md) — VM management
- [API Reference](./api-reference.md) — Complete endpoint list
