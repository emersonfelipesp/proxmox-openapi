# Proxmox Python SDK Guide

Welcome to the `proxmox-sdk` SDK! This is a **standalone, production-ready Python SDK** for the Proxmox API that works without any FastAPI server.

---

## What is the Proxmox SDK?

The Proxmox SDK provides a **Pythonic, dynamic interface** to the Proxmox REST API with:

- **Async-first design** - Built on `aiohttp` for efficient concurrent operations
- **Multiple backends** - HTTPS, SSH (Paramiko/OpenSSH), local pvesh, or mock
- **Type-safe** - Full exception handling with meaningful error types
- **Session management** - Automatic credential handling and ticket renewal
- **Real-world ready** - Used in production for automation, monitoring, and infrastructure-as-code

---

## Quick Overview

### Installation

```bash
pip install proxmox-sdk
```

### Basic Usage (3 ways)

**1. Async Context Manager (Recommended)**
```python
import asyncio
from proxmox_sdk import ProxmoxSDK

async def main():
    async with ProxmoxSDK(
        host="pve.example.com",
        user="admin@pam",
        password="secret",
    ) as proxmox:
        nodes = await proxmox.nodes.get()
        print(nodes)

asyncio.run(main())
```

**2. Synchronous (Blocking)**
```python
from proxmox_sdk import ProxmoxSDK

with ProxmoxSDK.sync(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
) as proxmox:
    nodes = proxmox.nodes.get()
    print(nodes)
```

**3. Manual Lifecycle (Async)**
```python
from proxmox_sdk import ProxmoxSDK

proxmox = ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
)
try:
    nodes = await proxmox.nodes.get()
finally:
    await proxmox.close()
```

---

## Core Concepts

### 1. Navigation via Attributes

The SDK builds API paths using **attribute access** and **function calls**:

```python
# Simple navigation
await proxmox.nodes.get()              # GET /api2/json/nodes

# With node name
await proxmox.nodes("pve1").get()      # GET /api2/json/nodes/pve1

# Deeper nesting
await proxmox.nodes("pve1").qemu.get()  # GET /api2/json/nodes/pve1/qemu

# Multiple segments
await proxmox.nodes("pve1").qemu(100).config.get()
# GET /api2/json/nodes/pve1/qemu/100/config

# Alternative: slash-separated ID
await proxmox.nodes("pve1/qemu/100").config.get()
# Same endpoint

# Alternative: list of segments
await proxmox.nodes(["pve1", "qemu", "100"]).config.get()
# Same endpoint
```

### 2. HTTP Methods

All HTTP methods return the response data (or task ID for long operations):

```python
# GET — retrieve data
vms = await proxmox.nodes("pve1").qemu.get()

# POST — create or trigger action
task = await proxmox.nodes("pve1").qemu.post(
    vmid=100,
    name="my-vm",
    memory=2048
)

# PUT — replace/update
await proxmox.nodes("pve1").qemu(100).config.put(memory=4096)

# PATCH — partial update
await proxmox.nodes("pve1").qemu(100).config.patch(
    memory=4096
)

# DELETE — destroy
await proxmox.nodes("pve1").qemu(100).delete()

# Aliases
await proxmox.nodes("pve1").qemu.create(vmid=100, name="vm")  # = .post()
await proxmox.nodes("pve1").qemu(100).set(memory=8192)         # = .put()
```

### 3. Parameters & Data

**Query parameters** (GET, DELETE):
```python
# GET with filter
await proxmox.nodes("pve1").qemu.get(status="running")
# GET /api2/json/nodes/pve1/qemu?status=running
```

**Request body** (POST, PUT, PATCH):
```python
# POST with data
await proxmox.nodes("pve1").qemu.post(
    vmid=100,
    name="my-vm",
    memory=2048,
    cores=2
)
```

### 4. Error Handling

The SDK raises typed exceptions for different scenarios:

