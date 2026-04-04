# Using the Proxmox SDK with Mock Data

The `proxmox-openapi` SDK provides built-in mock support for **zero-setup testing and development** — no real Proxmox server required!

---

## Quick Start

### Async Usage

```python
from proxmox_openapi.sdk import ProxmoxSDK

# Create a mock SDK instance
async with ProxmoxSDK.mock() as proxmox:
    # Query mock data
    nodes = await proxmox.nodes.get()
    print(f"Nodes: {nodes}")
    
    # Create mock resources
    vm = await proxmox.nodes("pve").qemu.post(vmid=100, name="test-vm")
    print(f"Created VM: {vm}")
    
    # Retrieve created resource
    retrieved = await proxmox.nodes("pve").qemu(100).get()
    print(f"Retrieved VM: {retrieved}")
```

### Sync Usage (No async/await)

```python
from proxmox_openapi.sdk import ProxmoxSDK

# Create a mock SDK instance (blocking)
with ProxmoxSDK.sync_mock() as proxmox:
    # All API calls block until complete
    nodes = proxmox.nodes.get()
    print(f"Nodes: {nodes}")
    
    # Create mock resources
    vm = proxmox.nodes("pve").qemu.post(vmid=100, name="test-vm")
    print(f"Created VM: {vm}")
```

---

## Features

✅ **Zero Setup** — No real Proxmox server needed  
✅ **In-Memory CRUD** — Create, read, update, delete mock resources  
✅ **Deterministic Data** — Same seed produces same data (testable)  
✅ **Schema-Driven** — Mock data respects Proxmox OpenAPI schema  
✅ **Multi-Service Support** — PVE, PMG, PBS  
✅ **State Persistence** — Changes persist during runtime  

---

## Detailed Guide

### Async with Context Manager (Recommended)

```python
from proxmox_openapi.sdk import ProxmoxSDK

async with ProxmoxSDK.mock() as proxmox:
    # proxmox is the root ProxmoxResource
    nodes = await proxmox.nodes.get()
    
    # Automatic cleanup when exiting context
```

### Async Manual Lifecycle

```python
from proxmox_openapi.sdk import ProxmoxSDK

proxmox_sdk = ProxmoxSDK.mock()
proxmox = proxmox_sdk._root  # Access the root resource

try:
    nodes = await proxmox.nodes.get()
finally:
    await proxmox_sdk.close()
```

### Sync with Context Manager (Recommended)

```python
from proxmox_openapi.sdk import ProxmoxSDK

with ProxmoxSDK.sync_mock() as proxmox:
    nodes = proxmox.nodes.get()
    print(nodes)
    
    # Automatic cleanup when exiting context
```

### Sync Manual Lifecycle

```python
from proxmox_openapi.sdk import ProxmoxSDK

proxmox = ProxmoxSDK.sync_mock()

try:
    nodes = proxmox.nodes.get()
    print(nodes)
finally:
    proxmox.close()
```

---

## Common Workflows

### Listing Resources

```python
from proxmox_openapi.sdk import ProxmoxSDK

with ProxmoxSDK.sync_mock() as proxmox:
    # List nodes
    nodes = proxmox.nodes.get()
    print(f"Nodes: {nodes}")
    
    # List VMs on a node
    vms = proxmox.nodes("pve").qemu.get()
    print(f"VMs: {vms}")
    
    # List containers (LXC)
    containers = proxmox.nodes("pve").lxc.get()
    print(f"Containers: {containers}")
```

### Creating Resources

```python
with ProxmoxSDK.sync_mock() as proxmox:
    # Create a VM
    vm = proxmox.nodes("pve").qemu.post(
        vmid=100,
        name="my-vm",
        memory=2048,
        cores=2
    )
    print(f"Created: {vm}")
```

### Retrieving Specific Resources

```python
with ProxmoxSDK.sync_mock() as proxmox:
    # Get a specific VM
    vm = proxmox.nodes("pve").qemu(100).get()
    print(f"VM 100: {vm}")
    
    # Get node status
    node_status = proxmox.nodes("pve").status.get()
    print(f"Node status: {node_status}")
```

### Updating Resources

```python
with ProxmoxSDK.sync_mock() as proxmox:
    # Update a VM (PUT replaces all fields)
    updated = proxmox.nodes("pve").qemu(100).put(
        name="updated-vm",
        memory=4096
    )
    print(f"Updated: {updated}")
    
    # Patch a VM (PATCH updates specific fields)
    patched = proxmox.nodes("pve").qemu(100).patch(
        name="patched-vm"
    )
    print(f"Patched: {patched}")
```

### Deleting Resources

```python
with ProxmoxSDK.sync_mock() as proxmox:
    # Delete a VM
    result = proxmox.nodes("pve").qemu(100).delete()
    print(f"Deleted: {result}")
```

---

## Specifying Schema Versions

Control which Proxmox OpenAPI schema to use:

```python
from proxmox_openapi.sdk import ProxmoxSDK

# Use latest version (default)
async with ProxmoxSDK.mock() as proxmox:
    nodes = await proxmox.nodes.get()

# Use a specific version
async with ProxmoxSDK.mock(schema_version="8.1") as proxmox:
    nodes = await proxmox.nodes.get()

# Sync version
with ProxmoxSDK.sync_mock(schema_version="8.0") as proxmox:
    nodes = proxmox.nodes.get()
```

