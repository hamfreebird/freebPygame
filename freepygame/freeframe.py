"""
Frame and window management utilities for Pygame applications.

This module provides a template application framework with built-in
FPS display, event handling, and time display functionality.
It serves as a starting point for creating Pygame applications
with proper window management and timing.

Example:
    >>> from freepygame.freeframe import FreeFrame
    >>>
    >>> # Create and run a basic application
    >>> app = FreeFrame(
    ...     title="My Application",
    ...     size=(800, 600),
    ...     fps=60
    ... )
    >>> app.run()
"""

import time
from typing import Optional, Tuple

import pygame
import pygame.colordict
import pygame.draw

from freepygame.freetext import SuperText


class FreeFrame:
    """
    A template application framework for Pygame.

    This class provides a complete application framework with window
    management, event handling, FPS display, and time display.
    It's designed to be extended for specific application needs.

    Attributes:
        title (str): Window title
        size (Tuple[int, int]): Window dimensions (width, height)
        fps (int): Target frames per second
        screen (pygame.Surface): Main display surface
        clock (pygame.time.Clock): Game clock for timing
        running (bool): Whether the application is running
        event_text (SuperText): Text display for time and FPS information

    Example:
        >>> class MyApp(FreeFrame):
        ...     def __init__(self):
        ...         super().__init__(
        ...             title="My Game",
        ...             size=(1024, 768),
        ...             fps=60
        ...         )
        ...         # Add your custom initialization here
        ...
        ...     def update(self):
        ...         # Add your game logic here
        ...         pass
        ...
        ...     def draw(self):
        ...         # Add your drawing code here
        ...         pass
        >>>
        >>> if __name__ == "__main__":
        ...     app = MyApp()
        ...     app.run()
    """

    def __init__(
        self,
        title: str = "freebird application",
        size: Tuple[int, int] = (720, 480),
        fps: int = 60,
        icon_path: Optional[str] = None,
        background_color: Tuple[int, int, int] = (0, 0, 0),
    ):
        """
        Initialize a FreeFrame application.

        Args:
            title: Window title (default: "freebird application")
            size: Window dimensions as (width, height) (default: (720, 480))
            fps: Target frames per second (default: 60)
            icon_path: Path to window icon file (default: None)
            background_color: Background color as (R, G, B) (default: black)

        Note:
            The application uses hardware acceleration (HWSURFACE) and
            double buffering (DOUBLEBUF) for better performance.
        """
        pygame.init()

        self.title = title
        self.size = size
        self.fps = fps
        self.background_color = background_color
        self.running = False

        # Set up display
        pygame.display.set_caption(title)

        if icon_path:
            try:
                icon = pygame.image.load(icon_path)
                pygame.display.set_icon(icon)
            except (FileNotFoundError, pygame.error) as e:
                print(f"Warning: Could not load icon from {icon_path}: {e}")

        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
        self.clock = pygame.time.Clock()

        # Create event text display (shows time and FPS)
        self.event_text = SuperText(
            screen=self.screen,
            coordinates=[3, 5],
            msg="",
            font=None,  # Use system default font
            size=10,
            color=pygame.colordict.THECOLORS.get("grey70"),
        )

        # Optional buffer surface for advanced rendering
        self.buffer = pygame.Surface(size)

    def handle_events(self) -> None:
        """
        Handle Pygame events.

        This method processes the event queue and handles common events
        like window close (QUIT). Override this method to add custom
        event handling.

        Note:
            The base implementation only handles the QUIT event.
            Override to add keyboard, mouse, or other event handling.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self) -> None:
        """
        Update application state.

        This method is called once per frame and should contain
        game logic, physics updates, and state changes.

        Note:
            This is an abstract method that should be overridden
            in subclasses. The base implementation does nothing.
        """
        pass

    def draw(self) -> None:
        """
        Draw the application.

        This method is called once per frame and should contain
        all drawing code for the current frame.

        Note:
            This is an abstract method that should be overridden
            in subclasses. The base implementation only draws
            the time and FPS display.
        """
        # Update time and FPS display
        current_time = time.localtime()
        time_str = (
            f"Time: {current_time.tm_year}-{current_time.tm_mon:02d}-"
            f"{current_time.tm_mday:02d} {current_time.tm_hour:02d}:"
            f"{current_time.tm_min:02d}:{current_time.tm_sec:02d}  "
            f"FPS: {int(self.clock.get_fps())}  "
            f"Copyright (c) {current_time.tm_year} freebird"
        )
        self.event_text.set_msg(time_str)
        self.event_text.draw()

    def run(self) -> None:
        """
        Run the application main loop.

        This method starts the application and runs the main game loop
        until the application is stopped (usually by closing the window).

        The main loop follows this pattern each frame:
        1. Handle events
        2. Update application state
        3. Clear screen
        4. Draw everything
        5. Update display
        6. Control frame rate

        Example:
            >>> app = FreeFrame()
            >>> app.run()  # Starts the application
        """
        self.running = True

        while self.running:
            # Handle events
            self.handle_events()

            # Update game state
            self.update()

            # Clear screen
            self.screen.fill(self.background_color)

            # Draw everything
            self.draw()

            # Update display
            pygame.display.flip()

            # Control frame rate
            self.clock.tick(self.fps)

        self.quit()

    def quit(self) -> None:
        """
        Clean up and quit the application.

        This method performs cleanup and properly shuts down Pygame.
        It's called automatically when the application exits.
        """
        pygame.quit()

    def get_fps(self) -> float:
        """
        Get the current frames per second.

        Returns:
            Current FPS as a float

        Example:
            >>> fps = app.get_fps()
            >>> print(f"Current FPS: {fps:.1f}")
        """
        return self.clock.get_fps()

    def set_title(self, title: str) -> None:
        """
        Set the window title.

        Args:
            title: New window title

        Example:
            >>> app.set_title("My Awesome Game")
        """
        self.title = title
        pygame.display.set_caption(title)

    def set_background_color(self, color: Tuple[int, int, int]) -> None:
        """
        Set the background color.

        Args:
            color: New background color as (R, G, B)

        Example:
            >>> app.set_background_color((30, 30, 30))
        """
        self.background_color = color

    def __str__(self) -> str:
        """
        Return string representation of the application.

        Returns:
            String describing the application state
        """
        return (
            f"FreeFrame(title='{self.title}', size={self.size}, "
            f"fps={self.fps}, running={self.running})"
        )

    __repr__ = __str__


def main():
    """
    Example usage of the FreeFrame class.

    This function demonstrates how to use the FreeFrame class
    to create a simple application with time and FPS display.
    """
    # Create a simple application
    app = FreeFrame(
        title="FreeFrame Example",
        size=(800, 600),
        fps=60,
        background_color=(20, 20, 40),
    )

    # Custom drawing example
    original_draw = app.draw

    def custom_draw():
        """Custom drawing function that adds a moving circle."""
        # Call the original draw method (shows time and FPS)
        original_draw()

        # Add a moving circle
        current_time = time.time()
        circle_x = 400 + int(
            200 * pygame.math.Vector2(1, 0).rotate(current_time * 100).x
        )
        circle_y = 300 + int(
            150 * pygame.math.Vector2(0, 1).rotate(current_time * 80).y
        )

        pygame.draw.circle(
            app.screen,
            (100, 200, 255),
            (circle_x, circle_y),
            30,
            2,
        )

    app.draw = custom_draw

    # Run the application
    print("Starting FreeFrame example application...")
    print("Close the window to exit.")
    app.run()


if __name__ == "__main__":
    main()
