# Virtual Machines: Getting Started Guide

Complete HOW-TO guide for managing Proxmox VMs using the SDK — from listing and retrieving VM details to creating and configuring new virtual machines.

---

## Overview

Proxmox manages two types of VMs:

| Type | CLI Name | Use Case |
|------|----------|----------|
| **QEMU/KVM** | `qemu` | Full virtualization (Linux, Windows, etc.) |
| **LXC Containers** | `lxc` | Lightweight OS containers |

This guide focuses on **QEMU VMs**. LXC containers work similarly.

---

## Session Setup

All examples use this basic session setup. Adjust credentials as needed:

=== "Async (Recommended)"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK
    
    async def main():
        async with ProxmoxSDK(
            host="pve.example.com",
            user="automation@pve",
            token_name="api-token",
            token_value="12345678-abcd-1234-abcd-1234567890ab",
        ) as proxmox:
            # Your code here
            pass
    
    asyncio.run(main())
    ```

=== "Sync (Blocking)"

    ```python
    from proxmox_openapi import ProxmoxSDK
    
    with ProxmoxSDK.sync(
        host="pve.example.com",
        user="automation@pve",
        token_name="api-token",
        token_value="12345678-abcd-1234-abcd-1234567890ab",
    ) as proxmox:
        # Your code here (blocking calls)
        pass
    ```

All examples below assume you have a `proxmox` connection object. Replace `host`, `user`, `token_name`, and `token_value` with your actual credentials.

---

## Getting VM Information

### List All Nodes

Before working with VMs, you need to know which node(s) to use:

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        nodes = await proxmox.nodes.get()
        for node in nodes:
            print(f"Node: {node['node']} ({node['status']})")
            # Output:
            # Node: pve1 (online)
            # Node: pve2 (online)
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        nodes = proxmox.nodes.get()
        for node in nodes:
            print(f"Node: {node['node']} ({node['status']})")
    ```

### List All VMs on a Node

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        vms = await proxmox.nodes("pve1").qemu.get()
        for vm in vms:
            print(f"VMID: {vm['vmid']}, Name: {vm['name']}, Status: {vm['status']}")
            # Output example:
            # VMID: 100, Name: web-server, Status: running
            # VMID: 101, Name: db-server, Status: stopped
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        vms = proxmox.nodes("pve1").qemu.get()
        for vm in vms:
            print(f"VMID: {vm['vmid']}, Name: {vm['name']}, Status: {vm['status']}")
    ```

### Get Detailed VM Configuration

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        # Get current VM config
        config = await proxmox.nodes("pve1").qemu(100).config.get()
        
        print(f"Name: {config['name']}")
        print(f"Memory: {config['memory']} MB")
        print(f"Cores: {config['cores']}")
        print(f"Boot: {config.get('boot', 'c')}")
        print(f"Network: {config.get('net0', 'Not configured')}")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        config = proxmox.nodes("pve1").qemu(100).config.get()
        print(f"Memory: {config['memory']} MB")
    ```

### Get VM Status

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        status = await proxmox.nodes("pve1").qemu(100).status.current.get()
        
        print(f"Status: {status['status']}")  # running, stopped, paused
        print(f"CPU: {status['cpu']:.2%}")
        print(f"Memory: {status['maxmem'] / 1024 / 1024:.2f} GB")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        status = proxmox.nodes("pve1").qemu(100).status.current.get()
        print(f"Status: {status['status']}")
    ```

### Filter Running VMs

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        vms = await proxmox.nodes("pve1").qemu.get()
        
        running_vms = [vm for vm in vms if vm['status'] == 'running']
        
        for vm in running_vms:
            print(f"Running VM: {vm['name']} (ID: {vm['vmid']})")
    ```

### Search VM by Name

=== "Async"

    ```python
    async def find_vm_by_name(proxmox, node, name):
        vms = await proxmox.nodes(node).qemu.get()
        for vm in vms:
            if vm['name'] == name:
                return vm
        return None
    
    async with ProxmoxSDK(...) as proxmox:
        vm = await find_vm_by_name(proxmox, "pve1", "web-server")
        if vm:
            print(f"Found: {vm['name']} (ID: {vm['vmid']})")
        else:
            print("VM not found")
    ```

---

## Creating Virtual Machines

### Minimal VM Creation

