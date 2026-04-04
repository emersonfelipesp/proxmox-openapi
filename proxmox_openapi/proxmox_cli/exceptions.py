"""CLI-specific exceptions and error handling."""

from __future__ import annotations


class ProxmoxCLIError(Exception):
    """Base exception for Proxmox CLI errors."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        """Initialize ProxmoxCLIError.

        Args:
            message: Error message to display to user
            exit_code: Exit code for the CLI (default: 1)
        """
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code


class ConfigError(ProxmoxCLIError):
    """Configuration loading/validation error."""

    def __init__(self, message: str) -> None:
        """Initialize ConfigError."""
        super().__init__(f"Configuration error: {message}", exit_code=2)


class AuthenticationError(ProxmoxCLIError):
    """Authentication error."""

    def __init__(self, message: str) -> None:
        """Initialize AuthenticationError."""
        super().__init__(f"Authentication failed: {message}", exit_code=3)


class BackendError(ProxmoxCLIError):
    """Backend initialization or connection error."""

    def __init__(self, message: str, backend: str | None = None) -> None:
        """Initialize BackendError."""
        prefix = f"Backend error ({backend})" if backend else "Backend error"
        super().__init__(f"{prefix}: {message}", exit_code=4)


class PathError(ProxmoxCLIError):
    """Invalid or malformed API path error."""

    def __init__(self, message: str, path: str | None = None) -> None:
        """Initialize PathError."""
        suffix = f" (path: {path})" if path else ""
        super().__init__(f"Invalid path: {message}{suffix}", exit_code=5)


class ParameterError(ProxmoxCLIError):
    """Invalid parameter or argument error."""

    def __init__(self, message: str, param: str | None = None) -> None:
        """Initialize ParameterError."""
        suffix = f" (param: {param})" if param else ""
        super().__init__(f"Invalid parameter: {message}{suffix}", exit_code=6)


class APIError(ProxmoxCLIError):
    """API request error."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize APIError."""
        prefix = f"API error ({status_code})" if status_code else "API error"
        super().__init__(f"{prefix}: {message}", exit_code=7)


class OutputError(ProxmoxCLIError):
    """Output formatting or writing error."""

    def __init__(self, message: str) -> None:
        """Initialize OutputError."""
        super().__init__(f"Output error: {message}", exit_code=8)
