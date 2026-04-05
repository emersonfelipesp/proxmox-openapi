"""Textual TUI application for proxmox-openapi CLI."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Literal

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, Header, Input, RichLog, Static

from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_openapi.proxmox_cli.utils import validate_api_path

TuiMode = Literal["production", "mock"]


@dataclass(frozen=True)
class TuiRuntime:
    """Runtime options passed to the TUI app."""

    mode: TuiMode
    initial_path: str = "/nodes"


class ProxmoxTuiApp(App[None]):
    """Simple command-driven TUI for Proxmox resources."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #status {
        height: auto;
        padding: 0 1;
        color: $text-muted;
    }

    #command_input {
        margin: 0 1;
    }

    #output_log {
        margin: 1;
        border: solid $panel;
        padding: 0 1;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("i", "focus_input", "Focus input"),
        Binding("ctrl+l", "clear_output", "Clear output"),
    ]

    def __init__(self, bridge: ProxmoxSDKBridge, runtime: TuiRuntime) -> None:
        super().__init__()
        self._bridge = bridge
        self._runtime = runtime
        self._last_command = runtime.initial_path

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Static(
                f"Mode: {self._runtime.mode} | Enter '/path' or '<method> /path' where method is get, ls, post, put, delete.",
                id="status",
            )
            yield Input(value=self._runtime.initial_path, id="command_input")
            yield RichLog(id="output_log", wrap=True, highlight=False, markup=False)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"Proxmox TUI ({self._runtime.mode})"
        self.sub_title = "Type a path and press Enter"
        self.query_one("#command_input", Input).focus()
        self._execute_command(self._runtime.initial_path)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._execute_command(event.value)

    def action_focus_input(self) -> None:
        self.query_one("#command_input", Input).focus()

    def action_refresh(self) -> None:
        self._execute_command(self._last_command)

    def action_clear_output(self) -> None:
        self.query_one("#output_log", RichLog).clear()

    def _execute_command(self, raw: str) -> None:
        method, path = self._parse_command(raw)
        self._last_command = f"{method} {path}" if raw.strip() else self._last_command

        log = self.query_one("#output_log", RichLog)
        log.write(f"$ {method.upper()} {path}")

        try:
            if method == "get":
                result = self._bridge.get(path)
            elif method == "ls":
                result = self._bridge.list_children(path)
            elif method == "post":
                result = self._bridge.post(path)
            elif method == "put":
                result = self._bridge.put(path)
            elif method == "delete":
                result = self._bridge.delete(path)
            else:
                log.write(f"Unsupported method: {method}")
                return

            log.write(self._format_result(result))
        except Exception as exc:
            log.write(f"ERROR: {exc}")

    def _parse_command(self, raw: str) -> tuple[str, str]:
        command = raw.strip()
        if not command:
            return ("get", self._runtime.initial_path)

        if command.startswith("/"):
            return ("get", validate_api_path(command))

        parts = command.split(maxsplit=1)
        if len(parts) == 1:
            return (
                "get",
                validate_api_path(parts[0] if parts[0].startswith("/") else f"/{parts[0]}"),
            )

        method = parts[0].lower()
        path = validate_api_path(parts[1])
        return (method, path)

    @staticmethod
    def _format_result(result: object) -> str:
        if result is None:
            return "null"
        if isinstance(result, (dict, list)):
            return json.dumps(result, indent=2, sort_keys=True, default=str)
        return str(result)


def _force_terminal_cleanup() -> None:
    """Best-effort terminal cleanup if Textual exits on exception."""
    stream = getattr(sys, "stdout", None)
    if stream is None or not hasattr(stream, "write"):
        return
    if hasattr(stream, "isatty") and not stream.isatty():
        return
    reset = "".join(
        (
            "\x1b[0m",
            "\x1b[?25h",
            "\x1b[?1000l",
            "\x1b[?1002l",
            "\x1b[?1003l",
            "\x1b[?1006l",
            "\x1b[?1015l",
            "\x1b[?2004l",
        )
    )
    try:
        stream.write(reset)
        stream.flush()
    except Exception:
        return


def run_proxmox_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_path: str = "/nodes",
) -> None:
    """Run the Proxmox Textual TUI."""
    app = ProxmoxTuiApp(bridge=bridge, runtime=TuiRuntime(mode=mode, initial_path=initial_path))
    try:
        app.run()
    finally:
        _force_terminal_cleanup()
