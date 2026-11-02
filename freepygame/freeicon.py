"""
Icon components for Pygame UI development.

This module provides icon and simple primitive drawing classes for Pygame
applications: a multi-state :class:`FreeIcon`, a :class:`Point`, and an
anti-aliased rectangle :class:`FreeAARectangle`.

It is the canonical implementation for icon-related components and is
re-exported by the top-level ``freepygame`` package.
"""

from __future__ import annotations

import pygame
import pygame.gfxdraw


class FreeIcon:
    """A customizable icon component that can switch between image states."""

    check_button = False
    display_button = True
    rect_pos = []

    def __init__(self, screen, coordinates, image_1, image_2):
        self.screen = screen
        self.coordinates = coordinates
        self.image = [image_1, image_2]
        self.image_index = 0

    def set_index(self, index: int):
        self.image_index = index

    def draw(self):
        self.screen.blit(self.image[self.image_index], self.coordinates)


class Point:
    """A simple drawable point (filled circle)."""

    def __init__(self, screen, coordinates, r, color=(0, 0, 0)):
        self.screen = screen
        self.coordinates = coordinates
        self.r = r
        self.color = color

    def move(self, coordinates):
        self.coordinates = coordinates

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.coordinates, self.r)


class FreeAARectangle:
    """An anti-aliased rectangle primitive."""

    def __init__(self, screen, coordinates, size, color=(0, 0, 0)):
        self.screen = screen
        self.coordinates = coordinates
        self.size = size
        self.color = color

    def get_attribute(self):
        return {
            "screen": self.screen,
            "coordinates": self.coordinates,
            "size": self.size,
            "color": self.color,
        }

    def det_coordinates(self):
        return [
            [self.coordinates[0], self.coordinates[1]],
            [self.coordinates[0] + self.size[0], self.coordinates[1]],
            [self.coordinates[0] + self.size[0], self.coordinates[1] + self.size[1]],
            [self.coordinates[0], self.coordinates[1] + self.size[1]],
        ]

    def get_center_coordinates(self):
        return [
            self.coordinates[0] + int(self.size[0] / 2),
            self.coordinates[1] + int(self.size[1] / 2),
        ]

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_size(self, size):
        self.size = size

    def set_color(self, color):
        self.color = color

    def draw(self):
        pygame.gfxdraw.rectangle(
            self.screen,
            (self.coordinates[0], self.coordinates[1], self.size[0], self.size[1]),
            self.color,
        )
