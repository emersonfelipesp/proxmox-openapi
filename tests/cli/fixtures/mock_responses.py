"""Fixtures for CLI tests."""

from __future__ import annotations

MOCK_NODES_RESPONSE = [
    {
        "node": "pve1",
        "status": "online",
        "uptime": 1234567,
        "cpu": 0.45,
        "maxcpu": 8,
        "mem": 8589934592,
        "maxmem": 17179869184,
        "disk": 107374182400,
        "maxdisk": 214748364800,
    },
    {
        "node": "pve2",
        "status": "online",
        "uptime": 9876543,
        "cpu": 0.12,
        "maxcpu": 8,
        "mem": 15032385536,
        "maxmem": 17179869184,
        "disk": 187649283072,
        "maxdisk": 214748364800,
    },
]

MOCK_QEMU_RESPONSE = [
    {
        "vmid": 100,
        "name": "ubuntu-20.04",
        "status": "running",
        "uptime": 604800,
        "cpus": 2,
        "memory": 2147483648,
    },
    {
        "vmid": 101,
        "name": "ubuntu-22.04",
        "status": "stopped",
        "uptime": 0,
        "cpus": 4,
        "memory": 4294967296,
    },
    {
        "vmid": 102,
        "name": "debian-11",
        "status": "running",
        "uptime": 86400,
        "cpus": 1,
        "memory": 1073741824,
    },
]

MOCK_CLUSTER_RESPONSE = {
    "name": "mycluster",
    "nodes": 3,
    "version": 3,
    "quorum": "ok",
}

__all__ = [
    "MOCK_NODES_RESPONSE",
    "MOCK_QEMU_RESPONSE",
    "MOCK_CLUSTER_RESPONSE",
]
