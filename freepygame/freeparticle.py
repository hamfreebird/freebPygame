"""
Particle system components for Pygame applications.

This module provides particle system classes for creating visual effects
such as explosions, fire, smoke, and fireworks in Pygame games.
"""

import math
import random
from typing import List, Optional, Tuple

import pygame

# Color constants for particle effects
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)


class Particle(pygame.sprite.Sprite):
    """
    A single particle for particle system effects.

    This class represents an individual particle with position, velocity,
    acceleration, lifespan, and visual properties.

    Attributes:
        image (pygame.Surface): The visual representation of the particle
        rect (pygame.Rect): The bounding rectangle of the particle
        pos (pygame.math.Vector2): Current position of the particle
        velocity (pygame.math.Vector2): Current velocity of the particle
        acceleration (pygame.math.Vector2): Current acceleration of the particle
        lifespan (int): Remaining lifetime of the particle in frames

    Example:
        >>> particle = Particle(
        ...     pos=(100, 100),
        ...     velocity=(2, -3),
        ...     acceleration=(0, 0.1),
        ...     lifespan=60
        ... )
    """

    def __init__(
        self,
        pos: Tuple[float, float],
        velocity: Tuple[float, float],
        acceleration: Tuple[float, float],
        lifespan: int,
        color: Tuple[int, int, int] = WHITE,
        size: int = 2,
    ):
        """
        Initialize a Particle instance.

        Args:
            pos: Initial position as (x, y) coordinates
            velocity: Initial velocity as (vx, vy)
            acceleration: Constant acceleration as (ax, ay)
            lifespan: Lifetime in frames before particle disappears
            color: Particle color as (R, G, B) (default: white)
            size: Particle size in pixels (default: 2)

        Note:
            Positive y velocity moves downward (screen coordinates).
            Acceleration is typically (0, 0.1) for gravity effects.
        """
        super().__init__()
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(velocity)
        self.acceleration = pygame.math.Vector2(acceleration)
        self.lifespan = lifespan
        self.color = color
        self.size = size

    def update(self) -> None:
        """
        Update the particle's state for one frame.

        This method applies physics (velocity + acceleration) to update
        the particle's position and decreases its lifespan. Particles
        are automatically removed when their lifespan reaches zero.
        """
        self.velocity += self.acceleration
        self.pos += self.velocity
        self.lifespan -= 1

        # Update visual position
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Fade out effect based on remaining lifespan
        if self.lifespan < 30:
            alpha = int(255 * (self.lifespan / 30))
            self.image.set_alpha(alpha)

        if self.lifespan <= 0:
            self.kill()


class ParticleEngine:
    """
    A particle system engine for managing multiple particles.

    This class provides methods to generate, update, and draw
    collections of particles for various visual effects.

    Attributes:
        particles (pygame.sprite.Group): Group containing all active particles

    Example:
        >>> engine = ParticleEngine()
        >>> engine.generate_particles(50, (400, 300))
        >>> # In game loop:
        >>> engine.update_particles()
        >>> engine.draw_particles(screen)
    """

    def __init__(self):
        """Initialize an empty ParticleEngine instance."""
        self.particles = pygame.sprite.Group()

    def generate_particles(
        self,
        num_particles: int,
        pos: Tuple[float, float],
        velocity_range: Tuple[float, float] = (-3, 3),
        color: Optional[Tuple[int, int, int]] = None,
        size_range: Tuple[int, int] = (1, 4),
        lifespan_range: Tuple[int, int] = (30, 90),
    ) -> None:
        """
        Generate a burst of particles at a specific position.

        Args:
            num_particles: Number of particles to generate
            pos: Center position for particle generation as (x, y)
            velocity_range: Range for random velocity components (min, max)
            color: Particle color (random if None)
            size_range: Range for random particle sizes (min, max)
            lifespan_range: Range for random particle lifespans (min, max)

        Example:
            >>> engine.generate_particles(
            ...     num_particles=100,
            ...     pos=(400, 300),
            ...     velocity_range=(-5, 5),
            ...     color=(255, 100, 0),
            ...     lifespan_range=(40, 80)
            ... )
        """
        for _ in range(num_particles):
            # Random velocity in all directions
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(velocity_range[0], velocity_range[1])
            velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed,
            )

            # Random acceleration (slight gravity)
            acceleration = (0, random.uniform(0.05, 0.15))

            # Random lifespan
            lifespan = random.randint(lifespan_range[0], lifespan_range[1])

            # Random or specified color
            if color is None:
                particle_color = (
                    random.randint(200, 255),
                    random.randint(100, 200),
                    random.randint(0, 100),
                )
            else:
                particle_color = color

            # Random size
            size = random.randint(size_range[0], size_range[1])

            particle = Particle(
                pos=pos,
                velocity=velocity,
                acceleration=acceleration,
                lifespan=lifespan,
                color=particle_color,
                size=size,
            )
            self.particles.add(particle)

    def update_particles(self) -> None:
        """
        Update all particles in the engine.

        This method should be called once per frame to update
        particle positions, velocities, and lifespans.
        """
        self.particles.update()

    def draw_particles(self, surface: pygame.Surface) -> None:
        """
        Draw all particles to a surface.

        Args:
            surface: Pygame surface to draw particles on
        """
        self.particles.draw(surface)

    def clear_particles(self) -> None:
        """Remove all particles from the engine."""
        self.particles.empty()


