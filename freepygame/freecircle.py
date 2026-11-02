"""
Circle components for Pygame UI development.

This module provides circle drawing classes and utility functions for creating
circles, arcs, ellipses, and other circular shapes in Pygame applications.

It is the canonical implementation for circle-related components and is
re-exported by the top-level ``freepygame`` package.
"""

from __future__ import annotations

import pygame
import pygame.draw
import pygame.gfxdraw


def _degree_to_radians(_degree: float) -> float:
    """
    Convert degrees to radians.

    Args:
        _degree: Angle in degrees

    Returns:
        Angle in radians
    """
    return _degree * float(6.283185307179586 / 360)


class FreeAllCircle:
    """Draw circles/arcs/ellipses (static helpers)."""

    @staticmethod
    def draw_circle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        width: int = 1,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Draw a plain circle."""
        pygame.draw.circle(screen, color, coordinates, radius, width)

    @staticmethod
    def draw_aacircle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Draw an anti-aliased hollow circle."""
        pygame.gfxdraw.aacircle(screen, coordinates[0], coordinates[1], radius, color)

    @staticmethod
    def draw_saacircle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Draw a solid (filled) circle."""
        pygame.gfxdraw.filled_circle(
            screen, coordinates[0], coordinates[1], radius, color
        )

    @staticmethod
    def draw_advanced_circle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        width: int = 1,
        rect: tuple[int, int] = (0, 0),
        angle: tuple[int, int] = (0, 360),
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Draw an advanced hollow circle or arc."""
        if rect == (0, 0):
            _rect = (
                coordinates[0] - radius,
                coordinates[1] - radius,
                radius * 2,
                radius * 2,
            )
        else:
            _rect = (
                coordinates[0] - rect[0],
                coordinates[1] - rect[1],
                rect[0] * 2,
                rect[1] * 2,
            )
        _angle = [_degree_to_radians(angle[0]), _degree_to_radians(angle[1])]
        pygame.draw.arc(screen, color, _rect, _angle[0], _angle[1], width)

    @staticmethod
    def draw_advanced_aacircle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        angle: tuple[int, int] = (0, 359),
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Draw an advanced anti-aliased hollow circle or arc."""
        pygame.gfxdraw.arc(
            screen, coordinates[0], coordinates[1], radius, angle[0], angle[1], color
        )

    @staticmethod
    def draw_advanced_aaellipse(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: tuple[int, int],
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """Draw an advanced anti-aliased hollow ellipse."""
        pygame.gfxdraw.aaellipse(
            screen, coordinates[0], coordinates[1], radius[0], radius[1], color
        )

    @staticmethod
    def draw_bezier(
        screen: pygame.Surface,
        points: list[tuple[int, int]],
        steps: int = 100,
        color: tuple[int, int, int] = (128, 128, 128),
    ) -> None:
        """Draw a B\u00e9zier curve through the given control points."""
        if len(points) < 2:
            return

        def bezier_point(t: float) -> tuple[float, float]:
            n = len(points) - 1
            x = 0.0
            y = 0.0
            for i, (px, py) in enumerate(points):
                coeff = math.comb(n, i) * (t**i) * ((1 - t) ** (n - i)) if n >= i else 0
                x += px * coeff
                y += py * coeff
            return (x, y)

        import math

        prev_point = bezier_point(0)
        for i in range(1, steps + 1):
            t = i / steps
            current_point = bezier_point(t)
            pygame.draw.line(
                screen,
                color,
                (int(prev_point[0]), int(prev_point[1])),
                (int(current_point[0]), int(current_point[1])),
                1,
            )
            prev_point = current_point


class FreeCircle:
    """A customizable circle / arc / curve object for Pygame applications."""

    check_circle = False
    display_circle = True

    def __init__(
        self,
        screen,
        coordinates,
        radius,
        width=1,
        rect=(0, 0),
        angle=(0, 360),
        aa=True,
        draw_border=False,
        border_width=1,
        color=(0, 0, 0),
        border_color=(0, 0, 0),
    ):
        self.screen = screen
        self.coordinates = coordinates
        self.radius = radius
        self.width = width
        self.rect = rect
        self.angle = angle
        self.aa = aa
        self.draw_border = draw_border
        self.border_width = border_width
        self.color = color
        self.border_color = border_color
        self._border_angle = [0, 360]
        super().__init__()

    def __str__(self):
        return """\u81ea\u5b9a\u4e49\u5706\uff0c\u5f27\uff0c\u66f2\u7ebf\u7c7b"""

    __repr__ = __str__

    def get_attribute(self):
        return {
            "screen": self.screen,
            "coordinates": self.coordinates,
            "radius": self.radius,
            "width": self.width,
            "rect": self.rect,
            "angle": self.angle,
            "aa": self.aa,
            "draw_border": self.draw_border,
            "border_width": self.border_width,
            "color": self.color,
            "border_color": self.border_color,
        }

    def get_center_coordinates(self):
        """Return the circle's center coordinates."""
        return self.coordinates

    def get_coordinates(self):
        """Return the circle's bounding-box coordinates (top-left, top-right,
        bottom-right, bottom-left). Only valid when rect == (0, 0)."""
        if self.rect == (0, 0):
            return [
                [self.coordinates[0] - self.radius, self.coordinates[1] - self.radius],
                [self.coordinates[0] + self.radius, self.coordinates[1] - self.radius],
                [self.coordinates[0] + self.radius, self.coordinates[1] + self.radius],
                [self.coordinates[0] - self.radius, self.coordinates[1] + self.radius],
            ]

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_radius(self, radius):
        self.radius = radius

    def set_width(self, width):
        self.width = width

    def set_rect(self, rect):
        self.rect = rect

    def set_angle(self, angle):
        self.angle = angle

    def set_aa(self, aa):
        self.aa = aa

    def open_border(self, draw_border: bool):
        self.draw_border = draw_border

    def set_border_width(self, border_width):
        self.border_width = border_width

    def set_color(self, color):
        self.color = color

    def set_border_color(self, border_color):
        self.border_color = border_color

    def _open_border_angle(self, _border_angle: tuple[int, int]):
        self._border_angle = list(_border_angle)

    def draw(self):
        """Draw the circle/arc/curve according to the current configuration."""
        try:
            if (
                self.aa is True
                and self.angle != (0, 360)
                and self.width != 0
                and self.rect == (0, 0)
            ):
                # Expand the arc by 1 degree on each end so the
                # anti-aliased endpoints render without gaps. We must NOT
                # mutate self.angle here: callers (e.g. get_attribute /
                # set_angle) expect the stored angle to remain unchanged.
                _arc_start = self.angle[0] - 1
                _arc_end = self.angle[1] + 1
                pygame.gfxdraw.arc(
                    self.screen,
                    self.coordinates[0],
                    self.coordinates[1],
                    self.radius,
                    _arc_start,
                    _arc_end,
                    self.color,
                )
            elif (
                self.aa is True
                and self.angle == (0, 360)
                and self.width != 0
                and self.rect == (0, 0)
            ):
                pygame.gfxdraw.aacircle(
                    self.screen,
                    self.coordinates[0],
                    self.coordinates[1],
                    self.radius,
                    self.color,
                )
            elif (
                self.aa is True
                and self.angle != (0, 360)
                and self.width != 0
                and self.rect != (0, 0)
            ):
                pygame.gfxdraw.aaellipse(
                    self.screen,
                    self.coordinates[0],
                    self.coordinates[1],
                    self.radius[0],
                    self.radius[1],
                    self.color,
                )
            elif (
                self.aa is True
                and self.angle == (0, 360)
                and self.width == 0
                and self.rect == (0, 0)
            ):
                pygame.gfxdraw.filled_circle(
                    self.screen,
                    self.coordinates[0],
                    self.coordinates[1],
                    self.radius,
                    self.color,
                )
            elif self.aa is False and self.angle == (0, 360) and self.rect == (0, 0):
                pygame.draw.circle(
                    self.screen, self.color, self.coordinates, self.radius, self.width
                )
            elif self.aa is False and self.angle == (0, 360):
                if self.rect == (0, 0):
                    _rect = (
                        self.coordinates[0] - self.radius,
                        self.coordinates[1] - self.radius,
                        self.radius * 2,
                        self.radius * 2,
                    )
                else:
                    _rect = (
                        self.coordinates[0] - self.rect[0],
                        self.coordinates[1] - self.rect[1],
                        self.rect[0] * 2,
                        self.rect[1] * 2,
                    )
                pygame.draw.ellipse(self.screen, self.color, _rect, self.width)
            elif self.aa is False and self.width != 0:
                if self.rect == (0, 0):
                    _rect = (
                        self.coordinates[0] - self.radius,
                        self.coordinates[1] - self.radius,
                        self.radius * 2,
                        self.radius * 2,
                    )
                else:
                    _rect = (
                        self.coordinates[0] - self.rect[0],
                        self.coordinates[1] - self.rect[1],
                        self.rect[0] * 2,
                        self.rect[1] * 2,
                    )
                _angle = [
                    _degree_to_radians(self.angle[0]),
                    _degree_to_radians(self.angle[1]),
                ]
                pygame.draw.arc(
                    self.screen, self.color, _rect, _angle[0], _angle[1], self.width
                )
            else:
                raise AssertionError(
                    "Unable to draw graphics with the parameters given -> "
                    "\u65e0\u6cd5\u7528\u7ed9\u5b9a\u7684\u53c2\u6570\u7ed8\u5236\u56fe\u5f62"
                )
            if (
                self.draw_border is True
                and self.border_width != 0
                and self._border_angle != [0, 360]
            ):
                if self.rect == (0, 0):
                    _rect = (
                        self.coordinates[0] - self.radius,
                        self.coordinates[1] - self.radius,
                        self.radius * 2,
                        self.radius * 2,
                    )
                else:
                    _rect = (
                        self.coordinates[0] - self.rect[0],
                        self.coordinates[1] - self.rect[1],
                        self.rect[0] * 2,
                        self.rect[1] * 2,
                    )
                _angle = [
                    _degree_to_radians(self._border_angle[0]),
                    _degree_to_radians(self._border_angle[1]),
                ]
                pygame.draw.arc(
                    self.screen,
                    self.border_color,
                    _rect,
                    _angle[0],
                    _angle[1],
                    self.border_width,
                )
            elif self.draw_border is True and self.border_width != 0:
                if self.rect == (0, 0):
                    _rect = (
                        self.coordinates[0] - self.radius,
                        self.coordinates[1] - self.radius,
                        self.radius * 2,
                        self.radius * 2,
                    )
                else:
                    _rect = (
                        self.coordinates[0] - self.rect[0],
                        self.coordinates[1] - self.rect[1],
                        self.rect[0] * 2,
                        self.rect[1] * 2,
                    )
                pygame.draw.ellipse(
                    self.screen, self.border_color, _rect, self.border_width
                )
        except Exception:
            raise AssertionError(
                "Unable to draw graphics with the parameters given -> "
                "\u65e0\u6cd5\u7528\u7ed9\u5b9a\u7684\u53c2\u6570\u7ed8\u5236\u56fe\u5f62"
            )

    def draw_bezier(self, surface, points, steps, color=(0, 0, 0)):
        """Draw a B\u00e9zier curve using this circle's color when color==self.color."""
        if color != self.color:
            pygame.gfxdraw.bezier(surface, points, steps, color)
        else:
            pygame.gfxdraw.bezier(surface, points, steps, self.color)


