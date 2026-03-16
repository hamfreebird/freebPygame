"""
Icon components for Pygame UI development.

This module provides icon display classes for creating interactive
icons with multiple states in Pygame applications.
"""

from typing import List, Optional, Tuple, Union

import pygame


class FreeIcon:
    """
    A customizable icon component for Pygame applications.

    This class provides an icon that can switch between multiple image
    states, useful for creating interactive buttons, toggles, or
    state-based icons.

    Attributes:
        check_button (bool): Whether the icon should be checked for clicks
        display_button (bool): Whether the icon should be displayed
        rect_pos (List): List of rectangle positions for click detection

    Example:
        >>> # Load icon images
        >>> normal_icon = pygame.image.load("icon_normal.png")
        >>> hover_icon = pygame.image.load("icon_hover.png")
        >>>
        >>> # Create icon with two states
        >>> icon = FreeIcon(
        ...     screen=screen,
        ...     coordinates=[100, 100],
        ...     image_1=normal_icon,
        ...     image_2=hover_icon
        ... )
        >>>
        >>> # Switch to hover state
        >>> icon.set_index(1)
        >>>
        >>> # Draw the icon
        >>> icon.draw()
    """

    check_button = False
    display_button = True
    rect_pos: List[List[int]] = []

    def __init__(
        self,
        screen: pygame.Surface,
        coordinates: List[int],
        image_1: pygame.Surface,
        image_2: pygame.Surface,
        *additional_images: pygame.Surface,
    ):
        """
        Initialize a FreeIcon instance.

        Args:
            screen: Pygame surface to draw the icon on
            coordinates: Icon position as [x, y] (top-left corner)
            image_1: Primary icon image (state 0)
            image_2: Secondary icon image (state 1)
            *additional_images: Additional icon images for more states

        Note:
            Images should be Pygame Surface objects. They can be loaded
            using pygame.image.load() or created programmatically.
            The icon starts displaying image_1 (state 0).

        Example:
            >>> icon = FreeIcon(
            ...     screen=screen,
            ...     coordinates=[50, 50],
            ...     image_1=normal_img,
            ...     image_2=hover_img,
            ...     image_3=pressed_img
            ... )
        """
        self.screen = screen
        self.coordinates = coordinates
        self.images = [image_1, image_2, *additional_images]
        self.image_index = 0

        # Calculate bounding rectangle for click detection
        if self.images:
            first_image = self.images[0]
            self.rect = pygame.Rect(
                coordinates[0],
                coordinates[1],
                first_image.get_width(),
                first_image.get_height(),
            )
            self.rect_pos = [
                [self.rect.left, self.rect.top],
                [self.rect.right, self.rect.top],
                [self.rect.right, self.rect.bottom],
                [self.rect.left, self.rect.bottom],
            ]

    def set_index(self, index: int) -> None:
        """
        Set the current icon state by index.

        Args:
            index: Index of the image to display (0 for image_1, 1 for image_2, etc.)

        Raises:
            IndexError: If the index is out of range for the available images

        Example:
            >>> icon.set_index(0)  # Show normal state
            >>> icon.set_index(1)  # Show hover state
            >>> icon.set_index(2)  # Show pressed state (if available)
        """
        if 0 <= index < len(self.images):
            self.image_index = index
        else:
            raise IndexError(
                f"Icon index {index} out of range. Available indices: 0-{len(self.images) - 1}"
            )

    def get_index(self) -> int:
        """
        Get the current icon state index.

        Returns:
            Current image index (0 for image_1, 1 for image_2, etc.)

        Example:
            >>> current_state = icon.get_index()
            >>> print(f"Current icon state: {current_state}")
        """
        return self.image_index

    def draw(self) -> None:
        """
        Draw the current icon image on the screen.

        This method blits the currently selected image to the screen
        at the icon's coordinates.

        Example:
            >>> # In game loop:
            >>> icon.draw()
        """
        if 0 <= self.image_index < len(self.images):
            self.screen.blit(self.images[self.image_index], self.coordinates)

    def get_coordinates(self) -> List[List[int]]:
        """
        Get the icon's bounding rectangle coordinates.

        Returns:
            List of four coordinate pairs representing the icon's bounding box:
            [top-left, top-right, bottom-right, bottom-left]

        Note:
            This is useful for click detection using position_button_class()
            from the freebutton module.

        Example:
            >>> coords = icon.get_coordinates()
            >>> if position_button_class(icon, mouse_pos):
            >>>     print("Icon clicked!")
        """
        return self.rect_pos

    def set_position(self, coordinates: List[int]) -> None:
        """
        Set the icon's position.

        Args:
            coordinates: New position as [x, y] (top-left corner)

        Example:
            >>> icon.set_position([200, 150])
        """
        self.coordinates = coordinates
        if self.images:
            first_image = self.images[0]
            self.rect = pygame.Rect(
                coordinates[0],
                coordinates[1],
                first_image.get_width(),
                first_image.get_height(),
            )
            self.rect_pos = [
                [self.rect.left, self.rect.top],
                [self.rect.right, self.rect.top],
                [self.rect.right, self.rect.bottom],
                [self.rect.left, self.rect.bottom],
            ]

    def add_image(self, image: pygame.Surface) -> None:
        """
        Add an additional image state to the icon.

        Args:
            image: New icon image to add

        Example:
            >>> new_state_img = pygame.image.load("new_state.png")
            >>> icon.add_image(new_state_img)
            >>> icon.set_index(3)  # Switch to the new state
        """
        self.images.append(image)

    def get_attribute(self) -> dict:
        """
        Get the icon's configuration attributes.

        Returns:
            Dictionary containing all icon configuration attributes:
            - screen: The surface the icon is drawn on
            - coordinates: Current position [x, y]
            - image_count: Number of available image states
            - current_index: Currently displayed image index
            - rect: Bounding rectangle (left, top, width, height)

        Example:
            >>> attr = icon.get_attribute()
            >>> print(f"Icon at position: {attr['coordinates']}")
            >>> print(f"Available states: {attr['image_count']}")
        """
        return {
            "screen": self.screen,
            "coordinates": self.coordinates,
            "image_count": len(self.images),
            "current_index": self.image_index,
            "rect": (
                self.rect.left,
                self.rect.top,
                self.rect.width,
                self.rect.height,
            ),
        }

    def __str__(self) -> str:
        """
        Return string representation of the icon.

        Returns:
            String describing the icon's state and position
        """
        return (
            f"FreeIcon at ({self.coordinates[0]}, {self.coordinates[1]}) "
            f"with {len(self.images)} states (current: {self.image_index})"
        )

    __repr__ = __str__
