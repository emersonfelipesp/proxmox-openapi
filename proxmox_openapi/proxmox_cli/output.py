"""Output formatting and styling for CLI results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from rich.console import Console
    from rich.syntax import Syntax
    from rich.table import Table

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .exceptions import OutputError


def get_context_options() -> dict[str, Any]:
    """Return Typer/Click context options if running inside a command callback."""
    try:
        import click

        ctx = click.get_current_context(silent=True)
        if ctx and isinstance(ctx.obj, dict):
            return ctx.obj
    except Exception:
        pass
    return {}


def resolve_output_format(
    output: str | None = None,
    *,
    json_output: bool = False,
    yaml_output: bool = False,
    markdown_output: bool = False,
    fallback: str = "human",
) -> str:
    """Resolve the final output format from explicit options and shorthand flags."""
    shorthand_formats = [
        name
        for enabled, name in (
            (json_output, "json"),
            (yaml_output, "yaml"),
            (markdown_output, "markdown"),
        )
        if enabled
    ]

    if len(shorthand_formats) > 1:
        raise OutputError("Use only one of --json, --yaml, or --markdown")

    if output and shorthand_formats:
        raise OutputError("Use either --output or --json/--yaml/--markdown, not both")

    selected = shorthand_formats[0] if shorthand_formats else (output or fallback)
    normalized = selected.lower().strip()
    aliases = {
        "yml": "yaml",
        "md": "markdown",
    }
    normalized = aliases.get(normalized, normalized)

    if normalized == "auto":
        # Keep backward compatibility while enforcing a structured readable default.
        return "human"

    if normalized not in OutputFormatter.FORMATS:
        raise OutputError(f"Unsupported output format: {normalized}")

    return normalized


class OutputFormatter:
    """Formats and outputs CLI results in various formats."""

    FORMATS: set[str] = {"human", "json", "yaml", "markdown", "table", "text", "raw", "auto"}
    """Supported output format identifiers."""
    
    AUTO_THRESHOLD: int = 5  # Number of items to auto-detect as table
    """Minimum item count to auto-detect output as table format."""

    def __init__(self, format: str = "auto", colors: bool = True) -> None:
        """Initialize OutputFormatter.

        Args:
            format: Output format (json, yaml, table, text, auto, raw)
            colors: Enable colored output (requires rich)
        """
        self.format = format
        self.colors = colors and RICH_AVAILABLE
        self.console = Console() if RICH_AVAILABLE else None

    def format_output(
        self,
        data: Any,
        title: str | None = None,
        columns: list[str] | None = None,
    ) -> str:
        """Format output data for display.

        Args:
            data: Data to format
            title: Optional title for output
            columns: Optional column selection for tables

        Returns:
            Formatted output string

        Raises:
            OutputError: If formatting fails
        """
        try:
            # Determine format if auto
            fmt = resolve_output_format(self.format, fallback="human")
            if fmt == "auto":
                fmt = self._detect_format(data)

            # Format based on selected format
            if fmt == "json":
                return self._format_json(data)
            elif fmt == "yaml":
                return self._format_yaml(data)
            elif fmt == "markdown":
                return self._format_markdown(data)
            elif fmt == "table":
                return self._format_table(data, columns=columns)
            elif fmt == "text":
                return self._format_text(data)
            elif fmt == "human":
                return self._format_human(data, columns=columns)
            elif fmt == "raw":
                return str(data)
            else:
                return str(data)
        except Exception as e:
            raise OutputError(f"Failed to format output: {e}")

    def print_output(
        self,
        data: Any,
        title: str | None = None,
        columns: list[str] | None = None,
        file: str | Path | None = None,
    ) -> None:
        """Print formatted output to console or file.

        Args:
            data: Data to format and print
            title: Optional title for output
            columns: Optional column selection for tables
            file: Optional file path to write output to

        Raises:
            OutputError: If output fails
        """
        output = self.format_output(data, title=title, columns=columns)

        if file:
            try:
                Path(file).write_text(output)
            except (IOError, OSError) as e:
                raise OutputError(f"Cannot write to {file}: {e}")
        else:
            if self.console:
                self.console.print(output)
            else:
                print(output)

    def _detect_format(self, data: Any) -> str:
        """Auto-detect appropriate output format.

        Args:
            data: Data to analyze

        Returns:
            Detected format (json, table, text)
        """
        if isinstance(data, dict):
            return "json"
        elif isinstance(data, list):
            if len(data) > self.AUTO_THRESHOLD and all(isinstance(item, dict) for item in data):
                return "table"
            return "json"
        elif isinstance(data, (bool, int, float, type(None))):
            return "text"
        else:
            return "text"

    def _format_human(self, data: Any, columns: list[str] | None = None) -> str:
        """Format data as structured human-readable output."""
        if isinstance(data, list) and data and all(isinstance(item, dict) for item in data):
            return self._format_table(data, columns=columns)

        if isinstance(data, dict):
            # Flat dictionaries are easier to scan as key/value lines.
            if all(not isinstance(v, (dict, list)) for v in data.values()):
                return self._format_text(data)
            return self._format_yaml(data)

        if isinstance(data, list):
            if not data:
                return "No results"
            if all(not isinstance(item, (dict, list)) for item in data):
                return "\n".join(f"- {item}" for item in data)
            return self._format_yaml(data)

        return self._format_text(data)

    def _format_json(self, data: Any) -> str:
        """Format data as JSON.

        Args:
            data: Data to format

        Returns:
            JSON string
        """
        output = json.dumps(data, indent=2, default=str)

        if self.colors and self.console:
            syntax = Syntax(output, "json", theme="monokai", line_numbers=False)
            return syntax
        return output

    def _format_yaml(self, data: Any) -> str:
        """Format data as YAML.

        Args:
            data: Data to format

        Returns:
            YAML string
        """
        try:
            import yaml

            output = yaml.dump(data, default_flow_style=False, sort_keys=False)
        except ImportError:
            # Fallback to JSON if yaml not available
            return self._format_json(data)

        if self.colors and self.console:
            syntax = Syntax(output, "yaml", theme="monokai", line_numbers=False)
            return syntax
        return output

    def _format_markdown(self, data: Any) -> str:
        """Format JSON-like data as Markdown derived from parsed response objects."""
        if isinstance(data, dict):
            if not data:
                return "_No results_"
            if all(not isinstance(v, (dict, list)) for v in data.values()):
                rows = ["| key | value |", "| --- | --- |"]
                rows.extend(f"| {k} | {v} |" for k, v in data.items())
                return "\n".join(rows)
            return f"```json\n{json.dumps(data, indent=2, default=str)}\n```"

        if isinstance(data, list):
            if not data:
                return "_No results_"

            if all(isinstance(item, dict) for item in data):
                return self._format_markdown_table(data)

            if all(not isinstance(item, (dict, list)) for item in data):
                return "\n".join(f"- {item}" for item in data)

            return f"```json\n{json.dumps(data, indent=2, default=str)}\n```"

        return str(data)

    def _format_markdown_table(self, data: list[dict[str, Any]]) -> str:
        """Format a list of dictionaries as a markdown table."""
        column_names: list[str] = []
        seen: set[str] = set()

        for row in data:
            for key in row.keys():
                if key not in seen:
                    seen.add(key)
                    column_names.append(key)

        if not column_names:
            return "_No results_"

        header = "| " + " | ".join(column_names) + " |"
        separator = "| " + " | ".join("---" for _ in column_names) + " |"
        lines = [header, separator]

        for row in data:
            values = [str(row.get(name, "")) for name in column_names]
            lines.append("| " + " | ".join(values) + " |")

        return "\n".join(lines)

    def _format_table(self, data: Any, columns: list[str] | None = None) -> str:
        """Format data as a table.

        Args:
            data: Data to format (should be list of dicts)
            columns: Optional columns to include

        Returns:
            Table string
        """
        if not isinstance(data, list):
            return self._format_json(data)

        if not data:
            return "No results"

        # Use first item to determine columns
        first_item = data[0]
        if not isinstance(first_item, dict):
            return self._format_json(data)

        if not RICH_AVAILABLE or not self.colors:
            return self._format_text_table(data, columns=columns)

        # Create rich table
        table = Table(show_header=True, header_style="bold magenta")

        # Add columns
        cols = columns or list(first_item.keys())
        for col in cols:
            table.add_column(col)

        # Add rows
        for item in data:
            if isinstance(item, dict):
                row = [str(item.get(col, "")) for col in cols]
                table.add_row(*row)

        return table

    def _format_text(self, data: Any) -> str:
        """Format data as plain text.

        Args:
            data: Data to format

        Returns:
            Text string
        """
        if isinstance(data, dict):
            lines = [f"{k}: {v}" for k, v in data.items()]
            return "\n".join(lines)
        elif isinstance(data, list):
            return "\n".join(str(item) for item in data)
        else:
            return str(data)

    def _format_text_table(self, data: list[dict], columns: list[str] | None = None) -> str:
        """Format data as a simple text table (when rich is not available).

        Args:
            data: List of dictionaries to format
            columns: Optional columns to include

        Returns:
            Text table string
        """
        if not data:
            return "No results"

        cols = columns or list(data[0].keys())
        col_widths = {col: len(col) for col in cols}

        # Calculate column widths
        for item in data:
            for col in cols:
                width = len(str(item.get(col, "")))
                col_widths[col] = max(col_widths[col], width)

        # Format header
        header = " | ".join(col.ljust(col_widths[col]) for col in cols)
        separator = "-+-".join("-" * col_widths[col] for col in cols)

        lines = [header, separator]

        # Format rows
        for item in data:
            row = " | ".join(str(item.get(col, "")).ljust(col_widths[col]) for col in cols)
            lines.append(row)

        return "\n".join(lines)

    def print_success(self, message: str) -> None:
        """Print a success message.

        Args:
            message: Success message
        """
        if self.console and self.colors:
            self.console.print(f"[green]✓[/green] {message}")
        else:
            print(f"✓ {message}")

    def print_error(self, message: str, title: str | None = None) -> None:
        """Print an error message.

        Args:
            message: Error message
            title: Optional error title
        """
        if self.console and self.colors:
            self.console.print(f"[red]✗[/red] {title or 'Error'}: {message}")
        else:
            print(f"✗ {title or 'Error'}: {message}")

    def print_warning(self, message: str) -> None:
        """Print a warning message.

        Args:
            message: Warning message
        """
        if self.console and self.colors:
            self.console.print(f"[yellow]⚠[/yellow] {message}")
        else:
            print(f"⚠ {message}")
