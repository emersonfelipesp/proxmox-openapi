# Proxmox SDK Examples

Production-ready examples demonstrating the Proxmox OpenAPI SDK for real-world use cases.

## Quick Start

### Run Examples with Mock Backend (No credentials needed)

```bash
# Navigate to repository
cd /root/nms/proxmox-openapi

# Install dependencies
pip install -e .

# Run any example
python examples/sdk-real/01_authentication.py
```

## Examples Overview

### 1. Authentication (`01_authentication.py`)

Demonstrates different authentication methods:

- **API Token** - Recommended for automation and CI/CD
- **Password** - Simple but less secure
- **SSH Key** - For remote script execution
- **Local** - Direct CLI access on Proxmox host
- **Mock** - Testing without real connection

**Run:**
```bash
python examples/sdk-real/01_authentication.py
```

**Key Concepts:**
- Setting up credentials
- Using environment variables
- Async context managers
- Sync wrappers (blocking calls)

---

### 2. Getting VM Information (`02_getting_vm_info.py`)

Learn how to retrieve and filter VM data:

- List all nodes
- List VMs on a node
- Get detailed VM configuration
- Check VM status
- Filter by status (running, stopped)
- Search VMs by name

**Run:**
```bash
python examples/sdk-real/02_getting_vm_info.py
```

**Key Concepts:**
- API path navigation
- Query operations (GET)
- Configuration retrieval
- Filtering and searching

---

### 3. Creating Virtual Machines (`03_creating_vms.py`)

Complete guide to VM creation scenarios:

- **Minimal VM** - Simplest configuration (1 core, 512MB)
- **Standard VM** - Production-ready (2 cores, 2GB, 60GB disk)
- **Cloud-Init VM** - Automated provisioning
- **Multi-Disk VM** - Multiple storage pools
- **Multi-Network VM** - Multiple bridges
- **Batch Creation** - Create multiple VMs

**Run:**
```bash
python examples/sdk-real/03_creating_vms.py
```

**Key Concepts:**
- POST operations (create)
- Configuration parameters
- Disk and network configuration
- Error handling
- Batch operations

---

### 4. VM Power Management (`04_vm_management.py`)

Control VM lifecycle:

- Start VM
- Stop VM (graceful shutdown)
- Force stop (immediate power off)
- Reboot VM
- Suspend VM
- Update configuration
- Resize disk
- Delete VM

**Run:**
```bash
python examples/sdk-real/04_vm_management.py
```

**Key Concepts:**
- Power control operations
- PUT/PATCH operations (updates)
- DELETE operations
- Task IDs
- VM lifecycle management

---

### 5. Advanced Operations (`05_advanced_operations.py`)

Production operations and monitoring:

- List storage pools
- Create backups
- Create and list snapshots
- Monitor node resources
- Get cluster information
- Find resource-heavy VMs
- Retry logic for resilience

**Run:**
```bash
python examples/sdk-real/05_advanced_operations.py
```

**Key Concepts:**
- Storage management
- Backup and snapshot operations
- Resource monitoring
- Cluster status
- Error handling with retries

---

## Using Real Proxmox Connection

To run examples against a real Proxmox instance:

### Option 1: Edit Examples Directly

```python
# Replace mock with real connection
async with ProxmoxSDK(
    host="pve.example.com",
    user="automation@pve",
    token_name="api-token",
    token_value="...",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### Option 2: Use Environment Variables

```bash
export PROXMOX_HOST="pve.example.com"
export PROXMOX_USER="automation@pve"
export PROXMOX_TOKEN_NAME="api-token"
export PROXMOX_TOKEN_VALUE="12345..."

python examples/sdk-real/01_authentication.py
```

### Option 3: Create a Config File

Create `~/.proxmox-config.json`:

```json
{
  "host": "pve.example.com",
  "user": "automation@pve",
  "token_name": "api-token",
  "token_value": "..."
}
```

Then load in your script:

```python
import json
from pathlib import Path

config = json.loads(Path.home().joinpath(".proxmox-config.json").read_text())

async with ProxmoxSDK(**config) as proxmox:
    nodes = await proxmox.nodes.get()
```

---

## Common Patterns

### Async Context Manager (Recommended)

```python
import asyncio
from proxmox_openapi import ProxmoxSDK

async def main():
    async with ProxmoxSDK(...) as proxmox:
        nodes = await proxmox.nodes.get()

asyncio.run(main())
```

### Sync Wrapper (Blocking)

```python
from proxmox_openapi import ProxmoxSDK

with ProxmoxSDK.sync(...) as proxmox:
    nodes = proxmox.nodes.get()  # Blocking call
```

### Error Handling

```python
from proxmox_openapi import (
    ProxmoxSDK,
    ResourceException,
    AuthenticationError,
)

try:
    async with ProxmoxSDK(...) as proxmox:
        vms = await proxmox.nodes("pve").qemu.post(vmid=100, name="vm")
except AuthenticationError:
    print("Invalid credentials")
except ResourceException as e:
    print(f"API error: {e.status_code} - {e.status_message}")
```

### Task Monitoring

```python
from proxmox_openapi.sdk.tools import Tasks

async with ProxmoxSDK(...) as proxmox:
    result = await proxmox.nodes("pve").qemu.post(vmid=100, name="vm")

    task_id = result.get("upid")
    if task_id:
        tasks = Tasks(proxmox)
        status = await tasks.wait_task(task_id, timeout=300)
```

### Batch Operations

```python
tasks = []

for vmid in range(100, 105):
    result = await proxmox.nodes("pve").qemu.post(
        vmid=vmid,
        name=f"vm-{vmid}",
        memory=2048,
    )
    tasks.append(result.get("upid"))

# Wait for all to complete
for task_id in tasks:
    await tasks_tool.wait_task(task_id)
```

---

## Documentation References

For detailed information, see the SDK documentation:

- **[SDK Guide](../docs/sdk-guide.md)** - Overview and core concepts
- **[Authentication Guide](../docs/sdk-authentication.md)** - All auth methods, token setup, security
- **[Virtual Machines HOW-TO](../docs/sdk-virtual-machines.md)** - Comprehensive VM management guide
- **[Examples & Recipes](../docs/sdk-examples.md)** - Advanced real-world scenarios
- **[API Reference](../docs/api-reference.md)** - Complete endpoint documentation

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'proxmox_openapi'"

Install the SDK:
```bash
pip install -e .
```

### "ConnectionError" or "SSL verification failed"

Update certificate handling:
```python
ProxmoxSDK(
    host="pve.example.com",
    user="...",
    password="...",
    verify_ssl=False,  # Development only!
)
```

### "Authentication failed"

Verify credentials:
```bash
# Check environment variables
echo $PROXMOX_HOST
echo $PROXMOX_USER

# Test real Proxmox connection
curl -k https://pve.example.com:8006/api2/json/version
```

---

## Contributing

Have a useful example? Submit a PR to `examples/sdk-real/`!

Example naming convention:
- `0N_descriptive_name.py` where N is 1-9
- Include docstrings at top
- Add to this README

---

## See Also

- [proxmox-openapi Repository](https://github.com/emersonfelipesp/proxmox-openapi)
- [Proxmox API Documentation](https://pve.proxmox.com/pve-docs/api-viewer/)
- [Official Proxmox Documentation](https://pve.proxmox.com/wiki/)
