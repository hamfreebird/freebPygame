"""
Layout managers for freepygame.

These helpers position a collection of components by writing to each component's
``coordinates`` attribute, so they work with any widget or button that exposes
``coordinates`` (the built-in components all do). Layouts are computed by calling
:meth:`arrange`, which returns the list of components in their new positions.
"""

from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

Align = str  # "top-left" | "center" | "bottom-right" ...


def _widget_size(widget) -> Tuple[int, int]:
    """Best-effort size extraction for any supported component."""
    size = getattr(widget, "size", None)
    if isinstance(size, (tuple, list)) and len(size) == 2:
        return int(size[0]), int(size[1])
    width = getattr(widget, "width", None)
    height = getattr(widget, "height", None)
    if width is not None and height is not None:
        return int(width), int(height)
    return (0, 0)


class Layout:
    """Base layout holding an ordered list of components."""

    def __init__(
        self,
        widgets: Optional[Sequence] = None,
        spacing: int = 10,
        padding: int = 10,
    ):
        self.widgets: List = list(widgets or [])
        self.spacing = spacing
        self.padding = padding
        self.origin: Tuple[int, int] = (0, 0)

    def add(self, widget) -> "Layout":
        self.widgets.append(widget)
        return self

    def arrange(self, origin: Optional[Tuple[int, int]] = None) -> List:
        raise NotImplementedError


class VBox(Layout):
    """Stack components vertically (top to bottom)."""

    def arrange(self, origin: Optional[Tuple[int, int]] = None) -> List:
        ox, oy = origin if origin is not None else self.origin
        x = ox + self.padding
        y = oy + self.padding
        for widget in self.widgets:
            widget.coordinates = [x, y]
            w, h = _widget_size(widget)
            y += h + self.spacing
        return self.widgets


class HBox(Layout):
    """Lay components out horizontally (left to right)."""

    def arrange(self, origin: Optional[Tuple[int, int]] = None) -> List:
        ox, oy = origin if origin is not None else self.origin
        x = ox + self.padding
        y = oy + self.padding
        for widget in self.widgets:
            widget.coordinates = [x, y]
            w, h = _widget_size(widget)
            x += w + self.spacing
        return self.widgets


class AnchorLayout(Layout):
    """Pin every component to a single anchor point inside the layout box."""

    def __init__(
        self,
        widgets: Optional[Sequence] = None,
        spacing: int = 10,
        padding: int = 10,
        align: Align = "top-left",
    ):
        super().__init__(widgets, spacing, padding)
        self.align = align

    def arrange(self, origin: Optional[Tuple[int, int]] = None) -> List:
        ox, oy = origin if origin is not None else self.origin
        for widget in self.widgets:
            w, h = _widget_size(widget)
            if self.align == "center":
                x = ox - w // 2
                y = oy - h // 2
            elif self.align == "bottom-right":
                x = ox - w
                y = oy - h
            else:  # top-left
                x, y = ox, oy
            widget.coordinates = [x, y]
        return self.widgets
