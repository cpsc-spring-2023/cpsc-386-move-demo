# Michael Shafae
# CPSC 386-01
# 2050-01-01
# mshafae@csu.fullerton.edu
# @mshafae
#
# Lab 00-00
#
# Partners:
#
# This my first program and it prints out Hello World!
#

"""Scene objects for making games with PyGame."""

import math
import os
import pygame
import rgbcolors
from random import randint, uniform
from animation import Explosion


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, background_color, soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Process a game event by the scene."""
        # This should be commented out or removed since it generates a lot of noise.
        # print(str(event))
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Bye bye!")
            self._is_valid = False

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.5)
            except pygame.error as pygame_error:
                print("\n".join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(-1)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class PressAnyKeyToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._is_valid = False


class Circle:
    """Class representing a ball with a bounding rect."""

    def __init__(self, position, speed, radius, color, name="None"):
        self._position = position
        self._speed = speed
        self._radius = radius
        self._color = color
        self._name = name

    @property
    def radius(self):
        """Return the circle's radius"""
        return self._radius

    @property
    def position(self):
        """Return the circle's position."""
        return self._position

    @position.setter
    def position(self, val):
        """Set the circle's position."""
        self._position = val

    @property
    def speed(self):
        """Return the circle's speed."""
        return self._speed

    def move_ip(self, x, y):
        self._position = self._position + pygame.math.Vector2(x, y)
    
    @property
    def rect(self):
        """Return bounding rect."""
        left = self._position.x - self._radius
        top = self._position.y - self._radius
        width = 2 * self._radius
        return pygame.Rect(left, top, width, width)

    @property
    def width(self):
        """Return the width of the bounding box the circle is in."""
        return 2 * self._radius

    @property
    def height(self):
        """Return the height of the bounding box the circle is in."""
        return 2 * self._radius

    def draw(self, screen):
        """Draw the circle to screen."""
        pygame.draw.circle(screen, self._color, self.position, self.radius)

    def __repr__(self):
        """Circle stringify."""
        return f'Circle({repr(self._position)}, {self._radius}, {self._color}, "{self._name}")'

class MoveScene(PressAnyKeyToExitScene):
    def __init__(self, screen):
        super().__init__(screen, rgbcolors.black, None)
        self._target_position = None
        self._delta_time = 0
        self._circles = []
        self.make_circles()

    def make_circles(self):
        num_circles = 1000
        circle_radius = 5
        min_speed = 0.25
        max_speed = 5.0
        (width, height) = self._screen.get_size()
        for i in range(num_circles):
            position = pygame.math.Vector2(randint(0, width-1), randint(0, height-1))
            speed = uniform(min_speed, max_speed)
            c = Circle(position, speed, circle_radius, rgbcolors.random_color(), i+1)
            self._circles.append(c)
    
    @property
    def delta_time(self):
        return self._delta_time
    
    @delta_time.setter
    def delta_time(self, val):
        self._delta_time = val
    
    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._target_position = pygame.math.Vector2(event.pos)
            print(f'Target position is {self._target_position}')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self._target_position = None
            self.make_circles()
        else:
            super().process_event(event)
    
    def update_scene(self):
        if self._target_position:
            for c in self._circles:
                if 1:
                    c.position.move_towards_ip(self._target_position, c.speed * self._delta_time)
                else:
                    max_distance = c.speed * self._delta_time
                    if math.isclose(max_distance, 0.0, rel_tol=1e-01):
                        continue
                    direction = self._target_position - c.position
                    distance = direction.length()
                    if math.isclose(distance, 0.0, rel_tol=1e-01):
                        continue
                    elif distance <= max_distance:
                        c.position = self._target_position
                    else:
                        movement = direction * (max_distance / distance)
                        c.move_ip(movement.x, movement.y)

    def draw(self):
        super().draw()
        for c in self._circles:
            c.draw(self._screen)