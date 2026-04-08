"""Proxmox CLI: A pvesh-like command-line interface for Proxmox API.

This package provides a user-friendly CLI for interacting with Proxmox VE, PMG, and PBS
over multiple transport backends (HTTPS, SSH, local pvesh, mock).

Basic usage:
    proxmox get /nodes
    proxmox create /nodes/pve1/qemu/100 --vmid 100 --name test-vm
    proxmox set /nodes/pve1 -d "description=Node 1"
    proxmox delete /nodes/pve1/qemu/100

For more information, see: https://emersonfelipesp.github.io/proxmox-openapi/
"""

from __future__ import annotations

__version__ = "0.0.2"

__all__ = [
    "__version__",
]
