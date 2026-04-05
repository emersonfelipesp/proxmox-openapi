# Mock API Mode

Complete guide to using proxmox-openapi in mock mode for development and testing.

---

## Overview

Mock mode provides a **fully functional Proxmox API simulation** with:

- ✅ **646 pre-generated endpoints** from official Proxmox API
- ✅ **In-memory CRUD operations** - Create, read, update, delete
- ✅ **Automatic data seeding** - Sample data generated on first access
- ✅ **State persistence** - Changes persist across requests (during runtime)
- ✅ **Custom mock data** - Load your own test data from JSON/YAML

---

## Starting Mock Mode

### Method 1: Dedicated Mock Server

```bash
proxmox-openapi-mock
```

This runs a standalone mock-only server.

### Method 2: Main App in Mock Mode (Default)

```bash
# Mock mode is the default
uvicorn proxmox_openapi.main:app

# Or explicitly set mock mode
export PROXMOX_API_MODE=mock
uvicorn proxmox_openapi.main:app
```

Both methods provide the same functionality.

---

## How Mock Data Works

### Automatic Seeding

When you make your first **GET** request to an endpoint, mock data is automatically generated:

```python
import httpx

# First GET request - data doesn't exist yet
response = httpx.get("http://localhost:8000/api2/json/nodes")

# Mock data automatically created and returned:
# [{"node": "pve", "status": "online", ...}]
```

### State Persistence

Changes persist in memory during the server lifetime:

```python
# Create a VM
httpx.post(
    "http://localhost:8000/api2/json/nodes/pve/qemu",
    json={"vmid": 100, "name": "test-vm"}
)

# Later requests return the same VM
response = httpx.get("http://localhost:8000/api2/json/nodes/pve/qemu/100")
print(response.json())  # Returns the VM we created
```

!!! warning "Memory Only"
    Mock data is stored in RAM and **will be lost** when the server restarts.

---

## Custom Mock Data

Load your own test data to simulate specific scenarios.

### JSON Format

Create `mock-data.json`:

```json
{
  "/api2/json/nodes": [
    {
      "node": "pve1",
      "status": "online",
      "cpu": 0.25,
      "maxcpu": 16,
      "mem": 8589934592,
      "maxmem": 68719476736
    },
    {
      "node": "pve2",
      "status": "online",
      "cpu": 0.50,
      "maxcpu": 32,
      "mem": 17179869184,
      "maxmem": 137438953472
    }
  ],
  "/api2/json/cluster/resources": [
    {"type": "node", "node": "pve1", "status": "online"},
    {"type": "node", "node": "pve2", "status": "online"},
    {"type": "qemu", "vmid": 100, "name": "prod-web-01", "node": "pve1"},
    {"type": "qemu", "vmid": 101, "name": "prod-db-01", "node": "pve2"}
  ]
}
```

### YAML Format

Create `mock-data.yaml`:

```yaml
/api2/json/nodes:
  - node: pve1
    status: online
    cpu: 0.25
    maxcpu: 16
  - node: pve2
    status: online
    cpu: 0.50
    maxcpu: 32

/api2/json/cluster/resources:
  - type: node
    node: pve1
    status: online
  - type: qemu
    vmid: 100
    name: prod-web-01
    node: pve1
```

### Load Custom Data

=== "Environment Variable"

    ```bash
    export PROXMOX_MOCK_DATA_PATH=./mock-data.json
    proxmox-openapi-mock
    ```

=== "Default Location"

    Place your file at the default path:

    ```bash
    sudo mkdir -p /etc/proxmox-openapi
    sudo cp mock-data.json /etc/proxmox-openapi/
    proxmox-openapi-mock
    ```

=== "Docker"

    ```bash
    docker run -p 8000:8000 \
      -v $(pwd)/mock-data.json:/data/mock.json \
      -e PROXMOX_MOCK_DATA_PATH=/data/mock.json \
      ghcr.io/emersonfelipesp/proxmox-openapi:latest
    ```

---

## CRUD Operations in Detail

### GET Requests

**Collections** (arrays):

```python
# Returns array of items
response = httpx.get("http://localhost:8000/api2/json/nodes")
# [{"node": "pve", ...}]
```

