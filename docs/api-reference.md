# API Reference

This page provides a comprehensive reference of all available endpoints in the Proxmox OpenAPI server.

## Endpoint Overview

The server provides **646 Proxmox VE API endpoints** organized into the following categories:

- **Access Control** - Users, groups, roles, permissions, ACLs
- **Cluster** - Cluster configuration, HA, resources, firewall
- **Nodes** - Node management, services, tasks, storage
- **Storage** - Storage configuration and content management
- **Virtual Machines (VMs)** - VM lifecycle, configuration, snapshots
- **Containers (LXC)** - Container lifecycle, configuration, snapshots
- **Network** - SDN, VLANs, zones, subnets
- **Pools** - Resource pools
- **Version** - API version information

## Interactive Documentation

The best way to explore the API is through the **interactive Swagger UI** included with the server:

```bash
# Start the server
uvicorn proxmox_sdk.main:app --reload

# Open in browser
http://localhost:8000/docs
```

The Swagger UI provides:

- Complete endpoint list with descriptions
- Request/response schemas for all operations
- Try-it-out functionality to test endpoints
- Example request/response payloads
- Authentication configuration

## Common Endpoints

### Version Information

```http
GET /version
```

Returns Proxmox VE API version information.

**Response:**
```json
{
  "version": "8.1",
  "release": "1",
  "repoid": "abc123"
}
```

### Access Tickets (Authentication)

```http
POST /access/ticket
```

Create authentication ticket (username/password login).

**Request Body:**
```json
{
  "username": "root@pam",
  "password": "your-password"
}
```

**Response:**
```json
{
  "ticket": "PVE:root@pam:...",
  "CSRFPreventionToken": "...",
  "username": "root@pam"
}
```

### Cluster Status

```http
GET /cluster/status
```

Get cluster status information.

**Response:**
```json
[
  {
    "type": "cluster",
    "name": "proxmox-cluster",
    "quorate": 1,
    "nodes": 3
  }
]
```

### Node List

```http
GET /nodes
```

List all nodes in the cluster.

**Response:**
```json
[
  {
    "node": "pve1",
    "status": "online",
    "cpu": 0.05,
    "maxcpu": 8,
    "mem": 8589934592,
    "maxmem": 34359738368
  }
]
```

### Virtual Machine List

```http
GET /nodes/{node}/qemu
```

List all VMs on a specific node.

**Path Parameters:**
- `node` (string, required) - Node name

**Response:**
```json
[
  {
    "vmid": 100,
    "name": "vm-test",
    "status": "running",
    "cpu": 0.02,
    "maxcpu": 2,
    "mem": 2147483648,
    "maxmem": 4294967296
  }
]
```

### Create Virtual Machine

```http
POST /nodes/{node}/qemu
```

Create a new virtual machine.

**Path Parameters:**
- `node` (string, required) - Node name

**Request Body:**
```json
{
  "vmid": 100,
  "name": "new-vm",
  "memory": 4096,
  "cores": 2,
  "sockets": 1,
  "ostype": "l26",
  "net0": "virtio,bridge=vmbr0",
  "scsi0": "local-lvm:32",
  "ide2": "local:iso/debian-12.0.0-amd64-netinst.iso,media=cdrom"
}
```

**Response:**
```json
{
  "success": true,
  "vmid": 100
}
```

### VM Configuration

```http
GET /nodes/{node}/qemu/{vmid}/config
```

Get VM configuration.

**Path Parameters:**
- `node` (string, required) - Node name
- `vmid` (integer, required) - VM ID

**Response:**
```json
{
  "vmid": 100,
  "name": "vm-test",
  "memory": 4096,
  "cores": 2,
  "sockets": 1,
  "bootdisk": "scsi0",
  "net0": "virtio=AA:BB:CC:DD:EE:FF,bridge=vmbr0"
}
```

### VM Start/Stop/Reboot

```http
POST /nodes/{node}/qemu/{vmid}/status/start
POST /nodes/{node}/qemu/{vmid}/status/stop
POST /nodes/{node}/qemu/{vmid}/status/reboot
POST /nodes/{node}/qemu/{vmid}/status/shutdown
```

