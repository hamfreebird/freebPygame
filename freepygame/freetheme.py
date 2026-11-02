"""
Theme system for freepygame UI components.

Provides a small, declarative :class:`Theme` descriptor and a registry of named
themes so applications can keep a consistent color palette across buttons,
text, and widgets. Themes are applied to existing components through helper
functions rather than constructor arguments, which keeps the component APIs
stable.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

Color = Tuple[int, int, int]


@dataclass
class Theme:
    """A named color palette for UI components.

    ``font`` is the default font path/name components fall back to when none is
    supplied. ``None`` means "use Pygame's built-in default font" (always
    available), which keeps the library portable.
    """

    name: str
    background: Color = (240, 240, 245)
    surface: Color = (255, 255, 255)
    primary: Color = (70, 130, 180)
    primary_text: Color = (255, 255, 255)
    secondary: Color = (100, 100, 110)
    border: Color = (60, 60, 70)
    text: Color = (30, 30, 30)
    success: Color = (46, 160, 67)
    warning: Color = (240, 173, 78)
    danger: Color = (200, 60, 60)
    font: Optional[str] = None


# A registry of built-in themes keyed by name (lowercase).
THEMES: Dict[str, Theme] = {
    "light": Theme(name="light"),
    "dark": Theme(
        name="dark",
        background=(32, 33, 36),
        surface=(48, 49, 54),
        primary=(88, 140, 220),
        primary_text=(255, 255, 255),
        secondary=(120, 122, 130),
        border=(90, 92, 100),
        text=(235, 235, 240),
        success=(67, 180, 100),
        warning=(220, 170, 70),
        danger=(220, 80, 80),
    ),
}


def get_theme(name: str = "light") -> Theme:
    """Return a named theme, falling back to the light theme for unknown names."""
    return THEMES.get(name.lower(), THEMES["light"])


def apply_theme(button, theme: Optional[Theme] = None) -> None:
    """Apply a theme's palette to a FreeButton / CircleButton instance.

    Sets the background, text, and border colors. Components that do not expose
    the relevant setters are simply ignored for that attribute.
    """
    if theme is None:
        theme = THEMES["light"]
    if hasattr(button, "set_button_color"):
        button.set_button_color(theme.primary)
    if hasattr(button, "set_text_color"):
        button.set_text_color(theme.primary_text)
    if hasattr(button, "set_border_color"):
        button.set_border_color(theme.border)
