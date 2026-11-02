"""
Text components for Pygame UI development.

This module provides text rendering classes for creating and displaying text in
Pygame applications, including basic text and scaled ("super") text.

It is the canonical implementation for text components and is re-exported by the
top-level ``freepygame`` package.
"""

from __future__ import annotations

import pygame


class FreeText:
    """A basic text rendering class for Pygame applications."""

    check_text = False
    display_text = True

    def __init__(
        self, screen, coordinates, msg, font=None, size=24, color=(0, 0, 0)
    ):
        self.screen, self.msg, self.font, self.size, self.color = (
            screen,
            msg,
            font,
            size,
            color,
        )
        self.x, self.y = coordinates[0], coordinates[1]
        try:
            self._font = pygame.font.Font(font, size)
        except TypeError:
            self._font = font
        self.img_text = self._font.render(self.msg, True, color)

    def __str__(self):
        return """\u81ea\u5b9a\u4e49\u6587\u672c\u7c7b"""

    __repr__ = __str__

    def get_attribute(self):
        return {
            "screen": self.screen,
            "coordinates": [self.x, self.y],
            "msg": self.msg,
            "font": self.font,
            "size": self.size,
            "color": self.color,
        }

    def get_coordinates(self):
        return [self.x, self.y]

    def set_color(self, color):
        """Change the text color (re-renders and stores the new color)."""
        self.color = color
        try:
            self._font = pygame.font.Font(self.font, self.size)
        except TypeError:
            self._font = self.font
        self.img_text = self._font.render(self.msg, True, color)

    def set_fout(self, font):
        """Change the font (re-renders and stores the new font)."""
        self.font = font
        try:
            self._font = pygame.font.Font(font, self.size)
        except TypeError:
            self._font = font
        self.img_text = self._font.render(self.msg, True, self.color)

    def set_size(self, size):
        """Change the font size (re-renders and stores the new size)."""
        self.size = size
        try:
            self._font = pygame.font.Font(self.font, size)
        except TypeError:
            self._font = self.font
        self.img_text = self._font.render(self.msg, True, self.color)

    def set_msg(self, msg):
        """Change the text content (re-renders and stores the new message)."""
        self.msg = msg
        try:
            self._font = pygame.font.Font(self.font, self.size)
        except TypeError:
            self._font = self.font
        self.img_text = self._font.render(msg, True, self.color)

    def set_coordinates(self, coordinates):
        self.x, self.y = coordinates[0], coordinates[1]

    def draw(self):
        self.screen.blit(self.img_text, (self.x, self.y))


class SuperText(FreeText):
    """Super text class with display-scaling (dsm) support."""

    def __init__(
        self, screen, coordinates, msg, font=None, size=24, color=(0, 0, 0), dsm=1
    ):
        super().__init__(screen, coordinates, msg, font, size, color)
        self.msg_len_next = -1
        self.dsm = dsm

    def draw(self):
        self.screen.blit(self.img_text, (self.x * self.dsm, self.y * self.dsm))

    def __del__(self):
        return super().get_attribute()

    def __add__(self, data):
        """Concatenate text using a string or another SuperText's message."""
        if type(data) == SuperText:
            super().set_msg(self.msg + data.get_attribute().get("msg"))
        elif type(data) == str:
            super().set_msg(self.msg + data)
        else:
            super().set_msg(self.msg + str(data))
        return super().get_attribute().get("msg")

    def __lshift__(self, data: tuple):
        """<< shortcut: 1 element=font size, 2=elements position, 3=color."""
        if len(data) == 1:
            super().set_size(data[0])
        elif len(data) == 2:
            super().set_coordinates(data)
        elif len(data) == 3:
            super().set_color(data)
        else:
            raise AssertionError("Redundant parameter -> \u5192\u4f59\u53c2\u6570")

    def __len__(self):
        return len(super().get_attribute())

    def __iter__(self):
        self.msg_len_next = -1
        return super().get_attribute().get("msg")

    def __next__(self):
        self.msg_len_next += 1
        if self.msg_len_next >= len(super().get_attribute().get("msg")):
            raise StopIteration
        return super().get_attribute().get("msg")[self.msg_len_next]
