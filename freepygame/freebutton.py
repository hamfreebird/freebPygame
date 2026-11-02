"""
Button components for Pygame UI development.

This module provides button classes and click-detection utilities for Pygame
applications, including rectangular buttons, circular buttons, and helper
functions.

It is the canonical implementation for button components and is re-exported by
the top-level ``freepygame`` package.
"""

from __future__ import annotations

import pygame
import pygame.draw
import pygame.gfxdraw

from .freecircle import FreeCircle


def position_button(
    rect: tuple[int, int, int, int] | list[int, int, int, int], pos: tuple[int, int]
) -> bool:
    """
    Check if a point is inside a rectangle.

    Note: ``rect`` is expected as (x1, x2, y1, y2), i.e. the horizontal then
    vertical bounds.
    """
    if rect[0] <= pos[0] <= rect[1] and rect[2] <= pos[1] <= rect[3]:
        return True
    return False


def position_button_class(button, pos: tuple[int, int]) -> bool:
    """
    Check if a point is inside a button object.

    For circular buttons (CircleButton) this uses the bounding rectangle of the
    circle, not the actual circular area.
    """
    coords = button.get_coordinates()
    if (
        coords[1][0] >= pos[0] >= coords[0][0]
        and coords[3][1] >= pos[1] >= coords[0][1]
    ):
        return True
    return False


