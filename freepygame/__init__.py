"""
freepygame - A comprehensive Pygame UI controls library.

This library provides a collection of UI components and utilities for Pygame game
development, including buttons, text rendering, circles, icons, particle systems,
and image processing tools.

Version: 0.1.0
Author: freebird
License: Apache License 2.0

Example usage:
    >>> import pygame
    >>> from freepygame import FreeButton, FreeText
    >>>
    >>> pygame.init()
    >>> screen = pygame.display.set_mode((800, 600))
    >>>
    >>> # Create a button
    >>> button = FreeButton(
    ...     screen=screen,
    ...     coordinates=[100, 100],
    ...     button_size=[200, 50],
    ...     msg="Click me",
    ...     button_color=(70, 130, 180),
    ...     text_color=(255, 255, 255)
    ... )
    >>>
    >>> # Create text
    >>> text = FreeText(
    ...     screen=screen,
    ...     coordinates=[100, 170],
    ...     msg="Hello, freepygame!",
    ...     color=(0, 0, 0)
    ... )
"""

__version__ = "0.1.0"
__author__ = "freebird"
__license__ = "Apache License 2.0"

# Export main classes
from .freebutton import CircleButton, FreeButton, position_button, position_button_class
from .freecircle import FreeAllCircle, FreeCircle, SuperCircle
from .freeicon import FreeIcon
from .freeparticle import Fireworks, Particle, ParticleEngine, explode

# Export all content from freepygamelib
from .freepygamelib import *
from .freetext import FreeMsg, FreeText, MidSuperText, NaSuperText, SuperText
from .freetransformation import array_mean_rgba, image_blur_processing, map_to_rgba

# Define __all__ for "from freepygame import *"
__all__ = [
    # Button components
    "FreeButton",
    "CircleButton",
    "position_button",
    "position_button_class",
    # Circle components
    "FreeCircle",
    "SuperCircle",
    "FreeAllCircle",
    # Text components
    "FreeText",
    "SuperText",
    "NaSuperText",
    "MidSuperText",
    "FreeMsg",
    # Other components
    "FreeIcon",
    # Particle system
    "Particle",
    "ParticleEngine",
    "Fireworks",
    "explode",
    # Image processing
    "image_blur_processing",
    "array_mean_rgba",
    "map_to_rgba",
    # Version info
    "__version__",
    "__author__",
    "__license__",
]
