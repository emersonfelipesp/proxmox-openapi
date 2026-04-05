# SDK Authentication & Session Setup

Complete guide to authenticating with the Proxmox SDK and setting up secure sessions for production environments.

---

## Authentication Methods Overview

The Proxmox SDK supports multiple authentication strategies:

| Method | Security | Use Case | Setup Difficulty |
|--------|----------|----------|------------------|
| **API Token** | ⭐⭐⭐⭐⭐ | Automation, CI/CD | Easy |
| **Password** | ⭐⭐⭐ | Manual scripts | Easy |
| **SSH Key** | ⭐⭐⭐⭐ | Remote scripts | Medium |
| **Local (no auth)** | ⭐⭐⭐⭐⭐ | On-host scripts | Easy |
| **2FA (TOTP)** | ⭐⭐⭐⭐⭐ | High security | Medium |

---

## 1. API Token Authentication (Recommended)

API tokens are the **recommended method** for automation because they:
- Have **fine-grained permissions**
- Don't require password changes
- Can be easily revoked
- Reduce blast radius if compromised

### Step 1: Create an API Token in Proxmox

This is done via the **Proxmox UI** or **API**:

#### Via Proxmox UI:

1. Log in to `https://pve.example.com:8006`
2. Navigate to **Datacenter → Permissions → API Tokens**
3. Click **Add**
4. Fill in:
   - **User:** Select the automation user (or create one)
   - **Token ID:** e.g., `my-automation-token`
   - **Realm:** Usually `pve`
   - **Comment:** (optional) e.g., "CI/CD automation token"
5. **Enable token**
6. Click **Add**
7. **Copy the Secret** (shown only once!) and save it securely

#### Via REST API:

```bash
curl -X POST "https://pve.example.com:8006/api2/json/access/ticket" \
  -d "username=root@pam&password=mypassword" \
  --insecure

# Then create token (replace with your ticket):
curl -X POST "https://pve.example.com:8006/api2/json/access/users/automation@pve/tokens/my-token" \
  -H "Authorization: PVEAPIToken=..." \
  --insecure
```

### Step 2: Use API Token in SDK

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="automation@pve",
    token_name="my-automation-token",
    token_value="12345678-abcd-1234-abcd-1234567890ab",
) as proxmox:
    nodes = await proxmox.nodes.get()
    print(nodes)
```

### Step 3: Store Credentials Securely

**Option A: Environment Variables (Recommended)**

```bash
export PROXMOX_HOST="pve.example.com"
export PROXMOX_USER="automation@pve"
export PROXMOX_TOKEN_NAME="my-automation-token"
export PROXMOX_TOKEN_VALUE="12345678-abcd-1234-abcd-1234567890ab"
```

Then load in code:

```python
import os
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host=os.getenv("PROXMOX_HOST"),
    user=os.getenv("PROXMOX_USER"),
    token_name=os.getenv("PROXMOX_TOKEN_NAME"),
    token_value=os.getenv("PROXMOX_TOKEN_VALUE"),
) as proxmox:
    nodes = await proxmox.nodes.get()
```

**Option B: Config File (with restricted permissions)**

Create `~/.proxmox/credentials.json`:

```json
{
  "host": "pve.example.com",
  "user": "automation@pve",
  "token_name": "my-automation-token",
  "token_value": "12345678-abcd-1234-abcd-1234567890ab"
}
```

Restrict permissions:

```bash
chmod 600 ~/.proxmox/credentials.json
```

Load in code:

```python
import json
from pathlib import Path
from proxmox_openapi import ProxmoxSDK

creds = json.loads(Path.home().joinpath(".proxmox/credentials.json").read_text())

async with ProxmoxSDK(**creds) as proxmox:
    nodes = await proxmox.nodes.get()
```

**Option C: Kubernetes Secret (for container environments)**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: proxmox-credentials
type: Opaque
stringData:
  host: "pve.example.com"
  user: "automation@pve"
  token_name: "my-automation-token"
  token_value: "12345678-abcd-1234-abcd-1234567890ab"
```

Then load from mounted secret:

```python
import json
from proxmox_openapi import ProxmoxSDK

creds = json.loads(Path("/var/run/secrets/proxmox-credentials").read_text())

async with ProxmoxSDK(**creds) as proxmox:
    await proxmox.nodes.get()
```

### Real-World Example: CI/CD Pipeline

```yaml
# .github/workflows/deploy-vm.yml
name: Deploy VM

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install SDK
        run: pip install proxmox-openapi

      - name: Deploy VM
        env:
          PROXMOX_HOST: ${{ secrets.PROXMOX_HOST }}
          PROXMOX_USER: ${{ secrets.PROXMOX_USER }}
          PROXMOX_TOKEN_NAME: ${{ secrets.PROXMOX_TOKEN_NAME }}
          PROXMOX_TOKEN_VALUE: ${{ secrets.PROXMOX_TOKEN_VALUE }}
        run: |
          python -c "
          import asyncio
          import os
          from proxmox_openapi import ProxmoxSDK

          async def main():
              async with ProxmoxSDK(
                  host=os.getenv('PROXMOX_HOST'),
                  user=os.getenv('PROXMOX_USER'),
                  token_name=os.getenv('PROXMOX_TOKEN_NAME'),
                  token_value=os.getenv('PROXMOX_TOKEN_VALUE'),
              ) as proxmox:
                  result = await proxmox.nodes('pve1').qemu.post(
                      vmid=100,
                      name='ci-vm',
                      memory=2048,
                  )
                  print(f'VM created: {result}')

          asyncio.run(main())
          "
```

