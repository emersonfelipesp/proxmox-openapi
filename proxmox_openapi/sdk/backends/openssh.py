"""SSH backend using the native OpenSSH client via openssh_wrapper."""

from __future__ import annotations

import asyncio
import io
import logging
import secrets
from functools import partial
from typing import TYPE_CHECKING, Any

from proxmox_openapi.sdk.backends._cli_base import CliResponse, CommandBaseBackend
from proxmox_openapi.sdk.exceptions import BackendNotAvailableError

if TYPE_CHECKING:
    from proxmox_openapi.sdk.services import ServiceConfig

logger = logging.getLogger(__name__)

try:
    import openssh_wrapper  # type: ignore[import-untyped]

    _OPENSSH_AVAILABLE = True
except ImportError:
    _OPENSSH_AVAILABLE = False


class OpenSshBackend(CommandBaseBackend):
    """Execute Proxmox API calls via the native OpenSSH client.

    Uses ``openssh_wrapper`` to invoke the system ``ssh`` binary.
    Respects ``~/.ssh/config``, supports SSH agent forwarding, and
    allows specifying an identity file.

    Requires::

        pip install proxmox-openapi[ssh]

    Example::

        backend = OpenSshBackend(
            host="pve.example.com",
            user="root",
            service_config=SERVICES["PVE"],
            identity_file="~/.ssh/id_rsa",
        )
        nodes = await backend.request("GET", "/api2/json/nodes")
    """

    def __init__(
        self,
        *,
        host: str,
        user: str,
        service_config: ServiceConfig,
        password: str | None = None,
        identity_file: str | None = None,
        forward_ssh_agent: bool = False,
        config_file: str | None = None,
        port: int = 22,
        sudo: bool = False,
    ) -> None:
        if not _OPENSSH_AVAILABLE:
            raise BackendNotAvailableError(
                "openssh_wrapper is required for the openssh backend. "
                "Install it with: pip install proxmox-openapi[ssh]"
            )
        super().__init__(service_config=service_config, sudo=sudo)
        self._host = host
        self._user = user
        self._password = password
        self._identity_file = identity_file
        self._forward_ssh_agent = forward_ssh_agent
        self._config_file = config_file
        self._port = port
        self._conn: Any = None  # openssh_wrapper.SSHConnection

    def _ensure_connection(self) -> None:
        if self._conn is not None:
            return
        kwargs: dict[str, Any] = {
            "server": self._host,
            "login": self._user,
            "port": self._port,
        }
        if self._identity_file:
            kwargs["identity_file"] = self._identity_file
        if self._config_file:
            kwargs["configfile"] = self._config_file
        if self._forward_ssh_agent:
            kwargs["ssh_agent"] = True

        self._conn = openssh_wrapper.SSHConnection(**kwargs)

    async def close(self) -> None:
        """OpenSSH connections are stateless (no persistent connection)."""
        self._conn = None

    async def _execute_command(self, command: list[str]) -> CliResponse:
        """Run command over OpenSSH in an executor thread."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(self._run_openssh, command))

    def _run_openssh(self, command: list[str]) -> CliResponse:
        """Synchronous OpenSSH command execution (runs in executor)."""
        self._ensure_connection()
        import shlex

        cmd_str = shlex.join(command)
        result = self._conn.run(cmd_str)

        stderr_text = result.stderr.decode("utf-8", errors="replace") if result.stderr else ""
        exit_code = result.returncode or 0
        status_code = self._detect_status_code(stderr_text, exit_code)

        return CliResponse(
            status_code=status_code,
            exit_code=exit_code,
            content=result.stdout or b"",
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Handle SCP file upload then delegate to parent."""
        if data and any(isinstance(v, io.IOBase) for v in data.values()):
            return await self._upload_and_request(method, path, params=params, data=data)
        return await super().request(method, path, params=params, data=data)

    async def _upload_and_request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Upload files via SCP then execute the pvesh command."""
        import os
        import shutil
        import tempfile

        resolved_data = dict(data or {})
        remote_paths: list[str] = []
        loop = asyncio.get_running_loop()

        for key, value in list(resolved_data.items()):
            if isinstance(value, io.IOBase):
                with tempfile.NamedTemporaryFile(delete=False) as tmp:
                    shutil.copyfileobj(value, tmp)
                    local_path = tmp.name

                remote_path = f"/tmp/proxmox_sdk_upload_{secrets.token_hex(8)}"  # noqa: S108
                await loop.run_in_executor(None, partial(self._scp_upload, local_path, remote_path))
                os.unlink(local_path)
                remote_paths.append(remote_path)
                resolved_data[key] = remote_path

        try:
            return await super().request(method, path, params=params, data=resolved_data)
        finally:
            if remote_paths:
                cleanup = ["rm", "-f"] + remote_paths
                try:
                    await loop.run_in_executor(None, partial(self._run_openssh, cleanup))
                except Exception:
                    logger.warning("Failed to clean up remote temp files: %s", remote_paths)

    def _scp_upload(self, local_path: str, remote_path: str) -> None:
        """Upload a local file to the remote host via SCP (blocking)."""
        self._ensure_connection()
        self._conn.scp(local_path, remote_path)


__all__ = ["OpenSshBackend"]
