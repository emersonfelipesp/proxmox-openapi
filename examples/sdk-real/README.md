# SDK Real-World Examples

Production-ready examples for the Proxmox OpenAPI SDK.

Here you'll find practical examples for real-world use cases:

## Examples

1. **[01_authentication.py](01_authentication.py)** - Session setup and credential management
   - API token authentication
   - Password authentication
   - SSH key authentication
   - Local backend (on Proxmox host)
   - Mock backend (testing)

2. **[02_getting_vm_info.py](02_getting_vm_info.py)** - Retrieving VM information
   - List nodes
   - List VMs
   - Get detailed configuration
   - Check VM status
   - Filter VMs
   - Search by name

3. **[03_creating_vms.py](03_creating_vms.py)** - Creating virtual machines
   - Minimal VM
   - Standard VM
   - Cloud-init VM
   - Multi-disk VM
   - Multi-network VM
   - Batch creation

4. **[04_vm_management.py](04_vm_management.py)** - VM power management
   - Start/stop/reboot
   - Graceful shutdown
   - Force stop
   - Update configuration
   - Resize disk
   - Delete VM
   - Complete lifecycle demo

5. **[05_advanced_operations.py](05_advanced_operations.py)** - Advanced operations
   - Storage management
   - Backups
   - Snapshots
   - Resource monitoring
   - Cluster information
   - Batch operations with retry logic

## Quick Start

### With Mock Backend (No credentials)

```bash
cd /root/nms/proxmox-openapi
python examples/sdk-real/01_authentication.py
```

All examples default to mock backend for safe testing.

### With Real Proxmox

Set credentials:
```bash
export PROXMOX_HOST="pve.example.com"
export PROXMOX_USER="automation@pve"
export PROXMOX_TOKEN_NAME="api-token"
export PROXMOX_TOKEN_VALUE="12345678-abcd-..."
```

Then edit an example to use real connection instead of mock.

## Running Individual Examples

```bash
# Session setup
python 01_authentication.py

# Listing VMs
python 02_getting_vm_info.py

# Creating VMs
python 03_creating_vms.py

# Power management
python 04_vm_management.py

# Advanced operations
python 05_advanced_operations.py
```

## Key Patterns

### Async (Recommended)

```python
import asyncio
from proxmox_openapi import ProxmoxSDK

async def main():
    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        for node in nodes:
            print(node['node'])

asyncio.run(main())
```

### Sync (Blocking)

```python
from proxmox_openapi import ProxmoxSDK

with ProxmoxSDK.sync(mock=True) as proxmox:
    nodes = proxmox.nodes.get()
```

## Documentation

For comprehensive documentation, see the main `docs/` directory:

- [SDK Guide](../../docs/sdk-guide.md)
- [Authentication Guide](../../docs/sdk-authentication.md)
- [Virtual Machines HOW-TO](../../docs/sdk-virtual-machines.md)
- [Examples & Recipes](../../docs/sdk-examples.md)