---

## 2. Password Authentication

Simple but less secure. Use for manual scripts or testing only.

### Basic Usage

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="my-secure-password",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### Interactive Password Prompt

```python
import getpass
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password=getpass.getpass("Enter Proxmox password: "),
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### With Environment Variable

```python
import os
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password=os.getenv("PROXMOX_PASSWORD"),
) as proxmox:
    nodes = await proxmox.nodes.get()
```

---

## 3. SSH Key Authentication

Connect via SSH instead of HTTPS. Useful for remote automation or when HTTPS is unavailable.

### Prerequisites

```bash
# Install paramiko (for SSH support)
pip install paramiko

# Or install with SSH extra
pip install proxmox-openapi[ssh]
```

### SSH Key-Based Auth

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="root",
    private_key_file="/home/user/.ssh/id_rsa",
    backend="ssh_paramiko",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### SSH with Password

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="root",
    password="ssh-password",
    backend="ssh_paramiko",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### SSH with SSH Agent

Enable SSH agent forwarding (uses your local agent):

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="root",
    backend="ssh_paramiko",
    forward_ssh_agent=True,  # Use local SSH agent
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### SSH with Custom Identity File

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="root",
    backend="ssh_paramiko",
    identity_file="/home/user/.ssh/custom_key",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### Real-World Example: Ansible Integration

```python
# proxmox_plugin.py
import asyncio
from proxmox_openapi import ProxmoxSDK

class ProxmoxPlugin:
    def __init__(self, host, user, key_file):
        self.host = host
        self.user = user
        self.key_file = key_file

    async def get_vms(self):
        async with ProxmoxSDK(
            host=self.host,
            user=self.user,
            private_key_file=self.key_file,
            backend="ssh_paramiko",
        ) as proxmox:
            return await proxmox.nodes.get()

    def get_vms_sync(self):
        return asyncio.run(self.get_vms())

# Usage in Ansible
plugin = ProxmoxPlugin(
    host="pve.example.com",
    user="root",
    key_file="/home/ansible/.ssh/id_rsa"
)
vms = plugin.get_vms_sync()
```

---

## 4. Local Backend (No Authentication)

Use when running scripts **directly on a Proxmox host**. No authentication required.

### Usage

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    backend="local",
    service="PVE",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### Real-World Example: Local Monitoring Script

```python
# Run this script on the Proxmox host itself
import asyncio
from proxmox_openapi import ProxmoxSDK

async def monitor_nodes():
    async with ProxmoxSDK(backend="local", service="PVE") as proxmox:
        nodes = await proxmox.nodes.get()

        for node in nodes:
            status = await proxmox.nodes(node["node"]).status.get()
            print(f"Node {node['node']}: {status['status']}")

asyncio.run(monitor_nodes())
```

---

## 5. Two-Factor Authentication (TOTP)

If your Proxmox account has 2FA enabled:

### Setup TOTP in Proxmox

1. Log in to `https://pve.example.com:8006`
2. Navigate to **Your Profile → Two-Factor Authentication**
3. Enable **TOTP**
4. Scan QR code with an authenticator (Google Authenticator, Authy, etc.)
5. Save recovery codes (in case you lose access)

### Use TOTP with SDK

```python
from proxmox_openapi import ProxmoxSDK

async with ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="my-password",
    otp="123456",  # Current 6-digit code from your authenticator
    otptype="totp",
) as proxmox:
    nodes = await proxmox.nodes.get()
```

### Dynamic TOTP Generation

Use `pyotp` to generate TOTP codes programmatically:

```bash
pip install pyotp
```

```python
import asyncio
import pyotp
from proxmox_openapi import ProxmoxSDK

async def with_dynamic_totp():
    # Your TOTP secret (from setup QR code)
    totp_secret = "JBSWY3DPEBLW64TMMQE4GDXR3A4WCQPQ"

    totp = pyotp.TOTP(totp_secret)
    current_code = totp.now()

    async with ProxmoxSDK(
        host="pve.example.com",
        user="admin@pam",
        password="my-password",
        otp=current_code,
    ) as proxmox:
        nodes = await proxmox.nodes.get()

asyncio.run(with_dynamic_totp())
```

---

## 6. Advanced: Custom Session Management

### Session Reuse Across Multiple Operations

```python
async def batch_operations():
    async with ProxmoxSDK(
        host="pve.example.com",
        user="automation@pve",
        token_name="my-token",
        token_value="...",
    ) as proxmox:
        # All reuse same session/connection
        nodes = await proxmox.nodes.get()
        for node in nodes:
            status = await proxmox.nodes(node["node"]).status.get()
            vms = await proxmox.nodes(node["node"]).qemu.get()
```

