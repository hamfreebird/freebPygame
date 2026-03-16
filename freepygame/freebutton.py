"""
Button components for Pygame UI development.

This module provides button classes and utility functions for creating interactive
buttons in Pygame applications, including rectangular buttons, circular buttons,
and click detection utilities.
"""

import pygame
import pygame.draw
import pygame.gfxdraw

from freepygame.freecircle import FreeCircle


def position_button(
    rect: tuple[int, int, int, int] | list[int, int, int, int], pos: tuple[int, int]
) -> bool:
    """
    Check if a point is inside a rectangle.

    Note: This function expects the rectangle in format (x1, x2, y1, y2),
    where x1 and x2 are the horizontal bounds, and y1 and y2 are the vertical bounds.

    Args:
        rect: Rectangle coordinates as (x1, x2, y1, y2) or [x1, x2, y1, y2]
        pos: Point coordinates as (x, y)

    Returns:
        True if the point is inside the rectangle, False otherwise.

    Example:
        >>> rect = (10, 60, 10, 40)  # x1=10, x2=60, y1=10, y2=40
        >>> position_button(rect, (25, 25))
        True
        >>> position_button(rect, (5, 5))
        False
    """
    if rect[0] <= pos[0] <= rect[1] and rect[2] <= pos[1] <= rect[3]:
        return True
    return False


def position_button_class(button, pos: tuple[int, int]) -> bool:
    """
    Check if a point is inside a button object.

    Note: For circular buttons (CircleButton), this function uses the bounding
    rectangle coordinates rather than checking the actual circular area.

    Args:
        button: Button object (FreeButton or CircleButton)
        pos: Point coordinates as (x, y)

    Returns:
        True if the point is inside the button's bounding area, False otherwise.

    Example:
        >>> button = FreeButton(screen, [100, 100], [200, 50], "Click me")
        >>> position_button_class(button, (150, 125))
        True
    """
    if (
        button.get_coordinates()[1][0] >= pos[0] >= button.get_coordinates()[0][0]
        and button.get_coordinates()[3][1] >= pos[1] >= button.get_coordinates()[0][1]
    ):
        return True
    return False