Control VM power state.

**Path Parameters:**
- `node` (string, required) - Node name
- `vmid` (integer, required) - VM ID

**Response:**
```json
{
  "success": true,
  "task": "UPID:pve1:..."
}
```

### Container (LXC) List

```http
GET /nodes/{node}/lxc
```

List all containers on a specific node.

**Path Parameters:**
- `node` (string, required) - Node name

**Response:**
```json
[
  {
    "vmid": 200,
    "name": "container-test",
    "status": "running",
    "cpu": 0.01,
    "maxcpu": 2,
    "mem": 536870912,
    "maxmem": 2147483648
  }
]
```

### Storage List

```http
GET /nodes/{node}/storage
```

List storage on a specific node.

**Path Parameters:**
- `node` (string, required) - Node name

**Response:**
```json
[
  {
    "storage": "local",
    "type": "dir",
    "content": "vztmpl,iso,backup",
    "active": 1,
    "total": 107374182400,
    "used": 21474836480,
    "avail": 85899345920
  }
]
```

### Tasks

```http
GET /nodes/{node}/tasks
GET /nodes/{node}/tasks/{upid}/status
GET /nodes/{node}/tasks/{upid}/log
```

View and monitor tasks.

**Response (task list):**
```json
[
  {
    "upid": "UPID:pve1:...",
    "type": "qmstart",
    "id": "100",
    "user": "root@pam",
    "status": "running",
    "starttime": 1704067200
  }
]
```

## Authentication

Most endpoints require authentication. See the [Real API Guide](real-api.md#authentication-methods) for details on:

- API token authentication
- Username/password authentication
- Setting up credentials

## Response Codes

The API uses standard HTTP response codes:

| Code | Description |
|------|-------------|
| `200` | Success |
| `201` | Created |
| `400` | Bad Request - Invalid parameters |
| `401` | Unauthorized - Missing or invalid authentication |
| `403` | Forbidden - Insufficient permissions |
| `404` | Not Found - Resource doesn't exist |
| `422` | Unprocessable Entity - Pydantic request validation failed |
| `500` | Internal Server Error |

## Pagination

Some endpoints support pagination via query parameters:

- `limit` - Maximum number of results (default: varies by endpoint)
- `start` - Starting offset (default: 0)

Example:
```http
GET /nodes/pve1/qemu?limit=10&start=0
```

## Filtering

Many list endpoints support filtering via query parameters. Check the Swagger UI for available filters per endpoint.

## Error Responses

Error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong",
  "errors": [
    {
      "field": "vmid",
      "message": "VM ID already exists"
    }
  ]
}
```

## Schema Models

All request and response schemas are validated using Pydantic models. You can find the complete model definitions in:

- **Swagger UI** - Interactive schema browser at `/docs`
- **ReDoc** - Alternative documentation at `/redoc`
- **OpenAPI JSON** - Raw schema at `/openapi.json`

## Mock vs Real Mode

The behavior of endpoints differs based on the mode:

### Mock Mode (Default)

- In-memory CRUD operations
- No actual Proxmox connection required
- Data resets on server restart
- Perfect for development and testing

### Real Mode

- Proxies requests to real Proxmox VE API
- Requires valid Proxmox credentials
- Full request/response validation
- Production-ready

See the [Mock API Guide](mock-api.md) and [Real API Guide](real-api.md) for mode-specific details.

## Rate Limiting

Proxmox API proxy endpoints have no rate limiting. The `/codegen/*` endpoints are rate-limited via SlowAPI:

| Endpoint | Limit |
|---|---|
| `POST /codegen/generate` | 1 / hour |
| `GET /codegen/pydantic` | 5 / hour |
| `GET /codegen/openapi` | 5 / hour |

See [Security](security.md) for details.

## Versioning

The API follows the Proxmox VE API versioning scheme. The current implementation is based on **Proxmox VE 8.1**.

For the most up-to-date endpoint reference, always check the Swagger UI at `/docs` when running the server.