**Single Resources** (objects):

```python
# Returns single object
response = httpx.get("http://localhost:8000/api2/json/nodes/pve/status")
# {"uptime": 12345, "cpu": 0.5, ...}
```

### POST Requests

**Create new items** in collections:

```python
response = httpx.post(
    "http://localhost:8000/api2/json/nodes/pve/qemu",
    json={
        "vmid": 100,
        "name": "test-vm",
        "memory": 2048,
        "cores": 2,
    }
)

# Item added to collection AND created as individual resource
# Now accessible at:
# - /api2/json/nodes/pve/qemu (in the collection)
# - /api2/json/nodes/pve/qemu/100 (individual resource)
```

### PUT Requests

**Replace entire resource**:

```python
response = httpx.put(
    "http://localhost:8000/api2/json/nodes/pve/qemu/100",
    json={
        "vmid": 100,
        "name": "test-vm-renamed",
        "memory": 4096,  # Changed
        "cores": 4,      # Changed
    }
)

# Entire object replaced with new values
```

### PATCH Requests

**Partial update** (merge):

```python
response = httpx.patch(
    "http://localhost:8000/api2/json/nodes/pve/qemu/100",
    json={"memory": 8192}
)

# Only 'memory' field updated, other fields unchanged
```

### DELETE Requests

**Remove resources**:

```python
response = httpx.delete("http://localhost:8000/api2/json/nodes/pve/qemu/100")

# Resource removed from:
# - Individual endpoint (/api2/json/nodes/pve/qemu/100)
# - Parent collection (/api2/json/nodes/pve/qemu)
```

---

## Query Parameters

Mock endpoints support query parameter filtering:

```python
# Get all VMs
all_vms = httpx.get("http://localhost:8000/api2/json/cluster/resources?type=qemu")

# Filter by status
running = httpx.get("http://localhost:8000/api2/json/cluster/resources?type=qemu&status=running")
```

---

## Environment Variables

Configure mock mode behavior:

| Variable | Default | Description |
|----------|---------|-------------|
| `PROXMOX_API_MODE` | `mock` | Set to `mock` for mock mode |
| `PROXMOX_MOCK_SCHEMA_VERSION` | `latest` | OpenAPI schema version to use |
| `PROXMOX_MOCK_DATA_PATH` | `/etc/proxmox-openapi/mock-data.json` | Custom mock data file path |
| `HOST` | `0.0.0.0` | Server host to bind |
| `PORT` | `8000` | Server port |

---

## Use Cases

### Integration Testing

```python
import httpx
import pytest

@pytest.fixture
def proxmox_client():
    return httpx.Client(base_url="http://localhost:8000/api2/json")

def test_create_vm(proxmox_client):
    response = proxmox_client.post(
        "/nodes/pve/qemu",
        json={"vmid": 100, "name": "test", "memory": 2048}
    )
    assert response.status_code == 200

    # Verify VM was created
    vm = proxmox_client.get("/nodes/pve/qemu/100")
    assert vm.json()["vmid"] == 100
```

### CI/CD Pipelines

```yaml
# .github/workflows/test.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Start Mock Proxmox API
        run: |
          pip install proxmox-openapi
          proxmox-openapi-mock &
          sleep 2

      - name: Run Integration Tests
        run: pytest tests/integration/
```

### Local Development

```bash
# Start mock API
proxmox-openapi-mock

# In another terminal, develop your application
python my_proxmox_app.py
```

Your application can make Proxmox API calls without needing a real cluster!

---

## Limitations

!!! warning "Mock Limitations"
    - **No real Proxmox logic** - Doesn't validate Proxmox-specific business rules
    - **Memory-only storage** - Data lost on restart
    - **Simplified state** - Doesn't track complex resource relationships
    - **No async operations** - Real Proxmox tasks are immediate in mock mode

For production use or testing against real Proxmox behavior, use [Real API Mode](real-api.md).

---

## Next Steps

- **[Real API Mode →](real-api.md)** - Connect to actual Proxmox servers
- **[API Reference →](api-reference.md)** - Explore all available endpoints
- **[Development Guide →](development.md)** - Contribute to the project
