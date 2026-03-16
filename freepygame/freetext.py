"""
Text components for Pygame UI development.

This module provides text rendering classes for creating and displaying
text in Pygame applications, including basic text, scaled text, and
text with various alignment options.
"""

import pygame


class FreeText:
    """
    A basic text rendering class for Pygame applications.

    This class provides simple text rendering with configurable font,
    size, color, and position.

    Attributes:
        check_text (bool): Whether the text should be checked for updates
        display_text (bool): Whether the text should be displayed

    Example:
        >>> text = FreeText(
        ...     screen=screen,
        ...     coordinates=[100, 100],
        ...     msg="Hello, World!",
        ...     font=None,
        ...     size=24,
        ...     color=(255, 255, 255)
        ... )
    """

    check_text = False
    display_text = True

    def __init__(
        self,
        screen: pygame.Surface,
        coordinates: list[int],
        msg: str,
        font: str = "SimHei",
        size: int = 24,
        color: tuple[int, int, int] = (0, 0, 0),
    ):
        """
        Initialize a FreeText instance.

        Args:
            screen: Pygame surface to draw the text on
            coordinates: Text position as [x, y] (top-left corner)
            msg: Text content to display
            font: Font file path or Pygame font object (default: 'SimHei')
            size: Font size in points (default: 24)
            color: Text color as (R, G, B) (default: black)

        Note:
            When font is a string, it should be a path to a font file.
            Use None for the system default font.
        """
        self.screen = screen
        self.msg = msg
        self.font = font
        self.size = size
        self.color = color
        self.x, self.y = coordinates[0], coordinates[1]

        try:
            self._font = pygame.font.Font(font, size)
        except TypeError:
            self._font = font

        self.img_text = self._font.render(self.msg, True, color)

    def draw(self) -> None:
        """
        Draw the text on the screen.

        This method renders the text with its current configuration
        and blits it to the screen at the specified coordinates.
        """
        self.screen.blit(self.img_text, (self.x, self.y))

    def set_color(self, color: tuple[int, int, int]) -> None:
        """
        Set the text color.

        Args:
            color: New text color as (R, G, B)
        """
        self.color = color
        self.img_text = self._font.render(self.msg, True, color)

    def set_msg(self, msg: str) -> None:
        """
        Set the text content.

        Args:
            msg: New text content
        """
        self.msg = msg
        self.img_text = self._font.render(self.msg, True, self.color)

    def set_font(self, font: str) -> None:
        """
        Set the text font.

        Args:
            font: New font file path or Pygame font object
        """
        self.font = font
        try:
            self._font = pygame.font.Font(font, self.size)
        except TypeError:
            self._font = font
        self.img_text = self._font.render(self.msg, True, self.color)

    def set_size(self, size: int) -> None:
        """
        Set the font size.

        Args:
            size: New font size in points
        """
        self.size = size
        try:
            self._font = pygame.font.Font(self.font, size)
        except TypeError:
            self._font = self.font
        self.img_text = self._font.render(self.msg, True, self.color)

    def set_position(self, coordinates: list[int]) -> None:
        """
        Set the text position.

        Args:
            coordinates: New position as [x, y] (top-left corner)
        """
        self.x, self.y = coordinates[0], coordinates[1]

    def get_coordinates(self) -> list[int]:
        """
        Get the text position.

        Returns:
            Text position as [x, y]
        """
        return [self.x, self.y]

    def get_attribute(self) -> dict:
        """
        Get the text configuration attributes.

        Returns:
            Dictionary containing all text configuration attributes
        """
        return {
            "screen": self.screen,
            "coordinates": [self.x, self.y],
            "msg": self.msg,
            "font": self.font,
            "size": self.size,
            "color": self.color,
        }

    def __str__(self) -> str:
        """Return string representation of the text object."""
        return "FreeText object"

    __repr__ = __str__


class SuperText(FreeText):
    """
    An enhanced text class with scaling support.

    This class extends FreeText to add display scaling multiplier (dsm)
    support for high-DPI displays and zoom functionality.

    Example:
        >>> text = SuperText(
        ...     screen=screen,
        ...     coordinates=[100, 100],
        ...     msg="Scaled Text",
        ...     size=24,
        ...     color=(255, 255, 255),
        ...     dsm=1.5
        ... )
    """

    def __init__(
        self,
        screen: pygame.Surface,
        coordinates: list[int],
        msg: str,
        font: str = "SimHei",
        size: int = 24,
        color: tuple[int, int, int] = (0, 0, 0),
        dsm: float = 1.0,
    ):
        """
        Initialize a SuperText instance.

        Args:
            screen: Pygame surface to draw the text on
            coordinates: Text position as [x, y] (top-left corner)
            msg: Text content to display
            font: Font file path or Pygame font object (default: 'SimHei')
            size: Font size in points (default: 24)
            color: Text color as (R, G, B) (default: black)
            dsm: Display scaling multiplier (default: 1.0)
        """
        super().__init__(screen, coordinates, msg, font, size, color)
        self.dsm = dsm
        self.msg_len_next = -1

    def draw(self) -> None:
        """
        Draw the scaled text on the screen.

        This method renders the text with scaling applied and blits it
        to the screen at the scaled coordinates.
        """
        scaled_x = int(self.x * self.dsm)
        scaled_y = int(self.y * self.dsm)
        self.screen.blit(self.img_text, (scaled_x, scaled_y))

    def __lshift__(self, value: tuple) -> "SuperText":
        """
        Overload the << operator for property setting.

        Args:
            value: Tuple containing property values in specific order:
                  - Single value: sets font size
                  - Tuple of two values: sets position
                  - Tuple of three values: sets color

        Returns:
            self for method chaining

        Example:
            >>> text << (36,)           # Set font size to 36
            >>> text << (200, 150)      # Set position to (200, 150)
            >>> text << (255, 0, 0)     # Set color to red
        """
        if isinstance(value, tuple):
            if len(value) == 1:
                self.set_size(value[0])
            elif len(value) == 2:
                self.set_position([value[0], value[1]])
            elif len(value) == 3:
                self.set_color(value)
        return self

    def __add__(self, text: str) -> "SuperText":
        """
        Overload the + operator for text concatenation.

        Args:
            text: String to append to current text

        Returns:
            self for method chaining

        Example:
            >>> text = SuperText(screen, [100, 100], "Hello")
            >>> text + " World!"  # Text becomes "Hello World!"
        """
        self.set_msg(self.msg + text)
        return self

    def get_attribute(self) -> dict:
        """
        Get the text configuration attributes including scaling.

        Returns:
            Dictionary containing all text configuration attributes
        """
        attr = super().get_attribute()
        attr["dsm"] = self.dsm
        return attr
