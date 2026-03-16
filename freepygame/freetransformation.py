"""
Image transformation utilities for Pygame applications.

This module provides image processing functions for blur effects,
color averaging, and RGBA data manipulation.
"""

from typing import List, Tuple


def _array_mean(number_list: List[float]) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
        number_list: List of numbers to calculate the mean of

    Returns:
        The arithmetic mean of the numbers in the list

    Note:
        This is an internal utility function used by array_mean_rgba.
        Returns 0 if the list is empty to avoid ZeroDivisionError.

    Example:
        >>> _array_mean([1, 2, 3, 4, 5])
        3.0
        >>> _array_mean([])
        0.0
    """
    number_list_len = len(number_list) - 1
    number_list_array_mean = 0.0

    for number in range(0, number_list_len):
        number_list_array_mean += number_list[number]

    try:
        number_list_array_mean /= number_list_len + 1
    except ZeroDivisionError:
        number_list_array_mean = 0.0

    return number_list_array_mean


def array_mean_rgba(
    rgba: Tuple[List[int], List[int], List[int], List[int]],
) -> Tuple[int, int, int, int]:
    """
    Calculate the average RGBA color from separate channel lists.

    Args:
        rgba: A tuple containing four lists:
            - List of red channel values
            - List of green channel values
            - List of blue channel values
            - List of alpha channel values

    Returns:
        A tuple containing the average (R, G, B, A) values as integers

    Example:
        >>> reds = [100, 150, 200]
        >>> greens = [50, 100, 150]
        >>> blues = [0, 50, 100]
        >>> alphas = [255, 255, 255]
        >>> array_mean_rgba((reds, greens, blues, alphas))
        (150, 100, 50, 255)
    """
    r = int(_array_mean(rgba[0]))
    g = int(_array_mean(rgba[1]))
    b = int(_array_mean(rgba[2]))
    a = int(_array_mean(rgba[3]))

    return (r, g, b, a)


def map_to_rgba(
    part: List[List[Tuple[int, ...]]],
) -> Tuple[List[int], List[int], List[int], List[int]]:
    """
    Extract and separate RGBA channels from a 2D array of pixel data.

    Args:
        part: A 2D list of pixel tuples, where each pixel can be:
            - (R, G, B) for RGB format
            - (R, G, B, A) for RGBA format

    Returns:
        A tuple containing four lists:
            - List of red channel values
            - List of green channel values
            - List of blue channel values
            - List of alpha channel values (defaults to 255 if not provided)

    Note:
        If alpha channel is not provided in the pixel data, it defaults to 255 (fully opaque).

    Example:
        >>> pixels = [
        ...     [(255, 0, 0), (0, 255, 0)],
        ...     [(0, 0, 255), (255, 255, 255, 128)]
        ... ]
        >>> map_to_rgba(pixels)
        ([255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255], [255, 255, 255, 128])
    """
    r, g, b, a = [], [], [], []

    for x in range(0, len(part) - 1):
        for y in range(0, len(part) - 1):
            pixel = part[x][y]
            r.append(pixel[0])
            g.append(pixel[1])
            b.append(pixel[2])

            if len(pixel) == 4:
                a.append(pixel[3])
            else:
                a.append(255)  # Default alpha for RGB pixels

    return r, g, b, a


def image_blur_processing(image, level: int = 2):
    """
    Apply a box blur effect to a Pygame image surface.

    Args:
        image: Pygame Surface object to blur
        level: Blur intensity level (higher values = more blur, default: 2)

    Returns:
        The blurred Pygame Surface (modified in-place)

    Note:
        This function modifies the original image surface in-place.
        The blur is applied using a box blur algorithm with a kernel size
        determined by the level parameter.

    Example:
        >>> import pygame
        >>> pygame.init()
        >>> image = pygame.Surface((100, 100))
        >>> image.fill((255, 0, 0))
        >>> blurred_image = image_blur_processing(image, level=3)
        >>> # image is now blurred
    """
    _size = image.get_size()

    # Create 2D arrays for old and new pixel data
    _old_image_pixels = [[None for _ in range(0, _size[0])] for _ in range(0, _size[1])]
    _new_image_pixels = [[None for _ in range(0, _size[0])] for _ in range(0, _size[1])]

    boundary_width = level + 1

    # Extract all pixel data from the image
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            _old_image_pixels[x][y] = image.get_at((x, y))

    # Apply blur to each pixel
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            ready_part = []

            try:
                # Extract neighborhood pixels for blurring
                for unit in _old_image_pixels[x - boundary_width : x + boundary_width]:
                    ready_part.append(unit[y - boundary_width : y + boundary_width])

                # Calculate average color of neighborhood
                pixels = array_mean_rgba(map_to_rgba(ready_part))
            except IndexError:
                # Handle edge pixels by using a neutral gray
                pixels = (125, 125, 125, 125)

            _new_image_pixels[x][y] = pixels

    # Apply blurred pixels back to the image
    for x in range(0, _size[0]):
        for y in range(0, _size[1]):
            image.set_at((x, y), _new_image_pixels[x][y])

    return image
