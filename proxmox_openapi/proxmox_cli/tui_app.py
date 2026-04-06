"""Textual TUI application for proxmox-openapi CLI."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any, Literal

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, RichLog, Static, TextArea, Tree

from proxmox_openapi.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_openapi.proxmox_cli.utils import validate_api_path

TuiMode = Literal["production", "mock"]


@dataclass(frozen=True)
class TuiRuntime:
    """Runtime options passed to the TUI app."""

    mode: TuiMode
    initial_path: str = "/nodes"


@dataclass
class PathNode:
    """Represents a browsable path in the tree."""

    path: str
    label: str
    data: dict[str, Any] | list[dict[str, Any]] | None = None
    children_loaded: bool = False


class ProxmoxTuiApp(App[None]):
    """Enhanced TUI with tree navigation, JSON viewer, and search."""

    CSS = """
    Screen {
        layout: vertical;
    }

    #status {
        height: auto;
        padding: 0 1;
        color: $text-muted;
        background: $surface;
    }

    #filter_bar {
        height: auto;
        padding: 0 1;
        background: $surface;
    }

    #filter_input {
        margin: 0 1;
    }

    #main_container {
        layout: horizontal;
        height: 100%;
    }

    #tree_panel {
        width: 30%;
        border-right: solid $panel;
    }

    #detail_panel {
        width: 70%;
    }

    #command_input {
        margin: 0 1;
    }

    #output_log {
        margin: 1;
        border: solid $panel;
        padding: 0 1;
    }

    #json_view {
        margin: 1;
        border: solid $panel;
    }

    .status-online {
        color: green;
    }

    .status-offline {
        color: red;
    }

    .status-warning {
        color: yellow;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("i", "focus_input", "Focus input"),
        Binding("f", "toggle_filter", "Filter"),
        Binding("t", "toggle_tree", "Tree"),
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("l", "expand_or_select", "Right", show=False),
        Binding("h", "collapse", "Left", show=False),
        Binding("ctrl+l", "clear_output", "Clear output"),
        Binding("/", "focus_filter", "Search", show=False),
        Binding("escape", "close_filter", "Close search", show=False),
    ]

    def __init__(self, bridge: ProxmoxSDKBridge, runtime: TuiRuntime) -> None:
        super().__init__()
        self._bridge = bridge
        self._runtime = runtime
        self._last_command = runtime.initial_path
        self._current_data: list[dict[str, Any]] | dict[str, Any] | None = None
        self._tree_data: dict[str, PathNode] = {}
        self._filter_query: str = ""
        self._show_tree: bool = True

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield Static(
                f"Mode: {self._runtime.mode} | [b]Keys:[/b] q=quit r=refresh f=filter t=tree /=search j/k/l/h=navigate",
                id="status",
            )
            with Horizontal(id="filter_bar"):
                yield Input(
                    placeholder="Filter results... (press / to focus, Esc to close)",
                    id="filter_input",
                )
            with Horizontal(id="main_container"):
                with Vertical(id="tree_panel"):
                    yield Static("Navigation Tree", id="tree_header")
                    yield Tree(id="nav_tree")
                with Vertical(id="detail_panel"):
                    yield Input(value=self._runtime.initial_path, id="command_input")
                    yield RichLog(id="output_log", wrap=True, highlight=False, markup=False)
                    yield TextArea(id="json_view", read_only=True, show_line_numbers=False)
        yield Footer()

    def on_mount(self) -> None:
        self.title = f"Proxmox TUI ({self._runtime.mode})"
        self.sub_title = "Type a path and press Enter - Use tree or / to search"

        # Hide filter bar initially
        self.query_one("#filter_bar", Vertical).display = False

        # Focus command input
        self.query_one("#command_input", Input).focus()

        # Initialize tree
        self._init_tree()

        # Execute initial command
        self._execute_command(self._runtime.initial_path)

    def _init_tree(self) -> None:
        """Initialize the navigation tree with root nodes."""
        tree = self.query_one("#nav_tree", Tree)
        tree.root.label = "/ (root)"

        # Add common paths as expandable nodes
        common_paths = [
            ("/nodes", "Nodes"),
            ("/nodes/{node}/qemu", "Virtual Machines"),
            ("/nodes/{node}/lxc", "Containers"),
            ("/cluster", "Cluster"),
            ("/storage", "Storage"),
            ("/access", "Access"),
        ]

        for path, label in common_paths:
            node = tree.root.add(label, data=PathNode(path=path, label=label))
            node.expandable = True

        tree.root.expand()

    def on_tree_node_expand(self, event: Tree.NodeExpanded) -> None:
        """Load children when a tree node is expanded."""
        node = event.node
        data = node.data
        if data and isinstance(data, PathNode) and not data.children_loaded:
            self._load_tree_children(node, data)

    def _load_tree_children(self, node: Tree.Node, data: PathNode) -> None:
        """Load children for a tree node."""
        try:
            # Replace {node} placeholder with actual node name if needed
            path = data.path
            if "{node}" in path and self._current_data:
                # Try to get first node
                if isinstance(self._current_data, list) and self._current_data:
                    first_item = self._current_data[0]
                    if "node" in first_item:
                        node_name = first_item["node"]
                        path = path.replace("{node}", node_name)

            result = self._bridge.list_children(path)
            if result and isinstance(result, list):
                data.children_loaded = True
                for item in result[:20]:  # Limit children
                    item_label = (
                        item.get("node") or item.get("vmid") or item.get("name") or str(item)
                    )
                    item_path = f"{path}/{item_label}"
                    child_node = node.add(
                        item_label, data=PathNode(path=item_path, label=str(item_label), data=item)
                    )
                    child_node.expandable = True
        except Exception:
            pass  # Silently fail for tree loading

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Navigate to selected tree node."""
        node = event.node
        data = node.data
        if data and isinstance(data, PathNode):
            self.query_one("#command_input", Input).value = data.path
            self._execute_command(data.path)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._execute_command(event.value)

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        pass

    def action_focus_input(self) -> None:
        self.query_one("#command_input", Input).focus()

    def action_focus_filter(self) -> None:
        self.query_one("#filter_bar", Vertical).display = True
        self.query_one("#filter_input", Input).focus()

    def action_close_filter(self) -> None:
        self.query_one("#filter_bar", Vertical).display = False
        self._filter_query = ""
        self.query_one("#command_input", Input).focus()

    def action_toggle_tree(self) -> None:
        """Toggle tree panel visibility."""
        self._show_tree = not self._show_tree
        tree_panel = self.query_one("#tree_panel", Vertical)
        detail_panel = self.query_one("#detail_panel", Vertical)

        if self._show_tree:
            tree_panel.display = True
            detail_panel.width = "70%"
        else:
            tree_panel.display = False
            detail_panel.width = "100%"

    def action_toggle_filter(self) -> None:
        """Toggle filter bar visibility."""
        filter_bar = self.query_one("#filter_bar", Vertical)
        if filter_bar.display:
            self.action_close_filter()
        else:
            self.action_focus_filter()

    def action_refresh(self) -> None:
        self._execute_command(self._last_command)

    def action_clear_output(self) -> None:
        self.query_one("#output_log", RichLog).clear()

    def action_move_down(self) -> None:
        """Move to next item in results."""
        # TODO: Implement data table navigation

    def action_move_up(self) -> None:
        """Move to previous item in results."""
        pass

    def action_expand_or_select(self) -> None:
        """Expand tree node or select current item."""
        tree = self.query_one("#nav_tree", Tree)
        selected = tree.selected_node
        if selected and selected.expandable:
            selected.toggle()
        elif not selected.expandable:
            # Navigate to this item
            data = selected.data
            if data and isinstance(data, PathNode):
                self._execute_command(data.path)

    def action_collapse(self) -> None:
        """Collapse tree node."""
        tree = self.query_one("#nav_tree", Tree)
        selected = tree.selected_node
        if selected and selected.is_expanded:
            selected.toggle()

    def _execute_command(self, raw: str) -> None:
        method, path = self._parse_command(raw)
        self._last_command = f"{method} {path}" if raw.strip() else self._last_command

        log = self.query_one("#output_log", RichLog)
        log.clear()
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

            self._current_data = result

            # Display as formatted JSON
            json_view = self.query_one("#json_view", TextArea)
            json_str = self._format_result(result)
            json_view.load_text(json_str)

            # Show in log too
            log.write(json_str[:2000])  # Truncate long output in log

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
