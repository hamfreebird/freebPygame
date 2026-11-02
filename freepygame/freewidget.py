"""
Widget components for freepygame.

This module provides reusable UI widgets built on top of Pygame drawing
primitives: a :class:`ProgressBar`, a :class:`Slider`, and a :class:`CheckBox`.
Each widget owns its screen surface, knows how to draw itself, and exposes
simple geometry helpers so layouts and click handlers can position and hit-test
them.

It is re-exported by the top-level ``freepygame`` package.
"""

from __future__ import annotations

from typing import Callable, Optional, Tuple

import pygame

Color = Tuple[int, int, int]


class Widget:
    """Base class for freepygame widgets."""

    def __init__(self, screen, coordinates: Tuple[int, int]):
        self.screen = screen
        self.coordinates = list(coordinates)

    def get_coordinates(self) -> list:
        return list(self.coordinates)

    def draw(self) -> None:
        raise NotImplementedError

    def contains(self, pos: Tuple[int, int]) -> bool:
        """Return True if ``pos`` is inside the widget's bounding box."""
        x, y = self.coordinates
        w, h = getattr(self, "size", (0, 0))
        return x <= pos[0] <= x + w and y <= pos[1] <= y + h


class ProgressBar(Widget):
    """A horizontal progress bar showing a value in the range [0, 1]."""

    def __init__(
        self,
        screen,
        coordinates: Tuple[int, int],
        width: int,
        height: int = 14,
        value: float = 0.0,
        color: Color = (70, 130, 180),
        bg_color: Color = (60, 60, 70),
        border_color: Color = (30, 30, 40),
    ):
        super().__init__(screen, coordinates)
        self.size = (width, height)
        self.color = color
        self.bg_color = bg_color
        self.border_color = border_color
        self._value = max(0.0, min(1.0, float(value)))

    def set_value(self, value: float) -> None:
        self._value = max(0.0, min(1.0, float(value)))

    def get_value(self) -> float:
        return self._value

    def draw(self) -> None:
        x, y = self.coordinates
        w, h = self.size
        self.screen.fill(self.bg_color, (x, y, w, h))
        fill_w = int(w * self._value)
        if fill_w > 0:
            self.screen.fill(self.color, (x, y, fill_w, h))
        pygame.draw.rect(self.screen, self.border_color, (x, y, w, h), 1)


class Slider(Widget):
    """A draggable slider for selecting a value in a numeric range."""

    def __init__(
        self,
        screen,
        coordinates: Tuple[int, int],
        width: int,
        height: int = 16,
        min_value: float = 0.0,
        max_value: float = 100.0,
        value: float = 0.0,
        orientation: str = "horizontal",
        handle_color: Color = (70, 130, 180),
        track_color: Color = (60, 60, 70),
        border_color: Color = (30, 30, 40),
    ):
        super().__init__(screen, coordinates)
        self.size = (width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.orientation = orientation
        self.handle_color = handle_color
        self.track_color = track_color
        self.border_color = border_color
        self.on_change: Optional[Callable[[float], None]] = None
        self._value = self._clamp(value)

    def _clamp(self, value: float) -> float:
        return max(self.min_value, min(self.max_value, float(value)))

    def set_value(self, value: float) -> None:
        self._value = self._clamp(value)
        if self.on_change is not None:
            self.on_change(self._value)

    def get_value(self) -> float:
        return self._value

    def _handle_radius(self) -> int:
        return max(4, int(min(self.size) / 2))

    def _handle_center(self) -> Tuple[int, int]:
        x, y = self.coordinates
        w, h = self.size
        t = 0.0 if self.max_value == self.min_value else (
            self._value - self.min_value
        ) / (self.max_value - self.min_value)
        r = self._handle_radius()
        if self.orientation == "horizontal":
            return (int(x + r + t * (w - 2 * r)), y + h // 2)
        return (x + w // 2, int(y + r + t * (h - 2 * r)))

    def set_from_pos(self, pos: Tuple[int, int]) -> bool:
        """Update the value from a pointer position if it lies on the track."""
        if not self.contains(pos):
            return False
        x, y = self.coordinates
        w, h = self.size
        r = self._handle_radius()
        if self.orientation == "horizontal":
            t = (pos[0] - x - r) / max(1, (w - 2 * r))
        else:
            t = (pos[1] - y - r) / max(1, (h - 2 * r))
        t = max(0.0, min(1.0, t))
        self.set_value(self.min_value + t * (self.max_value - self.min_value))
        return True

    def draw(self) -> None:
        x, y = self.coordinates
        w, h = self.size
        self.screen.fill(self.track_color, (x, y, w, h))
        pygame.draw.rect(self.screen, self.border_color, (x, y, w, h), 1)
        hx, hy = self._handle_center()
        r = self._handle_radius()
        pygame.draw.circle(self.screen, self.handle_color, (hx, hy), r)
        pygame.draw.circle(self.screen, self.border_color, (hx, hy), r, 1)


class CheckBox(Widget):
    """A toggleable check box with an optional change callback."""

    def __init__(
        self,
        screen,
        coordinates: Tuple[int, int],
        size: int = 20,
        checked: bool = False,
        box_color: Color = (255, 255, 255),
        check_color: Color = (70, 130, 180),
        border_color: Color = (60, 60, 70),
    ):
        super().__init__(screen, coordinates)
        self.size = (size, size)
        self.box_color = box_color
        self.check_color = check_color
        self.border_color = border_color
        self.checked = checked
        self.on_toggle: Optional[Callable[[bool], None]] = None

    def toggle(self) -> bool:
        self.checked = not self.checked
        if self.on_toggle is not None:
            self.on_toggle(self.checked)
        return self.checked

    def set_checked(self, value: bool) -> None:
        self.checked = bool(value)

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        if self.contains(pos):
            self.toggle()
            return True
        return False

    def draw(self) -> None:
        x, y = self.coordinates
        s = self.size[0]
        self.screen.fill(self.box_color, (x, y, s, s))
        pygame.draw.rect(self.screen, self.border_color, (x, y, s, s), 1)
        if self.checked:
            pad = max(3, s // 4)
            pygame.draw.line(
                self.screen, self.check_color,
                (x + pad, y + s // 2), (x + s // 2, y + s - pad), 3,
            )
            pygame.draw.line(
                self.screen, self.check_color,
                (x + s // 2, y + s - pad), (x + s - pad, y + pad), 3,
            )