class FreeButton:
    """
    A customizable rectangular button for Pygame applications.

    This class provides a rectangular button with configurable appearance,
    including colors, borders, text, and scaling support.

    Attributes:
        check_button (bool): Whether the button should be checked for clicks
        display_button (bool): Whether the button should be displayed

    Example:
        >>> button = FreeButton(
        ...     screen=screen,
        ...     coordinates=[100, 100],
        ...     button_size=[200, 50],
        ...     msg="Click me",
        ...     button_color=(70, 130, 180),
        ...     text_color=(255, 255, 255)
        ... )
    """

    check_button = False
    display_button = True

    def __init__(
        self,
        screen,
        coordinates,
        button_size,
        msg,
        font="SimHei",
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
        """
        Initialize a FreeButton instance.

        Args:
            screen: Pygame surface to draw the button on
            coordinates: Button's top-left corner coordinates as [x, y]
            button_size: Button dimensions as [width, height]
            msg: Text to display on the button
            font: Font file path or Pygame font object (default: 'SimHei')
            size: Font size (default: 24)
            border_width: Border width in pixels (default: 1)
            draw_border: Whether to draw a border (default: True)
            draw_line: Whether to draw a decorative line (default: False)
            msg_tran: Whether the text background is transparent (default: False)
            line_width: Decorative line width in pixels (default: 1)
            button_color: Button background color as (R, G, B) (default: black)
            text_color: Text color as (R, G, B) (default: white)
            border_color: Border color as (R, G, B) (default: black)
            line_color: Decorative line color as (R, G, B) (default: white)
            dsm: Display scaling multiplier (default: 1)

        Note:
            When font is a string, it should be a path to a font file.
            Use None for the system default font.
        """
        self.msg = msg
        self.dsm = dsm
        self.screen = screen
        self.width = button_size[0] * self.dsm
        self.height = button_size[1] * self.dsm
        self.coordinates = coordinates
        self.coordinates[0] *= self.dsm
        self.coordinates[1] *= self.dsm
        self.button_color = button_color
        self.text_color = text_color
        self.draw_line = draw_line
        self.draw_border = draw_border
        self.border = [border_width, border_color]
        self.line = [line_width, line_color]
        self.msg_tran = msg_tran
        self.font = pygame.font.Font(font, size)
        self.rect = pygame.Rect(0, 0, self.width * self.dsm, self.height * self.dsm)
        self.rect.centerx = self.coordinates[0] + self.width / 2
        self.rect.centery = self.coordinates[1] + self.height / 2

    def draw(self):
        """
        Draw the button on the screen.

        This method renders the button with its current configuration,
        including background, border, text, and optional decorative line.
        """
        pygame.draw.rect(self.screen, self.button_color, self.rect)
        if self.draw_border:
            pygame.draw.rect(self.screen, self.border[1], self.rect, self.border[0])
        if self.draw_line:
            pygame.draw.line(
                self.screen,
                self.line[1],
                (self.rect.left, self.rect.centery),
                (self.rect.right, self.rect.centery),
                self.line[0],
            )
        if self.msg_tran:
            img_text = self.font.render(self.msg, True, self.text_color, None)
        else:
            img_text = self.font.render(
                self.msg, True, self.text_color, self.button_color
            )
        img_text_rect = img_text.get_rect()
        img_text_rect.center = self.rect.center
        self.screen.blit(img_text, img_text_rect)

    def get_coordinates(self):
        """
        Get the button's corner coordinates.

        Returns:
            List of four coordinate pairs representing the button's corners:
            [top-left, top-right, bottom-right, bottom-left]
        """
        return [
            [self.rect.left, self.rect.top],
            [self.rect.right, self.rect.top],
            [self.rect.right, self.rect.bottom],
            [self.rect.left, self.rect.bottom],
        ]

    def set_color(self, color):
        """
        Set the button's background color.

        Args:
            color: New background color as (R, G, B)
        """
        self.button_color = color

    def set_text_color(self, color):
        """
        Set the button's text color.

        Args:
            color: New text color as (R, G, B)
        """
        self.text_color = color

    def set_border_color(self, color):
        """
        Set the button's border color.

        Args:
            color: New border color as (R, G, B)
        """
        self.border[1] = color

    def set_line_color(self, color):
        """
        Set the button's decorative line color.

        Args:
            color: New line color as (R, G, B)
        """
        self.line[1] = color

    def set_msg(self, msg):
        """
        Set the button's text message.

        Args:
            msg: New text message
        """
        self.msg = msg

    def get_attribute(self):
        """
        Get the button's configuration attributes.

        Returns:
            Dictionary containing all button configuration attributes
        """
        attribute = {
            "screen": self.screen,
            "coordinates": self.coordinates,
            "button_size": [self.width, self.height],
            "msg": self.msg,
            "font": self.font,
            "size": self.font.get_height(),
            "border_width": self.border[0],
            "draw_border": self.draw_border,
            "draw_line": self.draw_line,
            "msg_tran": self.msg_tran,
            "line_width": self.line[0],
            "button_color": self.button_color,
            "text_color": self.text_color,
            "border_color": self.border[1],
            "line_color": self.line[1],
            "dsm": self.dsm,
        }
        return attribute

    def __str__(self):
        """Return string representation of the button."""
        return "FreeButton object"

    __repr__ = __str__


class CircleButton(FreeCircle):
    """
    A circular button for Pygame applications.

    This class extends FreeCircle to create a circular button with text support.
    It inherits all circle drawing capabilities and adds button-specific functionality.

    Attributes:
        check_button (bool): Whether the button should be checked for clicks
        display_button (bool): Whether the button should be displayed

    Example:
        >>> button = CircleButton(
        ...     screen=screen,
        ...     coordinates=[200, 200],
        ...     radius=50,
        ...     msg="OK",
        ...     button_color=(220, 100, 100),
        ...     msg_color=(255, 255, 255)
        ... )
    """

    check_button = False
    display_button = True

    def __init__(
        self,
        screen,
        coordinates,
        radius,
        msg,
        font="SimHei",
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
        """
        Initialize a CircleButton instance.

        Args:
            screen: Pygame surface to draw the button on
            coordinates: Circle center coordinates as [x, y]
            radius: Circle radius in pixels
            msg: Text to display on the button
            font: Font file path or Pygame font object (default: 'SimHei')
            size: Font size (default: 24)
            width: Line width (0 for filled circle) (default: 0)
            rect: Ellipse axes as (width, height) for elliptical buttons (default: (0, 0))
            angle: Angle range for arc drawing as (start_angle, end_angle) (default: (0, 360))
            aa: Whether to use anti-aliasing (default: True)
            draw_border: Whether to draw a border (default: False)
            border_width: Border width in pixels (default: 1)
            color: Circle color as (R, G, B) (default: black)
            border_color: Border color as (R, G, B) (default: black)
            msg_color: Text color as (R, G, B) (default: white)
            button_color: Button background color (alias for color) (default: black)
            msg_tran: Whether the text background is transparent (default: False)
            dsm: Display scaling multiplier (default: 1)
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
        self.msg = msg
        self.dsm = dsm
        self.msg_color = msg_color
        self.button_color = button_color
        self.msg_tran = msg_tran
        self.font = pygame.font.Font(font, size)

    def draw(self):
        """
        Draw the circular button on the screen.

        This method renders the circle with its current configuration,
        then draws the text centered within the circle.
        """
        super().draw()
        if self.msg_tran:
            img_text = self.font.render(self.msg, True, self.msg_color, None)
        else:
            img_text = self.font.render(
                self.msg, True, self.msg_color, self.button_color
            )
        img_text_rect = img_text.get_rect()
        img_text_rect.center = (self.coordinates[0], self.coordinates[1])
        self.screen.blit(img_text, img_text_rect)

    def set_msg(self, msg):
        """
        Set the button's text message.

        Args:
            msg: New text message
        """
        self.msg = msg

    def set_msg_color(self, color):
        """
        Set the button's text color.

        Args:
            color: New text color as (R, G, B)
        """
        self.msg_color = color

    def set_button_color(self, color):
        """
        Set the button's background color.

        Args:
            color: New background color as (R, G, B)
        """
        self.button_color = color
        self.color = color

    def get_attribute(self):
        """
        Get the button's configuration attributes.

        Returns:
            Dictionary containing all button configuration attributes
        """
        attribute = super().get_attribute()
        attribute.update(
            {
                "msg": self.msg,
                "msg_color": self.msg_color,
                "button_color": self.button_color,
                "msg_tran": self.msg_tran,
                "font": self.font,
                "size": self.font.get_height(),
                "dsm": self.dsm,
            }
        )
        return attribute

    def __str__(self):
        """Return string representation of the circular button."""
        return "CircleButton object"

    __repr__ = __str__