```python
from proxmox_sdk import (
    ProxmoxSDK,
    ResourceException,
    AuthenticationError,
    BackendNotAvailableError,
    ProxmoxTimeoutError,
    ProxmoxConnectionError,
)

try:
    await proxmox.nodes("pve1").qemu.post(vmid=100)
except ProxmoxTimeoutError as e:
    # Request exceeded the configured timeout (status_code=504)
    print(f"Timed out: {e.content}")
except ProxmoxConnectionError as e:
    # TCP connection refused, DNS failure, or SSL error (status_code=503)
    print(f"Cannot reach Proxmox: {e.content}")
except ResourceException as e:
    # HTTP >= 400 from the Proxmox API — also catches the two above
    print(f"API error: {e.status_code} - {e.status_message}")
    print(f"Error details: {e.errors}")
except AuthenticationError:
    print("Invalid credentials or token")
except BackendNotAvailableError:
    print("Required backend dependency not installed")
```

`ProxmoxTimeoutError` and `ProxmoxConnectionError` both subclass `ResourceException`, so existing `except ResourceException` handlers continue to work without changes.

---

## Available Backends

The SDK supports multiple backends for different environments:

| Backend | Use Case | Installation |
|---------|----------|--------------|
| **https** (default) | Connect to remote Proxmox server | Built-in |
| **ssh_paramiko** | SSH connection via Paramiko library | `pip install paramiko` |
| **openssh** | SSH via system `openssh-wrapper` | `pip install openssh_wrapper` |
| **local** | Direct CLI access (on Proxmox host) | Built-in |
| **mock** | Testing & development (no real server) | Built-in |

---

## Configuration Options

### HTTPS Backend

```python
ProxmoxSDK(
    host="pve.example.com",           # Proxmox server address
    user="admin@pam",                  # Username with realm
    password="secret",                 # Password
    # OR
    token_name="api-token",            # API token ID (instead of password)
    token_value="xxxxxxxx-...",        # API token secret

    port=8006,                         # Custom port (default: 8006)
    verify_ssl=True,                   # Verify SSL cert (default: True)
    cert="/path/to/cert.pem",          # Custom CA cert
    timeout=30,                        # Total request timeout in seconds (default: 5)
    connect_timeout=5,                 # TCP connection timeout (default: None = use total)
    otp="123456",                      # One-time password for 2FA
    otptype="totp",                    # OTP type: "totp" or "oath"
    proxies={"https": "http://proxy.example.com:3128"},  # HTTP/HTTPS proxy
    max_retries=3,                     # Retry GET/HEAD on 502/503/504 (default: 0)
    retry_backoff=0.5,                 # Exponential backoff base in seconds (default: 0.5)
    backend="https",                   # Backend type
)
```

!!! note "Retry safety"
    Only `GET` and `HEAD` requests are retried. `POST`, `PUT`, `PATCH`, and `DELETE` are never retried automatically to prevent accidental double-mutation.

### SSH Backend (Paramiko)

```python
ProxmoxSDK(
    host="pve.example.com",
    user="root",
    password="secret",
    # OR
    private_key_file="/home/user/.ssh/id_rsa",

    backend="ssh_paramiko",
    # Paramiko-specific options
    identity_file="/custom/key",
    forward_ssh_agent=False,
    sudo=False,
)
```

### Local Backend

```python
ProxmoxSDK(
    backend="local",
    service="PVE",  # or "PMG", "PBS"
)
# Uses the local pvesh CLI — must be run on a Proxmox host!
```

### Mock Backend

```python
ProxmoxSDK(
    backend="mock",
)
# No credentials needed — returns simulated data
```

---

## Authentication Methods

### Method 1: Username & Password

Most common for user accounts:

```python
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="my-password",
)
```

### Method 2: API Token (Recommended for Automation)

More secure and fine-grained permissions:

```python
ProxmoxSDK(
    host="pve.example.com",
    user="monitoring@pve",
    token_name="my-token",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)
```

### Method 3: Two-Factor Authentication (TOTP)

```python
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="password",
    otp="123456",  # Current TOTP code
    otptype="totp",
)
```

### Method 4: SSH Key

```python
ProxmoxSDK(
    host="pve.example.com",
    user="root",
    private_key_file="/home/user/.ssh/id_rsa",
    backend="ssh_paramiko",
)
```

---

## Services & Versions

The SDK supports multiple Proxmox services:

