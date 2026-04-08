"""Proxmox task (UPID) management utilities."""

from __future__ import annotations

import asyncio
import re
import time
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from proxmox_openapi.sdk.exceptions import ResourceException

if TYPE_CHECKING:
    from proxmox_openapi.sdk.resource import ProxmoxResource

# UPID:pve1:0001E240:00A2F3E1:5F8B2D3C:qmstart:100:root@pam:
_UPID_RE = re.compile(
    r"^UPID:(?P<node>[^:]+):(?P<pid>[0-9A-Fa-f]+):(?P<pstart>[0-9A-Fa-f]+)"
    r":(?P<starttime>[0-9A-Fa-f]+):(?P<type>[^:]*):(?P<id>[^:]*):(?P<user>[^:]*):(?P<comment>.*)$"
)


class Tasks:
    """Utility class for Proxmox task (UPID) management.

    Usage::

        from proxmox_openapi import ProxmoxSDK, Tasks

        async with ProxmoxSDK(...) as proxmox:
            task_id = await proxmox.nodes("pve1").qemu(100).status.start.post()
            status = await Tasks.blocking_status(proxmox, task_id, timeout=120)

            info = Tasks.decode_upid(task_id)
            print(info["node"], info["type"])

            log_raw = await proxmox.nodes("pve1").tasks(task_id).log.get()
            print(Tasks.decode_log(log_raw))
    """

    @staticmethod
    async def blocking_status(
        proxmox: ProxmoxResource,
        task_id: str,
        *,
        timeout: float = 300.0,
        polling_interval: float = 1.0,
        max_polling_interval: float = 30.0,
    ) -> dict[str, Any]:
        """Poll a Proxmox task until it finishes or ``timeout`` is reached.

        Uses exponential backoff: starts at ``polling_interval`` and doubles
        each iteration up to ``max_polling_interval``, reducing unnecessary API
        calls for long-running operations such as migrations or backups.

        Args:
            proxmox: Root :class:`~proxmox_openapi.sdk.resource.ProxmoxResource`.
            task_id: UPID string returned by the task-creating API call.
            timeout: Maximum seconds to wait (default 300).
            polling_interval: Initial seconds between polls (default 1).
            max_polling_interval: Cap for exponential backoff (default 30).

        Returns:
            The final task status dict (``{"status": "stopped", ...}``).

        Raises:
            TimeoutError: If the task does not finish within ``timeout``.
            ResourceException: If the API returns an error.
        """
        info = Tasks.decode_upid(task_id)
        node = info["node"]

        deadline = time.monotonic() + timeout
        current_interval = polling_interval
        while time.monotonic() < deadline:
            status: dict[str, Any] = await proxmox.nodes(node).tasks(task_id).status.get()

            if status.get("status") == "stopped":
                return status

            # Exponential backoff capped at max_polling_interval
            # Sleep for min of current_interval and remaining time to respect deadline
            remaining_time = deadline - time.monotonic()
            sleep_duration = min(current_interval, remaining_time)
            await asyncio.sleep(sleep_duration)
            current_interval = min(current_interval * 2, max_polling_interval)

        raise TimeoutError(
            f"Task {task_id} did not finish within {timeout}s. "
            f"Check it manually: /nodes/{node}/tasks/{task_id}/status"
        )

    @staticmethod
    def decode_upid(upid: str) -> dict[str, Any]:
        """Parse a UPID string into its component fields.

        UPID format::

            UPID:{node}:{pid}:{pstart}:{starttime}:{type}:{id}:{user}:{comment}

        Args:
            upid: UPID string (e.g. ``UPID:pve1:0001E240:00A2F3E1:5F8B2D3C:qmstart:100:root@pam:``).

        Returns:
            Dict with keys: upid, node, pid, pstart, starttime (datetime), type, id, user, comment.

        Raises:
            ValueError: If the UPID string is malformed.
        """
        m = _UPID_RE.match(upid.strip())
        if not m:
            raise ValueError(f"Invalid UPID: {upid!r}")

        start_ts = int(m.group("starttime"), 16)
        return {
            "upid": upid,
            "node": m.group("node"),
            "pid": int(m.group("pid"), 16),
            "pstart": int(m.group("pstart"), 16),
            "starttime": datetime.fromtimestamp(start_ts, tz=timezone.utc),
            "type": m.group("type"),
            "id": m.group("id"),
            "user": m.group("user"),
            "comment": m.group("comment"),
        }

    @staticmethod
    def decode_log(log_data: list[dict[str, Any]]) -> str:
        """Convert Proxmox task log entries to human-readable text.

        Args:
            log_data: List of ``{"n": line_no, "t": text}`` dicts from
                ``GET /nodes/{node}/tasks/{upid}/log``.

        Returns:
            Newline-joined log text.
        """
        if not isinstance(log_data, list):
            return str(log_data)
        return "\n".join(entry.get("t", "") for entry in log_data if isinstance(entry, dict))

    @staticmethod
    async def wait_for_task(
        proxmox: ProxmoxResource,
        task_id: str,
        *,
        timeout: float = 300.0,
        polling_interval: float = 2.0,
        raise_on_failure: bool = True,
    ) -> dict[str, Any]:
        """Wait for a task and optionally raise on failure.

        Args:
            proxmox: Root ProxmoxResource.
            task_id: UPID string.
            timeout: Maximum wait time.
            polling_interval: Poll interval.
            raise_on_failure: If True, raise :exc:`ResourceException` when
                the task exits with ``exitstatus != "OK"``.

        Returns:
            Final task status dict.
        """
        status = await Tasks.blocking_status(
            proxmox, task_id, timeout=timeout, polling_interval=polling_interval
        )
        if raise_on_failure:
            exit_status = status.get("exitstatus", "")
            if exit_status and exit_status != "OK":
                raise ResourceException(
                    status_code=500,
                    status_message="Task Failed",
                    content=f"Task {task_id} exited with status: {exit_status}",
                )
        return status


__all__ = ["Tasks"]
