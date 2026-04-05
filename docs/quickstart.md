# Quick Start

Get up and running with proxmox-openapi in under 5 minutes.

---

## Step 1: Install

```bash
pip install proxmox-openapi
```

---

## Step 2: Start the Mock API

```bash
proxmox-openapi-mock
```

You should see output like:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 3: Explore the API

Open your browser to:

**http://localhost:8000/docs**

You'll see the **Swagger UI** with **646 Proxmox API endpoints** ready to use!

Try these endpoints:

- **GET /** - Root endpoint showing API info
- **GET /mode** - See current mode and configuration
- **GET /api2/json/nodes** - List Proxmox nodes (mock data)
- **GET /api2/json/version** - Get Proxmox version info

---

## Step 4: Make Your First Request

=== "Python (httpx)"

    ```python
    import httpx

    # Get nodes list
    response = httpx.get("http://localhost:8000/api2/json/nodes")
    print(response.json())
    ```

=== "Python (requests)"

    ```python
    import requests

    response = requests.get("http://localhost:8000/api2/json/nodes")
    print(response.json())
    ```

=== "curl"

    ```bash
    curl http://localhost:8000/api2/json/nodes
    ```

=== "JavaScript (fetch)"

    ```javascript
    fetch('http://localhost:8000/api2/json/nodes')
      .then(res => res.json())
      .then(data => console.log(data))
    ```

---

## Step 5: Try CRUD Operations

### Create a Resource (POST)

```python
import httpx

# Create a new VM
response = httpx.post(
    "http://localhost:8000/api2/json/nodes/pve/qemu",
    json={
        "vmid": 100,
        "name": "test-vm",
        "memory": 2048,
        "cores": 2,
    }
)

print(response.json())
# Mock data created and stored in memory!
```

### Read the Resource (GET)

```python
# Retrieve the VM we just created
response = httpx.get("http://localhost:8000/api2/json/nodes/pve/qemu/100")
print(response.json())
# Returns the same VM data - state persisted!
```

### Update the Resource (PUT)

```python
# Update the VM
response = httpx.put(
    "http://localhost:8000/api2/json/nodes/pve/qemu/100",
    json={"memory": 4096}
)

print(response.json())
# Memory updated to 4096MB
```

### Delete the Resource (DELETE)

```python
# Delete the VM
response = httpx.delete("http://localhost:8000/api2/json/nodes/pve/qemu/100")
print(response.status_code)  # 200 OK
```

---

## Using the SDK Directly (No Server Required)

The `proxmox-openapi` SDK can work standalone without a FastAPI server:

### Async SDK (with async/await)

```python
from proxmox_openapi.sdk import ProxmoxSDK
import asyncio

async def main():
    # Create mock SDK instance
    async with ProxmoxSDK.mock() as proxmox:
        # List nodes
        nodes = await proxmox.nodes.get()
        print(f"Nodes: {nodes}")

        # Create a VM
        vm = await proxmox.nodes("pve").qemu.post(
            vmid=100,
            name="my-vm"
        )
        print(f"Created: {vm}")

        # Retrieve VM
        retrieved = await proxmox.nodes("pve").qemu(100).get()
        print(f"Retrieved: {retrieved}")

asyncio.run(main())
```

### Sync SDK (No async/await)

```python
from proxmox_openapi.sdk import ProxmoxSDK

# Create mock SDK instance
with ProxmoxSDK.sync_mock() as proxmox:
    # All calls block
    nodes = proxmox.nodes.get()
    print(f"Nodes: {nodes}")

    # Create a VM
    vm = proxmox.nodes("pve").qemu.post(
        vmid=100,
        name="my-vm"
    )
    print(f"Created: {vm}")
```

!!! tip "SDK Benefits"
    - **Zero server setup** — No FastAPI required
    - **Direct Python** — Integration into scripts and libraries
    - **Same API** — Use synchronously or asynchronously
    - **Multiple backends** — Switch between mock, SSH, HTTPS, local at runtime
    - **Production-ready** — Same SDK for development and real Proxmox

---

## Understanding Mock Mode

!!! info "Mock Mode Behavior"
    - **In-memory state**: All data stored in RAM during runtime
    - **Automatic seeding**: First GET request creates sample data
    - **State persistence**: Changes persist across requests (until restart)
    - **No real Proxmox needed**: Perfect for development and testing

---

## Next Steps

### Learn More About Mock Mode

- **[Mock API Mode Guide →](mock-api.md)** - Custom mock data, advanced features
- **[API Reference →](api-reference.md)** - Complete endpoint documentation

### Connect to Real Proxmox

- **[Real API Mode Guide →](real-api.md)** - Connect to actual Proxmox servers

### Develop & Contribute

- **[Development Guide →](development.md)** - Set up development environment
- **[Architecture Overview →](architecture.md)** - How it works internally

---

## Common Next Tasks

### Load Custom Mock Data

```bash
# Create custom mock data file
cat > mock-data.json <<EOF
{
  "/api2/json/nodes": [
    {"node": "pve1", "status": "online", "cpu": 0.2},
    {"node": "pve2", "status": "online", "cpu": 0.5}
  ]
}
EOF

# Set environment variable
export PROXMOX_MOCK_DATA_PATH=./mock-data.json

# Start API
proxmox-openapi-mock
```

### Run with Docker

```bash
docker run -p 8000:8000 ghcr.io/emersonfelipesp/proxmox-openapi:latest
```

### Switch to Real API Mode

```bash
export PROXMOX_API_MODE=real
export PROXMOX_API_URL=https://pve.example.com:8006
export PROXMOX_API_TOKEN_ID=user@pam!mytoken
export PROXMOX_API_TOKEN_SECRET=your-secret

uvicorn proxmox_openapi.main:app
```

---

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
proxmox-openapi-mock --port 8080

# Or with environment variable
PORT=8080 proxmox-openapi-mock
```

### Import Errors

```bash
# Ensure proxmox-openapi is installed
pip show proxmox-openapi

# Reinstall if needed
pip install --upgrade proxmox-openapi
```

### No Endpoints Showing in /docs

This usually means the pre-generated schema isn't loading. Check:

```python
from proxmox_openapi.schema import load_proxmox_generated_openapi

schema = load_proxmox_generated_openapi("latest")
print(f"Schema loaded: {schema is not None}")
print(f"Paths: {len(schema.get('paths', {})) if schema else 0}")
```

---

## Get Help

- **[FAQ →](faq.md)** - Common questions and answers
- **[GitHub Issues](https://github.com/emersonfelipesp/proxmox-openapi/issues)** - Report bugs
- **[GitHub Discussions](https://github.com/emersonfelipesp/proxmox-openapi/discussions)** - Ask questions
