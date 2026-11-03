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

# The library is implemented across modular files (freebutton, freecircle,
# freetext, freeicon, freeparticle, freetransformation, freeframe). This
# package simply re-exports the canonical symbols so callers can do
# `from freepygame import FreeButton` etc.
from .freebutton import (
    CircleButton,
    Clickable,
    FreeButton,
    position_button,
    position_button_class,
)
from .freecircle import (
    FreeAllCircle,
    FreeCircle,
    SuperCircle,
    _degree_to_radians,
)
from .freetext import FreeText, SuperText
from .freeicon import FreeAARectangle, FreeIcon, Point
from .freeparticle import Fireworks, Particle, ParticleEngine, explode
from .freetransformation import (
    _array_mean,
    array_mean_rgba,
    image_blur_processing,
    map_to_rgba,
)
from .freetheme import THEMES, Theme, apply_theme, get_theme
from .freewidget import (
    CheckBox,
    Dropdown,
    InputBox,
    ProgressBar,
    RadioButton,
    RadioGroup,
    Slider,
    Switch,
    Widget,
)
from .freelayout import AnchorLayout, HBox, Layout, VBox
from .freeframe import FreeFrame

# Define __all__ for "from freepygame import *"
__all__ = [
    # Button components
    "FreeButton",
    "CircleButton",
    "Clickable",
    "position_button",
    "position_button_class",
    # Circle components
    "FreeCircle",
    "SuperCircle",
    "FreeAllCircle",
    # Text components
    "FreeText",
    "SuperText",
    # Other components
    "FreeIcon",
    "Point",
    "FreeAARectangle",
    # Particle system
    "Particle",
    "ParticleEngine",
    "Fireworks",
    "explode",
    # Image processing
    "image_blur_processing",
    "array_mean_rgba",
    "map_to_rgba",
    # Internal helpers
    "_degree_to_radians",
    "_array_mean",
    # Window / app framework
    "FreeFrame",
    # Theme system
    "Theme",
    "THEMES",
    "get_theme",
    "apply_theme",
    # Widgets
    "Widget",
    "ProgressBar",
    "Slider",
    "CheckBox",
    "InputBox",
    "Dropdown",
    "Switch",
    "RadioButton",
    "RadioGroup",
    # Layout managers
    "Layout",
    "VBox",
    "HBox",
    "AnchorLayout",
    # Version info
    "__version__",
    "__author__",
    "__license__",
]
