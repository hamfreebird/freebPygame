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

from typing import Callable, List, Optional, Tuple

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


class InputBox(Widget):
    """A single-line text input with keyboard focus and a blinking cursor.

    The box gains focus when clicked. While focused it consumes ``KEYDOWN``
    events forwarded by :class:`~freepygame.freeframe.FreeFrame` via
    :meth:`handle_key`. Supports editing keys (backspace, delete, arrows,
    home/end), a character limit, a password mask, a placeholder, and
    ``on_change`` / ``on_submit`` callbacks.
    """

    def __init__(
        self,
        screen,
        coordinates: Tuple[int, int],
        width: int,
        height: int = 30,
        value: str = "",
        placeholder: str = "",
        font=None,
        size: int = 24,
        max_length: int = 0,
        password: bool = False,
        border_radius: int = 0,
        theme: "Theme" = None,
        text_color: Color = (30, 30, 30),
        bg_color: Color = (255, 255, 255),
        border_color: Color = (120, 120, 130),
        focus_border_color: Color = (70, 130, 180),
        placeholder_color: Color = (150, 150, 160),
        on_change: Optional[Callable[[str], None]] = None,
        on_submit: Optional[Callable[[str], None]] = None,
    ):
        super().__init__(screen, coordinates)
        self.size = (width, height)
        if theme is not None:
            bg_color = theme.surface
            border_color = theme.border
            text_color = theme.text
            focus_border_color = theme.primary
            placeholder_color = theme.secondary
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.focus_border_color = focus_border_color
        self.placeholder_color = placeholder_color
        self.placeholder = placeholder
        self.password = password
        self.max_length = max_length
        self.border_radius = border_radius
        self.on_change = on_change
        self.on_submit = on_submit
        self.focused = False
        try:
            self._font = pygame.font.Font(font, size)
        except TypeError:
            self._font = font
        self.set_value(value)

    # -- value / focus ----------------------------------------------------
    def set_value(self, value: str) -> None:
        self.value = str(value)
        self._cursor = len(self.value)

    def get_value(self) -> str:
        return self.value

    def focus(self) -> None:
        self.focused = True
        self._cursor = len(self.value)

    def blur(self) -> None:
        self.focused = False

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        if self.contains(pos):
            self.focus()
            return True
        return False

    # -- keyboard ---------------------------------------------------------
    def handle_key(self, event) -> None:
        """Process a ``KEYDOWN`` event. Called by FreeFrame for the focused box."""
        if not self.focused:
            return
        key = event.key
        if key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            if self.on_submit is not None:
                self.on_submit(self.value)
            return
        if key == pygame.K_BACKSPACE:
            if self._cursor > 0:
                self.value = self.value[: self._cursor - 1] + self.value[self._cursor :]
                self._cursor -= 1
        elif key == pygame.K_DELETE:
            if self._cursor < len(self.value):
                self.value = self.value[: self._cursor] + self.value[self._cursor + 1 :]
        elif key == pygame.K_LEFT:
            self._cursor = max(0, self._cursor - 1)
            return
        elif key == pygame.K_RIGHT:
            self._cursor = min(len(self.value), self._cursor + 1)
            return
        elif key == pygame.K_HOME:
            self._cursor = 0
            return
        elif key == pygame.K_END:
            self._cursor = len(self.value)
            return
        else:
            ch = getattr(event, "unicode", "")
            if (
                ch
                and ch.isprintable()
                and (self.max_length == 0 or len(self.value) < self.max_length)
            ):
                self.value = self.value[: self._cursor] + ch + self.value[self._cursor :]
                self._cursor += 1
        if self.on_change is not None:
            self.on_change(self.value)

    # -- rendering --------------------------------------------------------
    def _cursor_visible(self) -> bool:
        return (pygame.time.get_ticks() // 500) % 2 == 0

    def draw(self) -> None:
        x, y = self.coordinates
        w, h = self.size
        pad = 6
        inner_w = w - 2 * pad
        pygame.draw.rect(
            self.screen, self.bg_color, (x, y, w, h), border_radius=self.border_radius
        )
        border = self.focus_border_color if self.focused else self.border_color
        pygame.draw.rect(
            self.screen, border, (x, y, w, h), 1, border_radius=self.border_radius
        )

        shown = "*" * len(self.value) if self.password else self.value
        if shown:
            text_img = self._font.render(shown, True, self.text_color)
        else:
            text_img = self._font.render(self.placeholder, True, self.placeholder_color)

        before = "*" * self._cursor if self.password else self.value[: self._cursor]
        cursor_x = self._font.size(before)[0]

        scroll = 0
        if cursor_x - scroll > inner_w:
            scroll = cursor_x - inner_w
        elif cursor_x - scroll < 0:
            scroll = cursor_x

        self.screen.set_clip((x + pad, y, inner_w, h))
        ty = y + (h - text_img.get_height()) // 2
        self.screen.blit(text_img, (x + pad - scroll, ty))
        if self.focused and self._cursor_visible():
            cx = x + pad - scroll + cursor_x + 1
            pygame.draw.line(
                self.screen, self.text_color, (cx, y + 4), (cx, y + h - 4), 2
            )
        self.screen.set_clip(None)


class Dropdown(Widget):
    """A select / combo box.

    Clicking the header toggles the option panel. Selecting an item fires
    ``on_select(index, value)``. The hovered item is highlighted via
    :meth:`on_mouse_move`, which FreeFrame calls on ``MOUSEMOTION``.
    """

    def __init__(
        self,
        screen,
        coordinates: Tuple[int, int],
        width: int,
        height: int = 30,
        options: Optional[List] = None,
        selected_index: int = -1,
        font=None,
        size: int = 22,
        theme: "Theme" = None,
        text_color: Color = (30, 30, 30),
        bg_color: Color = (255, 255, 255),
        border_color: Color = (120, 120, 130),
        open_bg_color: Color = (245, 245, 250),
        item_hover_color: Color = (220, 232, 245),
        border_radius: int = 0,
        on_select: Optional[Callable[[int, object], None]] = None,
    ):
        super().__init__(screen, coordinates)
        self.size = (width, height)
        if theme is not None:
            bg_color = theme.surface
            border_color = theme.border
            text_color = theme.text
            open_bg_color = theme.background
            item_hover_color = theme.primary
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.open_bg_color = open_bg_color
        self.item_hover_color = item_hover_color
        self.border_radius = border_radius
        self.options: List = list(options or [])
        self.selected_index = (
            selected_index if 0 <= selected_index < len(self.options) else -1
        )
        self.open = False
        self._hover_index = -1
        self.on_select = on_select
        try:
            self._font = pygame.font.Font(font, size)
        except TypeError:
            self._font = font

    # -- selection --------------------------------------------------------
    def set_options(self, options: List) -> None:
        self.options = list(options)
        if self.selected_index >= len(self.options):
            self.selected_index = -1

    def get_selected(self):
        """Return ``(index, value)`` of the current selection, or ``(-1, None)``."""
        if 0 <= self.selected_index < len(self.options):
            return self.selected_index, self.options[self.selected_index]
        return -1, None

    def set_selected(self, index: int) -> None:
        if 0 <= index < len(self.options):
            self.selected_index = index

    # -- interaction ------------------------------------------------------
    def _in_header(self, pos: Tuple[int, int]) -> bool:
        x, y = self.coordinates
        w, h = self.size
        return x <= pos[0] <= x + w and y <= pos[1] <= y + h

    def on_mouse_move(self, pos: Tuple[int, int]) -> None:
        if not self.open:
            self._hover_index = -1
            return
        x, y = self.coordinates
        w, h = self.size
        py = y + h
        if x <= pos[0] <= x + w and py <= pos[1] <= py + h * len(self.options):
            self._hover_index = (pos[1] - py) // h
        else:
            self._hover_index = -1

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        x, y = self.coordinates
        w, h = self.size
        if not self.open:
            if self._in_header(pos):
                self.open = True
                return True
            return False
        # open state
        py = y + h
        if self._in_header(pos):
            self.open = False
            return True
        if x <= pos[0] <= x + w and py <= pos[1] <= py + h * len(self.options):
            idx = (pos[1] - py) // h
            if 0 <= idx < len(self.options):
                self.selected_index = idx
                self.open = False
                if self.on_select is not None:
                    self.on_select(idx, self.options[idx])
                return True
        self.open = False
        return False

    # -- rendering --------------------------------------------------------
    def _draw_triangle(self, cx: int, cy: int, color: Color, open: bool) -> None:
        if open:
            pts = [(cx - 5, cy - 3), (cx + 5, cy - 3), (cx, cy + 4)]
        else:
            pts = [(cx - 5, cy + 3), (cx + 5, cy + 3), (cx, cy - 4)]
        pygame.draw.polygon(self.screen, color, pts)

    def draw(self) -> None:
        x, y = self.coordinates
        w, h = self.size
        pygame.draw.rect(
            self.screen, self.bg_color, (x, y, w, h), border_radius=self.border_radius
        )
        pygame.draw.rect(
            self.screen, self.border_color, (x, y, w, h), 1, border_radius=self.border_radius
        )
        label = ""
        if 0 <= self.selected_index < len(self.options):
            label = str(self.options[self.selected_index])
        img = self._font.render(label, True, self.text_color)
        self.screen.blit(img, (x + 6, y + (h - img.get_height()) // 2))
        self._draw_triangle(x + w - 14, y + h // 2, self.border_color, self.open)

        if self.open and self.options:
            py = y + h
            ph = h * len(self.options)
            self.screen.set_clip((x, py, w, ph))
            for i, opt in enumerate(self.options):
                iy = py + i * h
                bg = self.item_hover_color if i == self._hover_index else self.open_bg_color
                pygame.draw.rect(self.screen, bg, (x, iy, w, h))
                pygame.draw.rect(self.screen, self.border_color, (x, iy, w, h), 1)
                oimg = self._font.render(str(opt), True, self.text_color)
                self.screen.blit(oimg, (x + 6, iy + (h - oimg.get_height()) // 2))
            self.screen.set_clip(None)


class Switch(Widget):
    """A horizontal on/off toggle switch."""

    def __init__(
        self,
        screen,
        coordinates: Tuple[int, int],
        width: int = 50,
        height: int = 26,
        checked: bool = False,
        on_color: Color = (70, 130, 180),
        off_color: Color = (150, 150, 160),
        knob_color: Color = (255, 255, 255),
        on_change: Optional[Callable[[bool], None]] = None,
        theme: "Theme" = None,
    ):
        super().__init__(screen, coordinates)
        self.size = (width, height)
        if theme is not None:
            on_color = theme.primary
        self.checked = checked
        self.on_color = on_color
        self.off_color = off_color
        self.knob_color = knob_color
        self.on_change = on_change

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        if self.contains(pos):
            self.checked = not self.checked
            if self.on_change is not None:
                self.on_change(self.checked)
            return True
        return False

    def draw(self) -> None:
        x, y = self.coordinates
        w, h = self.size
        r = h // 2
        track = self.on_color if self.checked else self.off_color
        pygame.draw.circle(self.screen, track, (x + r, y + r), r)
        pygame.draw.circle(self.screen, track, (x + w - r, y + r), r)
        pygame.draw.rect(self.screen, track, (x + r, y, w - 2 * r, h))
        kx = x + w - r - 2 if self.checked else x + r + 2
        pygame.draw.circle(self.screen, self.knob_color, (kx, y + r), r - 3)


class RadioButton(Widget):
    """A single radio button; belongs to a :class:`RadioGroup` for single-select."""

    def __init__(
        self,
        screen,
        coordinates: Tuple[int, int],
        size: int = 20,
        label: str = "",
        checked: bool = False,
        value=None,
        color: Color = (70, 130, 180),
        border_color: Color = (60, 60, 70),
        text_color: Color = (30, 30, 30),
        font=None,
        font_size: int = 18,
        group=None,
        on_select: Optional[Callable[["RadioButton"], None]] = None,
        theme: "Theme" = None,
    ):
        super().__init__(screen, coordinates)
        self.size = (size, size)
        if theme is not None:
            color = theme.primary
            border_color = theme.border
            text_color = theme.text
        self.checked = checked
        self.label = label
        self.value = value if value is not None else label
        self.color = color
        self.border_color = border_color
        self.text_color = text_color
        self.group = group
        self.on_select = on_select
        try:
            self._font = pygame.font.Font(font, font_size)
        except TypeError:
            self._font = font

    def handle_click(self, pos: Tuple[int, int]) -> bool:
        if self.contains(pos):
            self.select()
            return True
        return False

    def select(self) -> None:
        if self.group is not None:
            self.group.select(self)
        else:
            self.checked = True
        if self.on_select is not None:
            self.on_select(self)

    def draw(self) -> None:
        x, y = self.coordinates
        s = self.size[0]
        r = s // 2
        cx, cy = x + r, y + r
        pygame.draw.circle(self.screen, self.border_color, (cx, cy), r, 1)
        if self.checked:
            pygame.draw.circle(self.screen, self.color, (cx, cy), r - 4)
        if self.label:
            img = self._font.render(self.label, True, self.text_color)
            self.screen.blit(img, (x + s + 6, y + (s - img.get_height()) // 2))


class RadioGroup:
    """A container that keeps at most one :class:`RadioButton` selected."""

    def __init__(self, on_change: Optional[Callable[[RadioButton], None]] = None):
        self.buttons: List[RadioButton] = []
        self.selected: Optional[RadioButton] = None
        self.on_change = on_change

    def add(self, button: RadioButton) -> "RadioGroup":
        button.group = self
        self.buttons.append(button)
        if button.checked and self.selected is None:
            self.selected = button
        return self

    def select(self, button: RadioButton) -> None:
        for b in self.buttons:
            b.checked = b is button
        self.selected = button
        if self.on_change is not None:
            self.on_change(button)

    def get_selected(self) -> Optional[RadioButton]:
        return self.selected