**Available versions depend on your installation.** See [Mock API documentation](mock-api.md) for a list of supported versions.

---

## Multi-Service Support

Create mock instances for different Proxmox services:

```python
from proxmox_openapi.sdk import ProxmoxSDK

# Proxmox VE (default)
async with ProxmoxSDK.mock(service="PVE") as proxmox:
    nodes = await proxmox.nodes.get()

# Proxmox Mail Gateway
async with ProxmoxSDK.mock(service="PMG") as proxmox:
    # PMG-specific endpoints
    pass

# Proxmox Backup Server
async with ProxmoxSDK.mock(service="PBS") as proxmox:
    # PBS-specific endpoints
    pass
```

---

## Testing

### Unit Tests

```python
import pytest
from proxmox_openapi.sdk import ProxmoxSDK

@pytest.mark.asyncio
async def test_node_listing():
    """Test listing nodes from mock API."""
    async with ProxmoxSDK.mock() as proxmox:
        nodes = await proxmox.nodes.get()
        assert isinstance(nodes, list)
        assert len(nodes) > 0
        assert nodes[0].get("node") is not None

@pytest.mark.asyncio
async def test_vm_creation():
    """Test creating a VM in mock API."""
    async with ProxmoxSDK.mock() as proxmox:
        vm = await proxmox.nodes("pve").qemu.post(
            vmid=100,
            name="test-vm"
        )
        assert vm.get("vmid") == 100
        assert vm.get("name") == "test-vm"

@pytest.mark.asyncio
async def test_vm_retrieval():
    """Test retrieving a created VM."""
    async with ProxmoxSDK.mock() as proxmox:
        # Create
        created = await proxmox.nodes("pve").qemu.post(
            vmid=101,
            name="test-vm-2"
        )
        
        # Retrieve
        retrieved = await proxmox.nodes("pve").qemu(101).get()
        assert retrieved.get("vmid") == created.get("vmid")
        assert retrieved.get("name") == created.get("name")
```

### Integration Tests

```python
def test_vm_lifecycle_sync():
    """Test full VM lifecycle using sync API."""
    with ProxmoxSDK.sync_mock() as proxmox:
        # Create
        vm = proxmox.nodes("pve").qemu.post(
            vmid=200,
            name="lifecycle-test"
        )
        assert vm["vmid"] == 200
        
        # Retrieve
        retrieved = proxmox.nodes("pve").qemu(200).get()
        assert retrieved["vmid"] == 200
        
        # Update
        updated = proxmox.nodes("pve").qemu(200).put(
            name="lifecycle-updated"
        )
        assert updated["name"] == "lifecycle-updated"
        
        # Delete
        proxmox.nodes("pve").qemu(200).delete()
        
        # Verify deletion (should raise or be empty, depending on mock behavior)
```

---

## State Persistence

Mock state persists in memory during a single session but **resets on restart**:

```python
with ProxmoxSDK.sync_mock() as proxmox:
    # Session 1: Create data
    vm = proxmox.nodes("pve").qemu.post(vmid=300, name="test")
    retrieved = proxmox.nodes("pve").qemu(300).get()
    print(retrieved)  # ✅ Works

# Context exits, state is lost

with ProxmoxSDK.sync_mock() as proxmox:
    # Session 2: Data is gone
    try:
        vm = proxmox.nodes("pve").qemu(300).get()
    except Exception:
        print("VM not found (state was reset)")  # ✅ Expected
```

For persistent mock data across sessions, see [Custom Mock Data (FastAPI Mode)](mock-api.md#custom-mock-data).

---

## Error Handling

The SDK raises `ResourceException` for API errors:

```python
from proxmox_openapi.sdk import ProxmoxSDK
from proxmox_openapi.sdk.exceptions import ResourceException

with ProxmoxSDK.sync_mock() as proxmox:
    try:
        # Attempt invalid operation
        proxmox.nodes("nonexistent").qemu.get()
    except ResourceException as e:
        print(f"API Error: {e.status_code} - {e.status_message}")
```

---

## Differences from Real Proxmox

### Similarities
- ✅ Same endpoint structure `/api2/json/...`
- ✅ Same request/response format (JSON)
- ✅ Same attribute-based navigation
- ✅ Same method names (GET, POST, PUT, PATCH, DELETE)

### Differences
- ⚠️ No actual VM/container creation (mock only)
- ⚠️ No permission validation (all operations allowed)
- ⚠️ No task tracking (UPIDs not returned)
- ⚠️ Limited data validation (basic schema compliance)
- ⚠️ State resets on server restart (in-memory only)

---

## Next Steps

- **[Real API Mode](real-api.md)** — Connect to actual Proxmox servers
- **[Mock API Mode (FastAPI)](mock-api.md)** — Run a mock server for HTTP clients
- **[Architecture Guide](architecture.md)** — Understand SDK internals
- **[API Reference](api-reference.md)** — Full endpoint documentation

---
