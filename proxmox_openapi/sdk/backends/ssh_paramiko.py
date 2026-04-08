"""SSH backend using Paramiko (pure-Python SSH)."""

from __future__ import annotations

import asyncio
import io
import logging
import secrets
import shlex
from functools import partial
from typing import TYPE_CHECKING, Any

from proxmox_openapi.sdk.backends._cli_base import CliResponse, CommandBaseBackend
from proxmox_openapi.sdk.exceptions import BackendNotAvailableError

if TYPE_CHECKING:
    from proxmox_openapi.sdk.services import ServiceConfig

logger = logging.getLogger(__name__)

try:
    import paramiko  # type: ignore[import-untyped]

    _PARAMIKO_AVAILABLE = True
except ImportError:
    _PARAMIKO_AVAILABLE = False


class SshParamikoBackend(CommandBaseBackend):
    """Execute Proxmox API calls via SSH using the Paramiko library.

    Supports password and private-key authentication.  Uses ``asyncio``
    executor wrapping to avoid blocking the event loop.

    Requires::

        pip install proxmox-openapi[ssh]

    Example::

        backend = SshParamikoBackend(
            host="pve.example.com",
            user="root",
            password="secret",
            service_config=SERVICES["PVE"],
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
        private_key_file: str | None = None,
        port: int = 22,
        sudo: bool = False,
        host_key_policy: Any = None,
    ) -> None:
        if not _PARAMIKO_AVAILABLE:
            raise BackendNotAvailableError(
                "paramiko is required for the ssh_paramiko backend. "
                "Install it with: pip install proxmox-openapi[ssh]"
            )
        super().__init__(service_config=service_config, sudo=sudo)
        self._host = host
        self._user = user
        self._password = password
        self._private_key_file = private_key_file
        self._port = port
        self._host_key_policy = host_key_policy
        self._ssh: Any = None  # paramiko.SSHClient

    def _connect(self) -> None:
        """Open (or reuse) the SSH connection (blocking)."""
        if self._ssh is not None:
            return
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        policy = (
            self._host_key_policy if self._host_key_policy is not None else paramiko.WarningPolicy()
        )
        client.set_missing_host_key_policy(policy)

        kwargs: dict[str, Any] = {
            "hostname": self._host,
            "port": self._port,
            "username": self._user,
        }
        if self._password:
            kwargs["password"] = self._password
        if self._private_key_file:
            kwargs["key_filename"] = self._private_key_file

        client.connect(**kwargs)
        self._ssh = client

    async def close(self) -> None:
        """Close the SSH connection."""
        if self._ssh is not None:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self._ssh.close)
            self._ssh = None

    async def _execute_command(self, command: list[str]) -> CliResponse:
        """Run a command over SSH in an executor thread."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(self._run_ssh, command))

    def _run_ssh(self, command: list[str]) -> CliResponse:
        """Synchronous SSH command execution (runs in executor)."""
        self._connect()
        cmd_str = shlex.join(command)
        _, stdout, stderr = self._ssh.exec_command(cmd_str)

        stdout_bytes = stdout.read()
        stderr_text = stderr.read().decode("utf-8", errors="replace")
        exit_code = stdout.channel.recv_exit_status()

        status_code = self._detect_status_code(stderr_text, exit_code)
        return CliResponse(
            status_code=status_code,
            exit_code=exit_code,
            content=stdout_bytes,
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Handle file upload via SFTP then delegate to parent."""
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
        """Upload files via SFTP then execute the pvesh command."""
        resolved_data = dict(data or {})
        remote_paths: list[str] = []
        loop = asyncio.get_running_loop()

        for key, value in list(resolved_data.items()):
            if isinstance(value, io.IOBase):
                remote_path = f"/tmp/proxmox_sdk_upload_{secrets.token_hex(8)}"  # noqa: S108
                await loop.run_in_executor(None, partial(self._sftp_upload, value, remote_path))
                remote_paths.append(remote_path)
                resolved_data[key] = remote_path

        try:
            return await super().request(method, path, params=params, data=resolved_data)
        finally:
            if remote_paths:
                cleanup_cmd = ["rm", "-f", *remote_paths]
                await loop.run_in_executor(None, partial(self._run_ssh, cleanup_cmd))

    def _sftp_upload(self, file_obj: io.IOBase, remote_path: str) -> None:
        """Upload a file-like object via SFTP (blocking)."""
        self._connect()
        sftp = self._ssh.open_sftp()
        try:
            sftp.putfo(file_obj, remote_path)
        finally:
            sftp.close()


__all__ = ["SshParamikoBackend"]