class SuperCircle(FreeCircle, FreeAllCircle):
    """Super circle class, inheriting FreeCircle and FreeAllCircle."""

    def __init__(
        self,
        screen,
        coordinates,
        radius,
        width=1,
        rect=(0, 0),
        angle=(0, 360),
        aa=True,
        draw_border=False,
        border_width=1,
        color=(0, 0, 0),
        border_color=(0, 0, 0),
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

    def __lshift__(self, data: tuple):
        """<< shortcut operator.

        Accepts a single tuple whose sole element selects the target:
        - ``<< (75,)``            -> set radius
        - ``<< ((80, 60),)``     -> set ellipse axes (rect)
        - ``<< ((255, 0, 0),)`` -> set color
        For convenience the unwrapped forms ``<< (80, 60)`` / ``<< (255,0,0)``
        are also accepted. Anything else raises AssertionError.
        """
        if len(data) == 1:
            item = data[0]
            if isinstance(item, tuple) and len(item) == 2:
                super().set_rect(item)
            elif isinstance(item, tuple) and len(item) == 3:
                super().set_color(item)
            else:
                super().set_radius(item)
        elif len(data) == 2:
            super().set_rect(data)
        elif len(data) == 3:
            super().set_color(data)
        else:
            raise AssertionError("Redundant parameter -> \u5192\u4f59\u53c2\u6570")

    def open_border_angle(self, angle: tuple[int, int]):
        """Enable an arc edge border: angle = (start, end)."""
        super()._open_border_angle(angle)

    @staticmethod
    def draw_scircle(screen, coordinates, radius, width=1, color=(0, 0, 0)):
        """Draw a plain circle (convenience wrapper)."""
        FreeAllCircle.draw_circle(screen, coordinates, radius, width, color)
