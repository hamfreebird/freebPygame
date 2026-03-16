"""
Circle components for Pygame UI development.

This module provides circle drawing classes and utility functions for creating
circles, arcs, ellipses, and other circular shapes in Pygame applications.
"""

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

    Note:
        This is an internal utility function used for angle conversion.
    """
    return _degree * float(6.283185307179586 / 360)


class FreeAllCircle:
    """
    A collection of static methods for drawing circles and related shapes.

    This class provides various circle drawing methods as static utilities,
    including basic circles, anti-aliased circles, arcs, and ellipses.

    All methods are static and can be used without instantiating the class.
    """

    @staticmethod
    def draw_circle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        width: int = 1,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """
        Draw a basic circle.

        Args:
            screen: Pygame surface to draw on
            coordinates: Center coordinates as (x, y)
            radius: Circle radius in pixels
            width: Line width (0 for filled circle, default: 1)
            color: Circle color as (R, G, B) (default: black)

        Example:
            >>> FreeAllCircle.draw_circle(screen, (100, 100), 50, 2, (255, 0, 0))
        """
        pygame.draw.circle(screen, color, coordinates, radius, width)

    @staticmethod
    def draw_aacircle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """
        Draw an anti-aliased hollow circle.

        Args:
            screen: Pygame surface to draw on
            coordinates: Center coordinates as (x, y)
            radius: Circle radius in pixels
            color: Circle color as (R, G, B) (default: black)

        Note:
            This method uses anti-aliasing for smoother edges but only draws
            the outline (hollow circle).

        Example:
            >>> FreeAllCircle.draw_aacircle(screen, (100, 100), 50, (0, 255, 0))
        """
        pygame.gfxdraw.aacircle(screen, coordinates[0], coordinates[1], radius, color)

    @staticmethod
    def draw_saacircle(
        screen: pygame.Surface,
        coordinates: tuple[int, int],
        radius: int,
        color: tuple[int, int, int] = (0, 0, 0),
    ) -> None:
        """
        Draw a solid (filled) circle.

        Args:
            screen: Pygame surface to draw on
            coordinates: Center coordinates as (x, y)
            radius: Circle radius in pixels
            color: Circle color as (R, G, B) (default: black)

        Example:
            >>> FreeAllCircle.draw_saacircle(screen, (100, 100), 50, (0, 0, 255))
        """
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
        """
        Draw an advanced hollow circle or arc.

        Args:
            screen: Pygame surface to draw on
            coordinates: Center coordinates as (x, y)
            radius: Circle radius in pixels
            width: Line width (default: 1)
            rect: Ellipse axes as (width, height) for elliptical shapes.
                  Use (0, 0) for circular shapes (default: (0, 0))
            angle: Angle range in degrees as (start_angle, end_angle) (default: (0, 360))
            color: Circle color as (R, G, B) (default: black)

        Note:
            When angle is not (0, 360), this draws an arc instead of a full circle.

        Example:
            >>> # Draw a full circle
            >>> FreeAllCircle.draw_advanced_circle(screen, (100, 100), 50, 2, (0, 0), (0, 360), (255, 0, 0))
            >>> # Draw a quarter circle (90-degree arc)
            >>> FreeAllCircle.draw_advanced_circle(screen, (100, 100), 50, 2, (0, 0), (0, 90), (0, 255, 0))
        """
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
        """
        Draw an advanced anti-aliased hollow circle or arc.

        Args:
            screen: Pygame surface to draw on
            coordinates: Center coordinates as (x, y)
            radius: Circle radius in pixels
            angle: Angle range in degrees as (start_angle, end_angle) (default: (0, 359))
            color: Circle color as (R, G, B) (default: black)

        Note:
            This method uses anti-aliasing for smoother edges.
            The angle range is exclusive of the end angle (359 instead of 360).

        Example:
            >>> FreeAllCircle.draw_advanced_aacircle(screen, (100, 100), 50, (0, 180), (255, 255, 0))
        """
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
        """
        Draw an advanced anti-aliased hollow ellipse.

        Args:
            screen: Pygame surface to draw on
            coordinates: Center coordinates as (x, y)
            radius: Ellipse axes as (horizontal_radius, vertical_radius)
            color: Ellipse color as (R, G, B) (default: black)

        Example:
            >>> FreeAllCircle.draw_advanced_aaellipse(screen, (100, 100), (60, 30), (128, 0, 128))
        """
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
        """
        Draw a Bézier curve through the given points.

        Args:
            screen: Pygame surface to draw on
            points: List of control points as [(x1, y1), (x2, y2), ...]
            steps: Number of line segments to approximate the curve (default: 100)
            color: Curve color as (R, G, B) (default: gray)

        Note:
            This method draws a smooth curve through the control points
            using Bézier interpolation.

        Example:
            >>> points = [(100, 100), (200, 50), (300, 150), (400, 100)]
            >>> FreeAllCircle.draw_bezier(screen, points, 50, (0, 0, 255))
        """
        if len(points) < 2:
            return

        def bezier_point(t: float) -> tuple[float, float]:
            """Calculate a point on the Bézier curve at parameter t."""
            n = len(points) - 1
            x = 0.0
            y = 0.0
            for i, (px, py) in enumerate(points):
                # Bernstein polynomial
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
    """
    A customizable circle object for Pygame applications.

    This class provides a circle object with configurable appearance,
    including radius, color, border, and arc support.
    """

    check_circle = False
    display_circle = True

    def __init__(
        self,
        screen: pygame.Surface,
        coordinates: list[int],
        radius: int,
        width: int = 0,
        rect: tuple[int, int] = (0, 0),
        angle: tuple[int, int] = (0, 360),
        aa: bool = True,
        draw_border: bool = False,
        border_width: int = 1,
        color: tuple[int, int, int] = (0, 0, 0),
        border_color: tuple[int, int, int] = (0, 0, 0),
    ):
        """
        Initialize a FreeCircle instance.

        Args:
            screen: Pygame surface to draw the circle on
            coordinates: Circle center coordinates as [x, y]
            radius: Circle radius in pixels
            width: Line width (0 for filled circle, default: 0)
            rect: Ellipse axes as (width, height) for elliptical shapes (default: (0, 0))
            angle: Angle range in degrees as (start_angle, end_angle) (default: (0, 360))
            aa: Whether to use anti-aliasing (default: True)
            draw_border: Whether to draw a border (default: False)
            border_width: Border width in pixels (default: 1)
            color: Circle color as (R, G, B) (default: black)
            border_color: Border color as (R, G, B) (default: black)

        Example:
            >>> circle = FreeCircle(
            ...     screen=screen,
            ...     coordinates=[200, 200],
            ...     radius=50,
            ...     width=2,
            ...     color=(255, 0, 0)
            ... )
        """
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

    def draw(self) -> None:
        """
        Draw the circle on the screen.

        This method renders the circle with its current configuration,
        including optional border and anti-aliasing.
        """
        if self.aa:
            if self.width == 0:  # Filled circle
                FreeAllCircle.draw_saacircle(
                    self.screen,
                    (self.coordinates[0], self.coordinates[1]),
                    self.radius,
                    self.color,
                )
            else:  # Hollow circle
                FreeAllCircle.draw_aacircle(
                    self.screen,
                    (self.coordinates[0], self.coordinates[1]),
                    self.radius,
                    self.color,
                )
        else:
            FreeAllCircle.draw_circle(
                self.screen,
                (self.coordinates[0], self.coordinates[1]),
                self.radius,
                self.width,
                self.color,
            )

        if self.draw_border:
            FreeAllCircle.draw_circle(
                self.screen,
                (self.coordinates[0], self.coordinates[1]),
                self.radius,
                self.border_width,
                self.border_color,
            )

    def set_color(self, color: tuple[int, int, int]) -> None:
        """
        Set the circle's color.

        Args:
            color: New circle color as (R, G, B)
        """
        self.color = color

    def set_border_color(self, color: tuple[int, int, int]) -> None:
        """
        Set the circle's border color.

        Args:
            color: New border color as (R, G, B)
        """
        self.border_color = color

    def set_radius(self, radius: int) -> None:
        """
        Set the circle's radius.

        Args:
            radius: New radius in pixels
        """
        self.radius = radius

    def get_coordinates(self) -> list[list[int]]:
        """
        Get the circle's bounding box coordinates.

        Returns:
            List of four coordinate pairs representing the bounding box:
            [top-left, top-right, bottom-right, bottom-left]
        """
        x, y = self.coordinates
        r = self.radius
        return [
            [x - r, y - r],
            [x + r, y - r],
            [x + r, y + r],
            [x - r, y + r],
        ]

    def get_attribute(self) -> dict:
        """
        Get the circle's configuration attributes.

        Returns:
            Dictionary containing all circle configuration attributes
        """
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

    def __str__(self) -> str:
        """Return string representation of the circle."""
        return "FreeCircle object"

    __repr__ = __str__


class SuperCircle(FreeCircle):
    """
    An enhanced circle class with additional features.

    This class extends FreeCircle with operator overloading support
    for easier property modification.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        coordinates: list[int],
        radius: int,
        width: int = 0,
        rect: tuple[int, int] = (0, 0),
        angle: tuple[int, int] = (0, 360),
        aa: bool = True,
        draw_border: bool = False,
        border_width: int = 1,
        color: tuple[int, int, int] = (0, 0, 0),
        border_color: tuple[int, int, int] = (0, 0, 0),
    ):
        """
        Initialize a SuperCircle instance.

        Args:
            screen: Pygame surface to draw the circle on
            coordinates: Circle center coordinates as [x, y]
            radius: Circle radius in pixels
            width: Line width (0 for filled circle, default: 0)
            rect: Ellipse axes as (width, height) for elliptical shapes (default: (0, 0))
            angle: Angle range in degrees as (start_angle, end_angle) (default: (0, 360))
            aa: Whether to use anti-aliasing (default: True)
            draw_border: Whether to draw a border (default: False)
            border_width: Border width in pixels (default: 1)
            color: Circle color as (R, G, B) (default: black)
            border_color: Border color as (R, G, B) (default: black)
        """
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

    def __lshift__(self, value: tuple) -> "SuperCircle":
        """
        Overload the << operator for property setting.

        Args:
            value: Tuple containing property values in specific order:
                  - Single value: sets radius
                  - Tuple of two values: sets ellipse axes
                  - Tuple of three values: sets color

        Returns:
            self for method chaining

        Example:
            >>> circle << (50,)           # Set radius to 50
            >>> circle << ((60, 30),)     # Set ellipse axes to (60, 30)
            >>> circle << ((255, 0, 0),)  # Set color to red
        """
        if isinstance(value, tuple):
            if len(value) == 1:
                if isinstance(value[0], tuple) and len(value[0]) == 2:
                    # Set ellipse axes
                    self.rect = value[0]
                elif isinstance(value[0], tuple) and len(value[0]) == 3:
                    # Set color
                    self.color = value[0]
                else:
                    # Set radius
                    self.radius = value[0]
        return self
