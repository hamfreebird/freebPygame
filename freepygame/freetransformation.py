"""
Image transformation utilities for Pygame applications.

This module provides image-processing functions for blur effects, color
averaging, and RGBA data manipulation.

It is the canonical implementation for image transformations and is re-exported
by the top-level ``freepygame`` package.
"""

from __future__ import annotations

import pygame
from typing import List, Tuple


def _array_mean(number_list: List[float]) -> float:
    """
    Calculate the arithmetic mean of a list of numbers.

    Returns 0.0 for an empty list to avoid ZeroDivisionError.
    """
    if not number_list:
        return 0.0
    return sum(number_list) / len(number_list)


def array_mean_rgba(
    rgba: Tuple[List[int], List[int], List[int], List[int]],
) -> Tuple[int, int, int, int]:
    """
    Calculate the average RGBA color from separate channel lists.

    ``rgba`` is a tuple of four lists: (R values, G values, B values, A values).
    Returns the average (R, G, B, A) as integers.
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

    Each pixel may be (R, G, B) or (R, G, B, A). Missing alpha defaults to 255
    only for RGBA pixels; for pixels that never carry alpha, the returned alpha
    list is empty.
    """
    r, g, b, a = [], [], [], []

    for x in range(0, len(part)):
        for y in range(0, len(part[x])):
            pixel = part[x][y]
            r.append(pixel[0])
            g.append(pixel[1])
            b.append(pixel[2])
            if len(pixel) == 4:
                a.append(pixel[3])

    return r, g, b, a


def image_blur_processing(image, level: int = 2):
    """
    Apply a box-blur effect to a Pygame image surface (in-place).

    Uses a fast NumPy / SurfaceArray path when available and falls back to a
    corrected per-pixel loop otherwise. Returns the SAME surface object it was
    given (modified in place).
    """
    try:
        import numpy as np
        from pygame import surfarray
    except Exception:
        return _image_blur_fallback(image, level)

    arr = surfarray.array3d(image).astype(np.int32)  # (width, height, 3)
    w, h, _ = arr.shape
    k = max(0, int(level))
    if k == 0:
        return image

    acc = np.zeros_like(arr)
    xs = np.arange(w)
    ys = np.arange(h)
    for dx in range(-k, k + 1):
        for dy in range(-k, k + 1):
            x_idx = np.clip(xs + dx, 0, w - 1)
            y_idx = np.clip(ys + dy, 0, h - 1)
            acc += arr[np.ix_(x_idx, y_idx)]
    acc //= (2 * k + 1) ** 2

    has_alpha = bool(image.get_flags() & pygame.SRCALPHA)
    try:
        if has_alpha:
            alpha = surfarray.array_alpha(image)
            rgba = np.dstack((acc, alpha)).astype(np.uint8)
            surfarray.blit_array(image, rgba)
        else:
            surfarray.blit_array(image, acc.astype(np.uint8))
    except Exception:
        return _image_blur_fallback(image, level)
    return image


def _image_blur_fallback(image, level):
    """Corrected per-pixel box-blur fallback (no NumPy dependency)."""
    w, h = image.get_size()
    k = max(0, int(level))
    if k == 0:
        return image

    old = [[image.get_at((x, y)) for y in range(h)] for x in range(w)]
    new = [[None for _ in range(h)] for _ in range(w)]
    has_alpha = bool(image.get_flags() & pygame.SRCALPHA)

    for x in range(w):
        for y in range(h):
            x0, x1 = max(0, x - k), min(w - 1, x + k)
            y0, y1 = max(0, y - k), min(h - 1, y + k)
            neighborhood = [
                [old[i][j] for j in range(y0, y1 + 1)] for i in range(x0, x1 + 1)
            ]
            color = array_mean_rgba(map_to_rgba(neighborhood))
            if not has_alpha:
                color = color[:3]
            new[x][y] = color

    for x in range(w):
        for y in range(h):
            image.set_at((x, y), new[x][y])
    return image