Create the simplest possible VM (1 core, 512MB RAM):

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        result = await proxmox.nodes("pve1").qemu.post(
            vmid=100,
            name="my-vm",
            memory=512,
            cores=1,
        )
        
        print(f"Task ID: {result['upid']}")
        # Output: Task ID: UPID:pve1:00001234:...
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        result = proxmox.nodes("pve1").qemu.post(
            vmid=100,
            name="my-vm",
            memory=512,
            cores=1,
        )
    ```

### Standard VM Creation (Recommended)

Create a more complete VM with customization:

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        result = await proxmox.nodes("pve1").qemu.post(
            vmid=101,
            name="web-server",
            
            # Hardware
            memory=2048,          # 2GB RAM
            cores=2,              # 2 CPU cores
            sockets=1,            # 1 socket (affects licensing)
            
            # Disk
            virtio0="local:60",   # 60GB disk on local storage
            
            # Boot and installation
            boot="c",             # Boot from disk (c: disk, n: network, d: cdrom)
            cdrom="local:iso/ubuntu-22.04-live.iso",
            
            # Network
            net0="virtio,bridge=vmbr0",
            
            # Other options
            bios="seabios",       # seabios or ovmf (UEFI)
            machine="q35",        # Machine type (i440fx or q35)
            description="Web server VM",
        )
        
        print(f"VM created with task: {result['upid']}")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        result = proxmox.nodes("pve1").qemu.post(
            vmid=101,
            name="web-server",
            memory=2048,
            cores=2,
            virtio0="local:60",
            boot="c",
            net0="virtio,bridge=vmbr0",
        )
    ```

### VM Creation with Cloud-Init

Create a VM with cloud-init support (for automated OS provisioning):

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        result = await proxmox.nodes("pve1").qemu.post(
            vmid=102,
            name="cloud-vm",
            
            # Hardware (suitable for cloud-init)
            memory=1024,
            cores=2,
            cores=2,
            agent=1,              # Enable QEMU guest agent
            
            # Storage
            scsi0="local:50",     # Cloud-init compatible disk
            
            # Cloud-init
            ide2="local:cloudinit",
            
            # Boot
            boot="order=scsi0;ide2",
            
            # Network  
            net0="virtio,bridge=vmbr0",
            
            # Cloud-init config
            citype="nocloud",
            ciuser="ubuntu",
            cipassword="mypassword",
            sshkeys="ssh-rsa AAAAB3Nza...",  # Your SSH public key
        )
        
        print(f"Cloud-init VM created: {result['upid']}")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        result = proxmox.nodes("pve1").qemu.post(
            vmid=102,
            name="cloud-vm",
            memory=1024,
            cores=2,
            agent=1,
            scsi0="local:50",
            ide2="local:cloudinit",
            citype="nocloud",
            ciuser="ubuntu",
        )
    ```

### VM Creation with Multiple Disks

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        result = await proxmox.nodes("pve1").qemu.post(
            vmid=103,
            name="data-vm",
            
            # Primary OS disk
            virtio0="local:100",
            
            # Data disks
            virtio1="local-lvm:100",  # Second disk from different storage
            virtio2="ceph-pool:200",  # Third disk from Ceph (if available)
            
            # Other config
            memory=4096,
            cores=4,
            boot="c",
            net0="virtio,bridge=vmbr0",
        )
    ```

### VM Creation with Multiple Network Interfaces

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        result = await proxmox.nodes("pve1").qemu.post(
            vmid=104,
            name="multi-net",
            
            # Hardware
            memory=2048,
            cores=2,
            virtio0="local:50",
            
            # Multiple networks
            net0="virtio,bridge=vmbr0",       # Management network
            net1="virtio,bridge=vmbr1",       # Data network
            net2="virtio,bridge=vmbr2",       # Storage network
            
            boot="c",
        )
    ```

---

## Handling Task Results

VM creation and many other operations return a **Task ID** because they run asynchronously. Monitor task progress:

=== "Async"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks
    
    async with ProxmoxSDK(...) as proxmox:
        # Create VM (returns task)
        result = await proxmox.nodes("pve1").qemu.post(
            vmid=100,
            name="my-vm",
            memory=2048,
            cores=2,
            virtio0="local:60",
        )
        
        task_id = result.get("upid")
        if task_id:
            # Wait for task completion
            tasks = Tasks(proxmox)
            
            print(f"Waiting for task {task_id}...")
            status = await tasks.wait_task(task_id, timeout=300)
            
            if status:
                print(f"✓ Task completed: {status}")
            else:
                print("✗ Task failed or timed out")
    ```

