"""Shared base for CLI backends (local pvesh, ssh_paramiko, openssh)."""

from __future__ import annotations

import json
import platform
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from proxmox_openapi.sdk.backends.base import AbstractBackend
from proxmox_openapi.sdk.exceptions import ResourceException

if TYPE_CHECKING:
    from proxmox_openapi.sdk.services import ServiceConfig

_HTTP_STATUS_RE = re.compile(r"(\d{3})\s+\w+")
_UPID_RE = re.compile(r"UPID:[^:]+:\w+:\w+:\w+:\w+:.*")

_METHOD_TO_VERB: dict[str, str] = {
    "GET": "get",
    "POST": "create",
    "PUT": "set",
    "DELETE": "delete",
    "PATCH": "set",
}


@dataclass
class CliResponse:
    """Represents the result of a CLI (pvesh/pmgsh) command execution."""

    status_code: int
    exit_code: int
    content: bytes

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")


class CommandBaseBackend(AbstractBackend):
    """Mixin providing pvesh/pmgsh command building and response parsing.

    Subclasses must implement ``_execute_command(command: list[str]) -> CliResponse``.
    """

    def __init__(
        self,
        *,
        service_config: ServiceConfig,
        sudo: bool = False,
    ) -> None:
        self._service_config = service_config
        self._sudo = sudo

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Build and execute a pvesh command, returning parsed JSON."""
        verb = _METHOD_TO_VERB.get(method.upper(), "get")
        cli_path = self._strip_api_prefix(path)
        combined = {**(params or {}), **(data or {})}
        clean = {k: v for k, v in combined.items() if v is not None}

        command = self._build_command(verb, cli_path, clean)
        response = await self._execute_command(command)
        return self._parse_response(response, method, path)

    async def close(self) -> None:
        """Nothing to close for CLI backends."""

    # ------------------------------------------------------------------
    # Command building
    # ------------------------------------------------------------------

    def _build_command(
        self,
        verb: str,
        path: str,
        options: dict[str, Any],
    ) -> list[str]:
        """Build the pvesh/pmgsh command list."""
        cli = self._service_config.cli_name
        if not cli:
            raise ResourceException(
                status_code=501,
                status_message="Not Implemented",
                content=f"Service {self._service_config.auth_cookie_name} does not support CLI backends",
            )

        cmd: list[str] = []
        if self._sudo:
            cmd.append("sudo")

        cmd += [cli, verb, path]
        cmd += list(self._service_config.cli_extra_options)

        for key, value in options.items():
            if key == "command" and verb == "create" and "agent/exec" in path:
                # QEMU agent exec — split command string unless on Windows
                if isinstance(value, str) and platform.system() != "Windows":
                    import shlex

                    value = shlex.split(value)
                if isinstance(value, (list, tuple)):
                    for part in value:
                        cmd.append(str(part))
                    continue

            if isinstance(value, bytes):
                value = value.decode("utf-8")
            value_str = str(value)
            if " " in value_str:
                value_str = f'"{value_str}"'
            cmd += [f"-{key}", value_str]

        return cmd

    # ------------------------------------------------------------------
    # Response parsing
    # ------------------------------------------------------------------

    def _parse_response(self, response: CliResponse, method: str, path: str) -> Any:  # noqa: ARG002
        """Parse a CliResponse into Python data."""
        # UPID means task creation succeeded — treat as success
        if _UPID_RE.search(response.text):
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return response.text.strip()

        if response.status_code >= 400:
            raise ResourceException(
                status_code=response.status_code,
                status_message="Error",
                content=response.text.strip(),
                exit_code=response.exit_code,
            )

        if not response.content.strip():
            return None

        try:
            raw = json.loads(response.text)
        except json.JSONDecodeError:
            return response.text.strip()

        if isinstance(raw, dict) and "data" in raw:
            return raw["data"]
        return raw

    def _detect_status_code(self, stderr: str, exit_code: int) -> int:
        """Extract HTTP status code from pvesh stderr output."""
        m = _HTTP_STATUS_RE.search(stderr)
        if m:
            return int(m.group(1))
        return 500 if exit_code != 0 else 200

    def _strip_api_prefix(self, path: str) -> str:
        """Remove the service API prefix (e.g. /api2/json) from the path."""
        prefix = self._service_config.api_path_prefix
        if path.startswith(prefix):
            stripped = path[len(prefix) :]
            return stripped if stripped.startswith("/") else f"/{stripped}"
        return path

    # ------------------------------------------------------------------
    # Abstract
    # ------------------------------------------------------------------

    async def _execute_command(self, command: list[str]) -> CliResponse:
        """Execute the command and return a CliResponse. Must be overridden."""
        raise NotImplementedError


__all__ = ["CommandBaseBackend", "CliResponse"]
