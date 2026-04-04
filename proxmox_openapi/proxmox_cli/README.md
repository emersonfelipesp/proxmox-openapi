# Proxmox CLI

A modern, pvesh-like command-line interface for Proxmox VE, PMG, and PBS.

## Features

- **Multi-backend support**: HTTPS, SSH, local pvesh, or mock
- **Intuitive commands**: `get`, `create`, `set`, `delete`, `ls`, `usage`, `help`
- **Flexible authentication**: Password, API token, or interactive
- **Multiple output formats**: JSON, YAML, table, or text
- **Configuration profiles**: Save multiple Proxmox endpoints
- **Full schema discovery**: Built-in help and usage introspection

## Installation

```bash
# With CLI support
pip install proxmox-openapi[cli]

# With all optional dependencies
pip install proxmox-openapi[all]
```

## Quick Start

### Basic Commands

```bash
# List all nodes
proxmox get /nodes

# Get node status
proxmox get /nodes/pve1/status

# List VMs on a node
proxmox ls /nodes/pve1/qemu

# Create a new VM
proxmox create /nodes/pve1/qemu/100 \
  --vmid 100 \
  --name test-vm \
  --cores 2 \
  --memory 2048

# Update VM configuration
proxmox set /nodes/pve1/qemu/100 \
  --cores 4 \
  --memory 4096

# Delete a VM
proxmox delete /nodes/pve1/qemu/100

# List available methods for endpoint
proxmox usage /nodes/pve1/qemu/100

# Get help on an endpoint
proxmox help /nodes/pve1/qemu
```

### Output Formats

```bash
# JSON format (default for structured data)
proxmox get /nodes --output json

# YAML format
proxmox get /nodes --output yaml

# Table format (default for lists)
proxmox ls /nodes/pve1/qemu --output table

# Raw response
proxmox get /nodes --raw

# Save to file
proxmox get /nodes --output-file nodes.json
```

### Global Options

```bash
--backend BACKEND              # https, ssh_paramiko, openssh, local, mock
--config PATH                  # Config file path
--host HOST                    # Proxmox host
--user USER                    # Username/token name
--password PASSWORD            # Password (insecure, use token instead)
--token-value TOKEN            # API token value
--port PORT                    # API port (default: 8006)
--service SERVICE              # PVE, PMG, PBS
--output FORMAT                # json, yaml, table, text, auto
--verbose                       # Enable verbose logging
--quiet                         # Suppress non-essential output
```

## Configuration

Create a config file at `~/.proxmox-cli/config.json`:

```json
{
  "default_profile": "default",
  "profiles": {
    "default": {
      "backend": "https",
      "host": "proxmox.example.com",
      "port": 8006,
      "service": "PVE",
      "user": "admin@pam",
      "token_name": "cli-api",
      "token_value": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "verify_ssl": true
    },
    "staging": {
      "backend": "https",
      "host": "proxmox-staging.example.com",
      "user": "admin@pam",
      "token_value": "..."
    },
    "remote-ssh": {
      "backend": "ssh_paramiko",
      "host": "pve2.example.com",
      "user": "root",
      "password": "secure-password"
    },
    "local": {
      "backend": "local",
      "service": "PVE"
    },
    "mock": {
      "backend": "mock",
      "service": "PVE",
      "version": "latest"
    }
  },
  "global": {
    "output_format": "auto",
    "colors": true,
    "completion_shell": "bash"
  }
}
```

## Backend Types

### HTTPS (default)

```bash
proxmox --backend https --host proxmox.example.com --user admin@pam get /nodes
```

Requires password or token authentication.

### SSH (Paramiko)

```bash
proxmox --backend ssh_paramiko --host pve2.example.com --user root get /nodes
```

Requires SSH credentials, executes pvesh on remote host.

### SSH (OpenSSH)

```bash
proxmox --backend openssh --host pve2.example.com --user root get /nodes
```

Uses system OpenSSH client.

### Local pvesh

Only available when running on a Proxmox host with root privileges:

```bash
proxmox --backend local get /nodes
```

### Mock (Development)

```bash
proxmox --backend mock get /nodes
```

Generates realistic mock data without connecting to Proxmox.

## API Parameter Formats

Parameters can be specified in multiple ways:

### Short form (-d)

```bash
proxmox create /nodes/pve1/qemu/100 \
  -d vmid=100 \
  -d name=test-vm \
  -d cores=2
```

### CLI arguments

```bash
proxmox create /nodes/pve1/qemu/100 \
  --vmid 100 \
  --name test-vm \
  --cores 2
```

### JSON file

```bash
proxmox create /nodes/pve1/qemu/100 \
  --json-file params.json
```

With `params.json`:

```json
{
  "vmid": 100,
  "name": "test-vm",
  "cores": 2,
  "memory": 2048
}
```

## Examples

### Create a Linux VM

```bash
proxmox create /nodes/pve1/qemu/100 \
  -d vmid=100 \
  -d name=linux-vm \
  -d cores=2 \
  -d memory=2048 \
  -d sockets=1 \
  -d ide2='local:cloudinit' \
  -d net0='virtio,bridge=vmbr0'
```

### Start a VM

```bash
proxmox create /nodes/pve1/qemu/100/status/current \
  -d command=start
```

### Get VM status

```bash
proxmox get /nodes/pve1/qemu/100/status/current --output json
```

### List snapshots

```bash
proxmox ls /nodes/pve1/qemu/100/snapshot --columns name,description,snaptime
```

### View configuration options

```bash
proxmox usage /nodes/pve1/qemu/100 --command set
```

## Integration with Configuration Management

### Ansible

```yaml
- name: Get Proxmox nodes
  shell: proxmox get /nodes --output json
  register: nodes_result

- name: Show nodes
  debug:
    msg: "{{ nodes_result.stdout | from_json }}"
```

### Terraform

```hcl
data "external" "proxmox_nodes" {
  program = ["proxmox", "get", "/nodes", "--output", "json"]
}
```

### Shell Scripts

```bash
#!/bin/bash

# Get count of VMs
vm_count=$(proxmox ls /nodes/pve1/qemu | wc -l)
echo "VMs on pve1: $vm_count"

# Backup loop
for vmid in $(proxmox ls /nodes/pve1/qemu --columns vmid | tail -n +2); do
  proxmox create /nodes/pve1/qemu/$vmid/status/current -d command=backup
done
```

## Troubleshooting

### Connection refused

```bash
proxmox --verbose --backend https --host proxmox.example.com get /nodes
```

Check host, port, and SSL certificate.

### Authentication failed

```bash
proxmox --user admin@pam --token-value xxxxxxxx-... get /nodes
```

Verify credentials and token format.

### Permission denied

API token may not have sufficient permissions. Check token scope on Proxmox API Token page.

### Schema errors

Try the mock backend to verify command syntax works:

```bash
proxmox --backend mock get /nodes
```

## See Also

- [Proxmox VE API Documentation](https://pve.proxmox.com/pve-docs/api-viewer/)
- [pvesh Manual](https://pve.proxmox.com/pve-docs/pvesh.1.html)
- [proxmox-openapi Documentation](https://emersonfelipesp.github.io/proxmox-openapi/)
