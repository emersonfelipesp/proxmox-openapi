"""Enhanced error handling with recovery suggestions."""

from __future__ import annotations

from typing import Optional


class ErrorSuggester:
    """Provides helpful suggestions for common errors."""

    COMMON_PATHS = [
        "/nodes",
        "/nodes/{node}",
        "/nodes/{node}/qemu",
        "/nodes/{node}/qemu/{vmid}",
        "/nodes/{node}/lxc",
        "/nodes/{node}/lxc/{vmid}",
        "/clusters",
        "/clusters/resources",
        "/storage",
        "/access",
        "/access/users",
        "/access/roles",
    ]

    @staticmethod
    def suggest_for_path_error(path: str) -> Optional[str]:
        """Suggest corrections for path errors.

        Args:
            path: Invalid path attempted

        Returns:
            Suggestion string or None
        """
        # Suggest similar paths
        if "node" in path.lower():
            return "Did you mean /nodes? Try: proxmox ls /nodes"
        elif "qemu" in path.lower():
            return "Did you mean /nodes/{node}/qemu? Try: proxmox ls /nodes/pve1/qemu"
        elif "lxc" in path.lower():
            return "Did you mean /nodes/{node}/lxc? Try: proxmox ls /nodes/pve1/lxc"
        return None

    @staticmethod
    def suggest_for_auth_error(error_msg: str) -> Optional[str]:
        """Suggest fixes for authentication errors.

        Args:
            error_msg: Error message

        Returns:
            Suggestion string or None
        """
        if "401" in error_msg or "Unauthorized" in error_msg:
            return (
                "Authentication failed. Check your credentials:\n"
                "  - Token-based (recommended): proxmox --user admin@pam --token-value <token>\n"
                "  - Password-based: proxmox --user admin@pam --password <pass>"
            )
        elif "403" in error_msg or "Forbidden" in error_msg:
            return "Access denied. Check your token permissions or user role."
        return None

    @staticmethod
    def suggest_for_connection_error(error_msg: str) -> Optional[str]:
        """Suggest fixes for connection errors.

        Args:
            error_msg: Error message

        Returns:
            Suggestion string or None
        """
        if "refused" in error_msg.lower() or "timeout" in error_msg.lower():
            return (
                "Connection failed. Check:\n"
                "  - Host is reachable: proxmox --host <host> --help\n"
                "  - Port is correct (default 8006): proxmox --port 8006\n"
                "  - Proxy/firewall allows connections"
            )
        elif "ssl" in error_msg.lower():
            return (
                "SSL verification failed. Try:\n"
                "  - Use a valid certificate\n"
                "  - Disable verification (insecure): proxmox --verify-ssl false"
            )
        return None