=== "Sync"

    ```python
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks
    import time
    
    with ProxmoxSDK.sync(...) as proxmox:
        result = proxmox.nodes("pve1").qemu.post(
            vmid=100,
            name="my-vm",
            memory=2048,
            cores=2,
            virtio0="local:60",
        )
        
        task_id = result.get("upid")
        if task_id:
            tasks = Tasks(proxmox)
            # Wait synchronously
            status = tasks.wait_task(task_id, timeout=300)
            print(f"Task completed: {status}")
    ```

---

## Modifying VMs

### Update VM Configuration

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        # Update memory and cores on a stopped VM
        result = await proxmox.nodes("pve1").qemu(100).config.put(
            memory=4096,  # Increase to 4GB
            cores=4,      # Increase to 4 cores
            description="Updated configuration",
        )
        
        print("VM configuration updated")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(...) as proxmox:
        proxmox.nodes("pve1").qemu(100).config.put(
            memory=4096,
            cores=4,
        )
    ```

### Partial Update (PATCH)

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        # Only update specific fields
        await proxmox.nodes("pve1").qemu(100).config.patch(
            memory=8192,
        )
    ```

### Resize Disk (while VM is running on some configs)

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        # Resize virtio0 disk to 100GB
        result = await proxmox.nodes("pve1").qemu(100).resize.post(
            disk="virtio0",
            size="+40G",  # Add 40GB (if already 60GB → 100GB)
        )
        
        print(f"Resize task: {result.get('upid')}")
    ```

---

## VM Power Control

### Start VM

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        result = await proxmox.nodes("pve1").qemu(100).status.start.post()
        print(f"Start task: {result.get('upid')}")
    ```

### Stop VM (clean shutdown)

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        # Clean shutdown
        result = await proxmox.nodes("pve1").qemu(100).status.shutdown.post()
        print("Shutdown initiated")
    ```

### Force Stop VM (immediate power off)

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        # Immediate power off (like pulling plug)
        result = await proxmox.nodes("pve1").qemu(100).status.stop.post()
        print("VM forcefully stopped")
    ```

### Reboot VM

=== "Async"

    ```python
    async with ProxmoxSDK(...) as proxmox:
        result = await proxmox.nodes("pve1").qemu(100).status.reboot.post()
        print("Reboot initiated")
    ```

---

## Real-World Examples

### Example 1: Batch Create VMs