class Clickable:
    """Mixin adding click-callback support to any component with ``get_coordinates()``.

    Register a callback via :meth:`set_callback` and dispatch pointer clicks with
    :meth:`handle_click`. Works for both rectangular (:class:`FreeButton`) and
    circular (:class:`CircleButton`) controls since both expose ``get_coordinates``.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_click_callback = None
        self.enabled = True

    def set_callback(self, callback):
        """Register ``callback(self)`` to run when the component is clicked."""
        self.on_click_callback = callback

    def handle_click(self, pos):
        """Return ``True`` if ``pos`` is inside the component and the click was
        consumed (the callback fires when registered). Disabled components
        ignore all clicks."""
        if not self.enabled:
            return False
        if position_button_class(self, pos):
            if self.on_click_callback is not None:
                self.on_click_callback(self)
            return True
        return False


class FreeButton(Clickable):
    """A customizable rectangular button for Pygame applications."""

    check_button = False
    display_button = True

    def __init__(
        self,
        screen,
        coordinates,
        button_size,
        msg,
        font=None,
        size=24,
        border_width=1,
        draw_border=True,
        draw_line=False,
        msg_tran=False,
        line_width=1,
        button_color=(0, 0, 0),
        text_color=(255, 255, 255),
        border_color=(0, 0, 0),
        line_color=(255, 255, 255),
        dsm=1,
    ):
        super().__init__()
        self.msg = msg
        self.dsm = dsm
        self.screen = screen
        self.width = button_size[0] * self.dsm
        self.height = button_size[1] * self.dsm
        # Copy the caller's list so we never mutate their input in place.
        self.coordinates = list(coordinates)
        self.coordinates[0] *= self.dsm
        self.coordinates[1] *= self.dsm
        self.button_color = button_color
        self.text_color = text_color
        self.draw_line = draw_line
        self.draw_border = draw_border
        self.border = [border_width, border_color]
        self.line = [line_width, line_color]
        self.msg_tran = msg_tran
        try:
            self.font = pygame.font.Font(font, size)
        except TypeError:
            self.font = font
        self.rect = pygame.Rect(0, 0, int(self.width), int(self.height))
        self.rect.centerx = self.coordinates[0] + self.width / 2
        self.rect.centery = self.coordinates[1] + self.height / 2
        self.msg_img = self.font.render(
            self.msg, True, self.text_color, self.button_color
        )
        if self.msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def __str__(self):
        return """\u57fa\u7840\u6309\u94ae\u7c7b"""

    __repr__ = __str__

    def get_attribute(self):
        return {
            "screen": self.screen,
            "coordinates": [self.coordinates[0], self.coordinates[1]],
            "button_size": [self.width, self.height],
            "msg": self.msg,
            "draw_border": self.draw_border,
            "draw_line": self.draw_line,
            "border_width": self.border[0],
            "line_width": self.line[0],
            "text_color": self.text_color,
            "button_color": self.button_color,
            "border_color": self.border[1],
            "line_color": self.line[1],
        }

    def get_coordinates(self):
        return [
            [self.coordinates[0], self.coordinates[1]],
            [self.coordinates[0] + self.width, self.coordinates[1]],
            [self.coordinates[0] + self.width, self.coordinates[1] + self.height],
            [self.coordinates[0], self.coordinates[1] + self.height],
        ]

    def open_line(self, draw_line: bool):
        self.draw_line = draw_line

    def open_border(self, draw_border: bool):
        self.draw_border = draw_border

    def set_msg(self, msg):
        self.msg = msg
        self.msg_img = self.font.render(
            self.msg, True, self.text_color, self.button_color
        )
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_line_color(self, color):
        self.line[1] = color

    def set_msg_color(self, color):
        self.text_color = color
        self.msg_img = self.font.render(
            self.msg, True, self.text_color, self.button_color
        )
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_border_color(self, color):
        self.border[1] = color

    def set_button_color(self, color):
        self.button_color = color
        self.msg_img = self.font.render(
            self.msg, True, self.text_color, self.button_color
        )
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_text_color(self, color):
        self.text_color = color
        self.msg_img = self.font.render(self.msg, True, color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center

    def set_line_width(self, width):
        self.line[0] = width

    def set_border_width(self, width):
        self.border[0] = width

    def set_msg_tran(self, msg_tran):
        if msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.msg_tran = msg_tran

    def draw(self):
        if self.msg_tran is False:
            self.screen.fill(self.button_color, self.rect)
        if self.draw_line is True:
            pygame.draw.line(
                self.screen,
                self.line[1],
                (self.coordinates[0], self.coordinates[1]),
                (self.coordinates[0] + self.width, self.coordinates[1] + self.height),
                self.line[0],
            )
            pygame.draw.line(
                self.screen,
                self.line[1],
                (self.coordinates[0] + self.width, self.coordinates[1]),
                (self.coordinates[0], self.coordinates[1] + self.height),
                self.line[0],
            )
        if self.msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.screen.blit(self.msg_img, self.msg_img_rect)
        if self.draw_border is True:
            pygame.draw.rect(
                self.screen,
                self.border[1],
                (self.coordinates[0], self.coordinates[1], self.width, self.height),
                self.border[0],
            )


class CircleButton(FreeCircle, Clickable):
    """A circular button for Pygame applications."""

    check_button = False
    display_button = True

    def __init__(
        self,
        screen,
        coordinates,
        radius,
        msg,
        font=None,
        size=24,
        width=0,
        rect=(0, 0),
        angle=(0, 360),
        aa=True,
        draw_border=False,
        border_width=1,
        color=(0, 0, 0),
        border_color=(0, 0, 0),
        msg_color=(255, 255, 255),
        button_color=(0, 0, 0),
        msg_tran=False,
        dsm=1,
    ):
        super().__init__(
            screen,
            coordinates,
            radius,
            width,
            rect,
            angle,
            aa,
            draw_border,
            border_width,
            color,
            border_color,
        )
        self.msg = msg
        self.dsm = dsm
        try:
            self._font = pygame.font.Font(font, size)
        except TypeError:
            self._font = font
        self.button_color = button_color
        self.size = size
        self.msg_color = msg_color
        self.msgrect = pygame.Rect(0, 0, rect[0] * self.dsm, rect[1] * self.dsm)
        self.msgrect.centerx = self.coordinates[0] * self.dsm
        self.msgrect.centery = self.coordinates[1] * self.dsm
        self.msg_tran = msg_tran
        self.msg_img = self._font.render(
            self.msg, True, self.msg_color, self.button_color
        )
        if self.msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.msgrect.center

    def draw(self):
        super().draw()
        if self.msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.screen.blit(self.msg_img, self.msg_img_rect)

    def set_button_color(self, color):
        self.button_color = color
        self.color = color
        self.msg_img = self._font.render(
            self.msg, True, self.msg_color, self.button_color
        )
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.msgrect.center

    def set_msg_color(self, color):
        self.msg_color = color
        self.msg_img = self._font.render(
            self.msg, True, self.msg_color, self.button_color
        )
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.msgrect.center

    def set_msg(self, msg):
        self.msg = msg
        self.msg_img = self._font.render(
            self.msg, True, self.msg_color, self.button_color
        )
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.msgrect.center

    def set_msg_tran(self, msg_tran):
        if msg_tran is True:
            self.msg_img.set_colorkey(self.button_color)
        self.msg_tran = msg_tran
