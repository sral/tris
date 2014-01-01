import pkg_resources
import pygame

__author__ = 'Lars Djerf <lars.djerf@gmail.com'

TILE_WIDTH = 8
TILE_HEIGHT = 8


class Font(object):
    def __init__(self):
        """Initialize instance."""

        tiles = pkg_resources.resource_filename(__name__, 'data/font.gif')
        self.font = pygame.image.load(tiles)

    def write(self, x, y, message):
        """Write message.

        Keyword arguments:
        x -- x-coordinate
        y -- y-coordinate
        message -- Message to write
        """

        surface = pygame.display.get_surface()
        for i, char in enumerate(message):
            area = pygame.Rect(ord(char) * 8, 0, TILE_WIDTH, TILE_HEIGHT)
            surface.blit(self.font,
                         (x + i * TILE_WIDTH, y),
                         area)

    def write_centered(self, y, message):
        """Write centered message.

        Keyword arguments:
        y -- y-coordinate
        message -- Message to write
        """

        width = pygame.display.get_surface().get_width()
        self.write((width - len(message) * TILE_WIDTH) / 2, y, message)