```python
# Proxmox VE (default)
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
    service="PVE",
)

# Proxmox Mail Gateway
ProxmoxSDK(
    host="pmg.example.com",
    user="admin@pam",
    password="secret",
    service="PMG",
)

# Proxmox Backup Server
ProxmoxSDK(
    host="pbs.example.com",
    user="admin@pam",
    password="secret",
    service="PBS",
    port=8007,  # PBS uses port 8007 by default
)
```

!!! tip "PBS HOW-TO Guide"
    For a complete guide to PBS operations — datastores, snapshots, garbage
    collection, verification, pruning, and user management — see the
    **[Proxmox Backup Server HOW-TO →](./sdk-pbs.md)**.

---

## Patterns & Best Practices

### Pattern 1: Use Async Context Manager (Recommended)

```python
async def deploy_vm():
    async with ProxmoxSDK(
        host="pve.example.com",
        user="admin@pam",
        password="secret",
    ) as proxmox:
        # Your code here
        nodes = await proxmox.nodes.get()
    # Automatically closes connection
```

✅ **Benefits:**
- Automatic resource cleanup
- Exception-safe
- Clean syntax

### Pattern 2: Reuse Connection for Multiple Operations

```python
async def setup_environment():
    async with ProxmoxSDK(...) as proxmox:
        # Multiple operations on same connection
        nodes = await proxmox.nodes.get()
        for node in nodes:
            status = await proxmox.nodes(node["node"]).status.get()
            print(f"Node {node['node']}: {status}")
```

### Pattern 3: Handle Task IDs (Long Operations)

Many operations (create VM, backup, etc.) return a **Task ID** you can monitor:

```python
from proxmox_sdk.sdk.tools import Tasks

async with ProxmoxSDK(...) as proxmox:
    # Create VM returns task ID
    result = await proxmox.nodes("pve1").qemu.post(
        vmid=100,
        name="my-vm"
    )

    task_id = result.get("upid")
    if task_id:
        # Monitor the task
        tasks_tool = Tasks(proxmox)
        status = await tasks_tool.wait_task(task_id)
        print(f"Task completed: {status}")
```

### Pattern 4: File Operations

Upload and download backups or configs:

```python
from proxmox_sdk.sdk.tools import Files

async with ProxmoxSDK(...) as proxmox:
    files_tool = Files(proxmox)

    # Download a file
    content = await files_tool.download(
        node="pve1",
        storage="local",
        filename="backup.tar"
    )
```

---

## Next Steps

- **[Complete Authentication Guide →](./sdk-authentication.md)** - Detailed auth methods and token setup
- **[Virtual Machines HOW-TO →](./sdk-virtual-machines.md)** - Getting, creating, and managing VMs
- **[Proxmox Backup Server HOW-TO →](./sdk-pbs.md)** - Datastores, snapshots, GC, and backup management
- **[More Examples →](./sdk-examples.md)** - Clustering, backups, networking, and more

---

## Troubleshooting

### SSL Certificate Error

```python
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
    verify_ssl=False,  # Disable verification (development only!)
)
```

Or provide a custom CA:

```python
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
    cert="/path/to/cacert.pem",
)
```

### Connection Timeout

```python
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
    timeout=30,          # Total request timeout (includes connect + read)
    connect_timeout=5,   # Separate TCP connection deadline
)
```

A `ProxmoxTimeoutError` is raised when the request exceeds the timeout — catch it specifically or via the parent `ResourceException`. To automatically retry on transient failures:

```python
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="secret",
    max_retries=3,       # Retry GET/HEAD up to 3 times
    retry_backoff=1.0,   # 1s, 2s, 4s backoff between attempts
)
```

### SSH Connection Issues

Ensure SSH is enabled and you have the right credentials:

```bash
# Test SSH connection manually first
ssh root@pve.example.com

# Ensure Paramiko is installed
pip install paramiko
```

Then:

```python
ProxmoxSDK(
    host="pve.example.com",
    user="root",
    password="secret",
    backend="ssh_paramiko",
    forward_ssh_agent=True,  # Use SSH agent if available
)
```

---

## See Also

- [pytest test examples](/tests/) in the repository
- [Architecture](./architecture.md) — How the SDK works internally
- [API Reference](./api-reference.md) — Endpoint documentation
- [Proxmox Backup Server HOW-TO](./sdk-pbs.md) — PBS datastores, snapshots, and maintenance