### Sync Wrapper for Scripts

```python
from proxmox_openapi import ProxmoxSDK

def automation_script():
    with ProxmoxSDK.sync(
        host="pve.example.com",
        user="automation@pve",
        token_name="my-token",
        token_value="...",
    ) as proxmox:
        # Blocking calls (no async/await needed)
        nodes = proxmox.nodes.get()
        for node in nodes:
            status = proxmox.nodes(node["node"]).status.get()
            print(f"{node['node']}: {status}")
```

### Synchronous Context Manager with Error Handling

```python
from proxmox_openapi import ProxmoxSDK, AuthenticationError, ResourceException

try:
    with ProxmoxSDK.sync(
        host="pve.example.com",
        user="automation@pve",
        token_name="my-token",
        token_value="...",
    ) as proxmox:
        nodes = proxmox.nodes.get()
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except ResourceException as e:
    print(f"API error: {e.status_code} - {e.status_message}")
```

---

## Security Best Practices

### 1. ✅ DO: Use API Tokens for Automation

```python
# ✅ GOOD
ProxmoxSDK(
    host="pve.example.com",
    user="automation@pve",
    token_name="my-token",
    token_value=os.getenv("PROXMOX_TOKEN"),
)
```

### 2. ❌ DON'T: Hardcode Credentials

```python
# ❌ BAD
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="my-password",  # Hardcoded!
)
```

### 3. ✅ DO: Use Environment Variables or Secrets

```python
# ✅ GOOD
import os

ProxmoxSDK(
    host=os.getenv("PROXMOX_HOST"),
    user=os.getenv("PROXMOX_USER"),
    token_name=os.getenv("PROXMOX_TOKEN_NAME"),
    token_value=os.getenv("PROXMOX_TOKEN_VALUE"),
)
```

### 4. ✅ DO: Restrict API Token Permissions

In Proxmox UI, when creating an API token, assign **minimal required permissions**:

- For read-only operations: Assign `Monitoring` role
- For VM creation: Assign `Administrator` role on specific resource pools only
- For backups: Assign `Backup Operator` role

### 5. ✅ DO: Rotate Tokens Regularly

Set up quarterly rotation in your automation:

```python
import asyncio
from proxmox_openapi import ProxmoxSDK

async def rotate_token():
    async with ProxmoxSDK(
        host="pve.example.com",
        user="admin@pam",
        password=os.getenv("ADMIN_PASSWORD"),
    ) as proxmox:
        # Delete old token
        await proxmox.access.users("automation@pve").tokens("old-token").delete()

        # Create new token
        new_token = await proxmox.access.users("automation@pve").tokens.post(
            tokenid="my-token-v2",
            comment="Rotated quarterly",
        )

        print(f"New token secret: {new_token['value']}")
        # Save to secrets manager
```

### 6. ❌ DON'T: Use Sudo with Passwords

```python
# ❌ BAD (password + sudo)
ProxmoxSDK(
    host="pve.example.com",
    user="automation",
    password="password",
    backend="ssh_paramiko",
    sudo=True,
)
```

Instead, use SSH keys with sudoers configuration:

```bash
# /etc/sudoers
automation ALL=(ALL) NOPASSWD: /usr/bin/pvesh
```

---

## Troubleshooting Authentication

### Issue: "Invalid username or password"

**Causes:**
- Wrong credentials
- User doesn't exist
- Wrong realm (e.g., `admin` vs `admin@pam`)

**Solution:**
```python
# Check exact username format in Proxmox UI
# Format is usually: username@realm
# Examples: admin@pam, automation@pve, user@ldap

ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",      # Note the @pam realm
    password="secret",
)
```

### Issue: "Token authentication failed"

**Causes:**
- Wrong token ID or secret
- Token is disabled
- Token is expired

**Solution:**
```bash
# Verify token exists and is enabled in Proxmox UI
# Check token format: user@realm!tokenid=secret
# Example:
#   User: automation@pve
#   Token ID: my-token
#   Secret: 12345678-abcd-...

# Try regenerating token in UI
```

### Issue: "2FA authentication required"

**Message:** `401 Unauthorized - OTP needed`

**Solution:**
```python
# Add OTP parameter
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam",
    password="password",
    otp="123456",  # Add 6-digit code from authenticator
)
```

### Issue: "SSH authentication failed"

**Causes:**
- SSH key not in `~/.ssh/authorized_keys`
- Wrong key file path
- Key is passphrase-protected

**Solution:**
```bash
# Ensure key is in authorized_keys
ssh-copy-id root@pve.example.com

# Test SSH works
ssh root@pve.example.com

# For passphrase-protected keys, use SSH agent
eval $(ssh-agent)
ssh-add ~/.ssh/id_rsa
```

Then in code:
```python
ProxmoxSDK(
    host="pve.example.com",
    user="root",
    backend="ssh_paramiko",
    forward_ssh_agent=True,
)
```

---

## See Also

- [SDK Guide](./sdk-guide.md) — General SDK usage
- [Virtual Machines HOW-TO](./sdk-virtual-machines.md) — Create and manage VMs
- [API Reference](./api-reference.md) — All available endpoints