class Fireworks:
    """
    A fireworks effect with multiple explosion stages.

    This class creates a realistic fireworks effect with a rising
    trail and colorful explosion particles.

    Attributes:
        x (float): Current x position
        y (float): Current y position
        color (Tuple[int, int, int]): Primary color of the firework
        velocity (float): Vertical velocity
        exploded (bool): Whether the firework has exploded
        trail_particles (List): List of trail particles
        explosion_particles (List): List of explosion particles

    Example:
        >>> firework = Fireworks(400, 600, RED)
        >>> # In game loop:
        >>> firework.update()
        >>> firework.draw(screen)
    """

    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        """
        Initialize a Fireworks instance.

        Args:
            x: Initial x position
            y: Initial y position
            color: Primary color of the firework
        """
        self.x = x
        self.y = y
        self.color = color
        self.velocity = -8.0  # Initial upward velocity
        self.exploded = False
        self.trail_particles = []
        self.explosion_particles = []

    def update(self) -> bool:
        """
        Update the firework's state.

        Returns:
            True if the firework is still active, False if it has finished

        Note:
            The firework rises until it reaches a random height,
            then explodes into multiple particles.
        """
        if not self.exploded:
            # Update position
            self.y += self.velocity
            self.velocity += 0.2  # Gravity

            # Create trail particles
            if random.random() < 0.7:
                self.trail_particles.append(
                    {
                        "x": self.x + random.uniform(-2, 2),
                        "y": self.y + random.uniform(-2, 2),
                        "color": self.color,
                        "size": random.randint(1, 3),
                        "life": 15,
                    }
                )

            # Check for explosion
            if self.velocity >= 0:  # Reached apex
                self.explode()
                self.exploded = True

        # Update trail particles
        for particle in self.trail_particles[:]:
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.trail_particles.remove(particle)

        # Update explosion particles
        for particle in self.explosion_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # Gravity
            particle["life"] -= 1

            if particle["life"] <= 0:
                self.explosion_particles.remove(particle)

        # Return True if there are still active particles
        return len(self.trail_particles) > 0 or len(self.explosion_particles) > 0

    def explode(self) -> None:
        """Create explosion particles for the firework."""
        num_particles = random.randint(50, 150)

        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)

            # Random color variation
            color_variation = random.randint(-30, 30)
            color = (
                min(255, max(0, self.color[0] + color_variation)),
                min(255, max(0, self.color[1] + color_variation)),
                min(255, max(0, self.color[2] + color_variation)),
            )

            self.explosion_particles.append(
                {
                    "x": self.x,
                    "y": self.y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "color": color,
                    "size": random.randint(2, 4),
                    "life": random.randint(30, 60),
                }
            )

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the firework and all its particles.

        Args:
            surface: Pygame surface to draw on
        """
        # Draw trail particles
        for particle in self.trail_particles:
            pygame.draw.circle(
                surface,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                particle["size"],
            )

        # Draw explosion particles
        for particle in self.explosion_particles:
            alpha = int(255 * (particle["life"] / 60))
            color_with_alpha = (*particle["color"], alpha)

            # Create a temporary surface for alpha blending
            temp_surface = pygame.Surface(
                (particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                temp_surface,
                color_with_alpha,
                (particle["size"], particle["size"]),
                particle["size"],
            )
            surface.blit(
                temp_surface,
                (
                    int(particle["x"] - particle["size"]),
                    int(particle["y"] - particle["size"]),
                ),
            )


def explode(
    pos: Tuple[float, float],
    num_particles: int = 100,
    color: Optional[Tuple[int, int, int]] = None,
    engine: Optional[ParticleEngine] = None,
) -> ParticleEngine:
    """
    Create an explosion effect at the specified position.

    Args:
        pos: Explosion center position as (x, y)
        num_particles: Number of particles in the explosion (default: 100)
        color: Primary explosion color (random if None)
        engine: Existing ParticleEngine to use, or None to create new one

    Returns:
        ParticleEngine containing the explosion particles

    Example:
        >>> # Create a red explosion
        >>> explosion = explode((400, 300), 150, RED)
        >>> # In game loop:
        >>> explosion.update_particles()
        >>> explosion.draw_particles(screen)
    """
    if engine is None:
        engine = ParticleEngine()

    if color is None:
        color = (
            random.randint(200, 255),
            random.randint(100, 200),
            random.randint(0, 100),
        )

    engine.generate_particles(
        num_particles=num_particles,
        pos=pos,
        velocity_range=(-8, 8),
        color=color,
        size_range=(2, 6),
        lifespan_range=(40, 80),
    )

    return engine
