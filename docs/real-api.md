# Real API Mode

Connect proxmox-openapi to actual Proxmox servers with full request/response validation.

---

## Overview

Real mode transforms proxmox-openapi into a **validated proxy** for your Proxmox API:

- ✅ **646 endpoints** route to real Proxmox server
- ✅ **Request validation** - Pydantic models ensure correct request format
- ✅ **Response validation** - Guarantees response data integrity
- ✅ **Multiple auth methods** - API tokens or username/password
- ✅ **SSL control** - Verify certificates or disable for self-signed
- ✅ **Production-ready** - Async HTTP client with connection pooling

---

## Quick Start

### Prerequisites

- Running Proxmox VE server (7.x or 8.x)
- API credentials (token or username/password)
- Network access to Proxmox server

### Setup

```bash
# Set environment variables
export PROXMOX_API_MODE=real
export PROXMOX_API_URL=https://pve.example.com:8006
export PROXMOX_API_TOKEN_ID=user@pam!mytoken
export PROXMOX_API_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# Start the API
uvicorn proxmox_openapi.main:app
```

Now all requests to `http://localhost:8000/api2/json/*` are proxied to your real Proxmox server!

---

## Authentication Methods

### Method 1: API Tokens (Recommended)

**Create token in Proxmox:**

1. Log into Proxmox web UI
2. Navigate to **Datacenter → Permissions → API Tokens**
3. Click **Add** and create a new token
4. Note the **Token ID** and **Secret** (shown once!)

**Configure:**

```bash
export PROXMOX_API_TOKEN_ID=user@pam!mytoken
export PROXMOX_API_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Format:**
- Token ID: `{username}@{realm}!{token-name}`
- Examples:
  - `root@pam!automation`
  - `admin@pve!backup-token`
  - `deploy@pam!ci-cd`

### Method 2: Username/Password

!!! warning "Less Secure"
    Password auth is less secure than tokens. Use tokens when possible.

```bash
export PROXMOX_API_USERNAME=root@pam
export PROXMOX_API_PASSWORD=your-password
```

The client will automatically obtain a ticket on first request.

---

## SSL Certificate Verification

### Verify SSL (Default, Recommended)

```bash
export PROXMOX_API_VERIFY_SSL=true  # Default
```

Use this with:
- Public CA-signed certificates
- Properly configured domain certificates

### Disable SSL Verification

```bash
export PROXMOX_API_VERIFY_SSL=false
```

Use this for:
- Self-signed certificates
- Development/testing environments
- Internal Proxmox clusters with private CAs

!!! danger "Production Warning"
    Disabling SSL verification in production is a security risk. Use proper certificates instead.

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PROXMOX_API_MODE` | Yes | `mock` | Must be `real` for real mode |
| `PROXMOX_API_URL` | Yes | - | Proxmox server URL |
| `PROXMOX_API_TOKEN_ID` | If using tokens | - | API token ID |
| `PROXMOX_API_TOKEN_SECRET` | If using tokens | - | API token secret |
| `PROXMOX_API_USERNAME` | If using password | - | Username (e.g., `root@pam`) |
| `PROXMOX_API_PASSWORD` | If using password | - | Password |
| `PROXMOX_API_VERIFY_SSL` | No | `true` | Verify SSL certificates |
| `HOST` | No | `0.0.0.0` | Server bind host |
| `PORT` | No | `8000` | Server bind port |

---

## Examples

### Basic Usage

```python
import httpx

# All requests go to real Proxmox
base_url = "http://localhost:8000/api2/json"

# List nodes
nodes = httpx.get(f"{base_url}/nodes").json()
print(nodes)  # Real data from your Proxmox cluster!

# Get specific node status
status = httpx.get(f"{base_url}/nodes/pve/status").json()
print(f"Uptime: {status['uptime']} seconds")
```

### Create a VM

```python
import httpx

response = httpx.post(
    "http://localhost:8000/api2/json/nodes/pve/qemu",
    json={
        "vmid": 100,
        "name": "test-vm",
        "memory": 2048,
        "cores": 2,
        "sockets": 1,
        "scsi0": "local-lvm:32",
        "ide2": "local:iso/debian-12.iso,media=cdrom",
        "net0": "virtio,bridge=vmbr0",
    }
)

if response.status_code == 200:
    print("VM created successfully!")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### List All VMs

```python
import httpx

response = httpx.get("http://localhost:8000/api2/json/cluster/resources?type=vm")
vms = response.json()

for vm in vms:
    print(f"VM {vm['vmid']}: {vm['name']} (status: {vm['status']})")
```

---

## Docker Deployment

### Using Environment Variables

```bash
docker run -p 8000:8000 \
  -e PROXMOX_API_MODE=real \
  -e PROXMOX_API_URL=https://pve.example.com:8006 \
  -e PROXMOX_API_TOKEN_ID=root@pam!mytoken \
  -e PROXMOX_API_TOKEN_SECRET=your-secret \
  -e PROXMOX_API_VERIFY_SSL=false \
  ghcr.io/emersonfelipesp/proxmox-openapi:latest
