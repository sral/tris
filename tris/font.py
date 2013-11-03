import pygame

__author__ = 'Lars Djerf <lars.djerf@gmail.com'

WIDTH = 8
HEIGHT = 8


class Font(object):
    def __init__(self):
        """Initialize instance."""

        self.font = pygame.image.load('data/font.gif')

    def write(self, surface, x, y, message):
        """Write message on surface.

        Keyword arguments:
        surface -- Surface
        x -- x-coordinate
        y -- y-coordinate
        message -- Message to write
        """

        for char, i in zip(message, range(len(message))):
            area = pygame.Rect(ord(char) * 8, 0, WIDTH, HEIGHT)
            surface.blit(self.font,
                         (x + i * WIDTH, y),
                         area)

