"""Output themes and styling configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ColorTheme:
    """Color theme configuration."""

    name: str
    primary: str = "#00AA00"  # Green
    secondary: str = "#00AAFF"  # Cyan
    error: str = "#FF0000"  # Red
    warning: str = "#FFAA00"  # Orange
    info: str = "#0000FF"  # Blue
    success: str = "#00AA00"  # Green
    muted: str = "#666666"  # Gray


# Built-in themes
DARK_THEME = ColorTheme(
    name="dark",
    primary="#00DD00",
    secondary="#00DDFF",
    error="#FF3333",
    warning="#FFDD00",
    info="#3399FF",
    success="#00DD00",
    muted="#888888",
)

LIGHT_THEME = ColorTheme(
    name="light",
    primary="#008800",
    secondary="#0088FF",
    error="#DD0000",
    warning="#DD8800",
    info="#0000DD",
    success="#008800",
    muted="#444444",
)

MONOKAI_THEME = ColorTheme(
    name="monokai",
    primary="#A1EFE4",
    secondary="#F92672",
    error="#F92672",
    warning="#E6DB74",
    info="#66D9EF",
    success="#A1EFE4",
    muted="#75715E",
)


def get_theme(name: str) -> Optional[ColorTheme]:
    """Get a theme by name.

    Args:
        name: Theme name (dark, light, monokai)

    Returns:
        ColorTheme or None if not found
    """
    themes = {
        "dark": DARK_THEME,
        "light": LIGHT_THEME,
        "monokai": MONOKAI_THEME,
    }
    return themes.get(name)


def list_themes() -> list[str]:
    """Get list of available theme names.

    Returns:
        List of theme names
    """
    return ["dark", "light", "monokai"]