```

### Using .env File

Create `.env`:

```bash
PROXMOX_API_MODE=real
PROXMOX_API_URL=https://pve.example.com:8006
PROXMOX_API_TOKEN_ID=root@pam!automation
PROXMOX_API_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
PROXMOX_API_VERIFY_SSL=true
```

Run with env file:

```bash
docker run -p 8000:8000 --env-file .env ghcr.io/emersonfelipesp/proxmox-openapi:latest
```

---

## Request/Response Validation

### How It Works

1. **Request arrives** at proxmox-openapi
2. **Pydantic validation** checks request matches OpenAPI schema
3. **Validation passes** → Forward to real Proxmox
4. **Proxmox responds** with data
5. **Pydantic validation** checks response matches schema
6. **Validation passes** → Return to client

### Validation Benefits

- **Type safety** - Catch invalid requests before hitting Proxmox
- **Schema enforcement** - Ensure API contract compliance
- **Error clarity** - Detailed validation error messages
- **Documentation** - Self-documenting via Pydantic models

### Example: Invalid Request

```python
import httpx

# Missing required field 'name'
response = httpx.post(
    "http://localhost:8000/api2/json/nodes/pve/qemu",
    json={"vmid": 100, "memory": 2048}  # Missing 'name'
)

print(response.status_code)  # 422 Unprocessable Entity
print(response.json())
# {
#   "detail": [
#     {
#       "loc": ["body", "name"],
#       "msg": "field required",
#       "type": "value_error.missing"
#     }
#   ]
# }
```

---

## Troubleshooting

### Connection Refused

```
Failed to connect to Proxmox API: Cannot connect to host pve.example.com:8006
```

**Solutions:**
- Verify Proxmox server is running
- Check network connectivity: `ping pve.example.com`
- Verify port 8006 is accessible: `telnet pve.example.com 8006`
- Check firewall rules

### SSL Certificate Verification Failed

```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solutions:**
- Add proper SSL certificate to Proxmox
- Disable verification (dev only): `PROXMOX_API_VERIFY_SSL=false`
- Install CA certificate on system running proxmox-openapi

### Authentication Failed

```
Proxmox authentication failed: 401 Unauthorized
```

**Solutions:**
- Verify credentials are correct
- Check token hasn't expired
- Ensure user has required permissions in Proxmox
- For tokens: verify token privilege separation is configured correctly

### Permission Denied

```
Proxmox API error: 403 Forbidden
```

**Solutions:**
- Grant required permissions to user/token in Proxmox
- Check **Datacenter → Permissions** in Proxmox UI
- Common required privileges:
  - VM.Allocate
  - VM.Config.*
  - Datastore.AllocateSpace
  - Pool.Allocate (if using pools)

---

## Production Deployment

### Recommended Setup

```bash
# Use systemd service
sudo tee /etc/systemd/system/proxmox-openapi.service <<EOF
[Unit]
Description=Proxmox OpenAPI Gateway
After=network.target

[Service]
Type=simple
User=proxmox-api
Group=proxmox-api
WorkingDirectory=/opt/proxmox-openapi
Environment="PROXMOX_API_MODE=real"
Environment="PROXMOX_API_URL=https://pve.example.com:8006"
Environment="PROXMOX_API_TOKEN_ID=automation@pam!gateway"
EnvironmentFile=/etc/proxmox-openapi/env
ExecStart=/usr/local/bin/uvicorn proxmox_openapi.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Store secret in protected file
sudo mkdir -p /etc/proxmox-openapi
sudo tee /etc/proxmox-openapi/env <<EOF
PROXMOX_API_TOKEN_SECRET=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
EOF
sudo chmod 600 /etc/proxmox-openapi/env

# Enable and start
sudo systemctl enable proxmox-openapi
sudo systemctl start proxmox-openapi
```

### Behind Reverse Proxy (nginx)

```nginx
server {
    listen 443 ssl http2;
    server_name proxmox-api.example.com;

    ssl_certificate /etc/ssl/certs/proxmox-api.crt;
    ssl_certificate_key /etc/ssl/private/proxmox-api.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Monitoring

### Health Check Endpoint

```bash
curl http://localhost:8000/health
# {"status": "ready"}
```

### Mode Information

```bash
curl http://localhost:8000/mode
```

Response:

```json
{
  "mode": "real",
  "schema_version": "latest",
  "proxmox_endpoints": 646,
  "proxmox_paths": 428,
  "proxmox_methods": 646,
  "proxmox_url": "https://pve.example.com:8006",
  "auth_method": "token",
  "ssl_verify": true
}
```

---

## Next Steps

- **[API Reference →](api-reference.md)** - Explore available endpoints
- **[Architecture →](architecture.md)** - Understand how it works
- **[Development →](development.md)** - Contribute to the project