=== "Async"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks
    
    async def create_vms_batch():
        """Create multiple VMs in parallel."""
        async with ProxmoxSDK(
            host="pve.example.com",
            user="automation@pve",
            token_name="api-token",
            token_value="...",
        ) as proxmox:
            vms_to_create = [
                {"vmid": 200, "name": "web-01", "cores": 2},
                {"vmid": 201, "name": "web-02", "cores": 2},
                {"vmid": 202, "name": "app-01", "cores": 4},
            ]
            
            tasks = []
            for vm_config in vms_to_create:
                vmid = vm_config["vmid"]
                
                result = await proxmox.nodes("pve1").qemu.post(
                    vmid=vmid,
                    name=vm_config["name"],
                    memory=2048,
                    cores=vm_config["cores"],
                    virtio0="local:100",
                    boot="c",
                    net0="virtio,bridge=vmbr0",
                )
                
                task_id = result.get("upid")
                tasks.append((vmid, task_id))
                print(f"Creating {vm_config['name']} (ID: {vmid})...")
            
            # Wait for all tasks
            tasks_tool = Tasks(proxmox)
            for vmid, task_id in tasks:
                await tasks_tool.wait_task(task_id)
                print(f"✓ VM {vmid} created")
    
    asyncio.run(create_vms_batch())
    ```

### Example 2: VM Lifecycle Management

=== "Async"

    ```python
    from proxmox_openapi import ProxmoxSDK
    import asyncio
    
    async def vm_lifecycle_demo():
        """Demonstrate full VM lifecycle."""
        async with ProxmoxSDK(...) as proxmox:
            vmid = 300
            node = "pve1"
            
            # 1. CREATE
            print("[1/5] Creating VM...")
            await proxmox.nodes(node).qemu.post(
                vmid=vmid,
                name="lifecycle-demo",
                memory=2048,
                cores=2,
                virtio0="local:50",
                boot="c",
                net0="virtio,bridge=vmbr0",
            )
            await asyncio.sleep(2)
            
            # 2. START
            print("[2/5] Starting VM...")
            await proxmox.nodes(node).qemu(vmid).status.start.post()
            await asyncio.sleep(3)
            
            # 3. CHECK STATUS
            print("[3/5] Checking status...")
            status = await proxmox.nodes(node).qemu(vmid).status.current.get()
            print(f"  Status: {status['status']}")
            
            # 4. MODIFY
            print("[4/5] Updating configuration...")
            # Note: Some changes require VM to be stopped
            # await proxmox.nodes(node).qemu(vmid).status.shutdown.post()
            # await asyncio.sleep(2)
            # await proxmox.nodes(node).qemu(vmid).config.put(memory=4096)
            
            # 5. DELETE
            print("[5/5] Deleting VM...")
            await proxmox.nodes(node).qemu(vmid).delete()
            print("✓ VM lifecycle complete")
    
    asyncio.run(vm_lifecycle_demo())
    ```

### Example 3: Inventory Report

=== "Async"

    ```python
    from proxmox_openapi import ProxmoxSDK
    import asyncio
    
    async def generate_inventory_report():
        """Generate an inventory report of all VMs."""
        async with ProxmoxSDK(...) as proxmox:
            nodes = await proxmox.nodes.get()
            
            print("\n" + "="*60)
            print("PROXMOX INVENTORY REPORT")
            print("="*60 + "\n")
            
            total_vms = 0
            total_memory = 0
            total_cores = 0
            
            for node_info in nodes:
                node = node_info["node"]
                vms = await proxmox.nodes(node).qemu.get()
                
                print(f"\nNode: {node} ({node_info['status']})")
                print("-" * 60)
                print(f"{'VMID':<8} {'Name':<20} {'Status':<10} {'Memory':<10} {'Cores':<6}")
                print("-" * 60)
                
                for vm in vms:
                    config = await proxmox.nodes(node).qemu(vm['vmid']).config.get()
                    memory_gb = config['memory'] / 1024
                    
                    print(f"{vm['vmid']:<8} {vm['name']:<20} {vm['status']:<10} "
                          f"{memory_gb:<10.1f} {config['cores']:<6}")
                    
                    total_vms += 1
                    total_memory += config['memory']
                    total_cores += config['cores']
            
            print("\n" + "="*60)
            print(f"Total: {total_vms} VMs | Memory: {total_memory/1024:.1f}GB | Cores: {total_cores}")
            print("="*60 + "\n")
    
    asyncio.run(generate_inventory_report())
    ```

---

## Common Parameters Reference

### VM Creation Parameters

| Parameter | Type | Example | Notes |
|-----------|------|---------|-------|
| `vmid` | int | `100` | Unique VM ID (1-999) |
| `name` | str | `"web-server"` | VM hostname |
| `memory` | int | `2048` | RAM in MB |
| `cores` | int | `2` | CPU cores |
| `sockets` | int | `1` | CPU sockets |
| `virtio0-9` | str | `"local:60"` | Virtual disks |
| `scsi0-30` | str | `"local:100"` | SCSI disks |
| `net0-5` | str | `"virtio,bridge=..."` | Network interfaces |
| `boot` | str | `"c"` | Boot order (c: disk, n: network, d: cdrom) |
| `bios` | str | `"seabios"` |BIOS or UEFI |
| `description` | str | `"Production web server"` | Notes |
| `agent` | int | `1` | Enable QEMU agent |
| `cdrom` | str | `"local:iso/..."` | CD-ROM image |

### Disk Storage Formats

- `local:50` — 50GB on local storage
- `local-lvm:100` — 100GB on local LVM
- `ceph-pool:200` — 200GB on Ceph (if configured)

---

## Troubleshooting

### "Permission denied" Errors

Ensure your API token has sufficient permissions:

```python
# In Proxmox UI, API tokens need at least:
# - Permissions: Proxmox "Administrator" or specific VM permissions
```

### "VMID already exists"

Use a unique VMID that doesn't exist:

```python
# Check existing VMIDs first
async with ProxmoxSDK(...) as proxmox:
    vms = await proxmox.nodes("pve1").qemu.get()
    existing_ids = [vm['vmid'] for vm in vms]
    print(f"In use: {existing_ids}")
    
    # Pick next available
    new_vmid = max(existing_ids) + 1 if existing_ids else 100
```

### Disk Space Issues

Check available storage:

```python
async with ProxmoxSDK(...) as proxmox:
    storage = await proxmox.storage.get()
    for store in storage:
        print(f"{store['storage']}: "
              f"{store.get('used', 0)} / {store.get('content', 0)} bytes")
```

---

## See Also

- [SDK Guide](./sdk-guide.md) — General SDK usage patterns
- [Authentication Guide](./sdk-authentication.md) — Setting up credentials
- [Advanced Examples](./sdk-examples.md) — Backups, clustering, monitoring
- [API Reference](./api-reference.md) — Complete endpoint documentation
