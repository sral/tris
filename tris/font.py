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

    def write(self, x, y, line):
        """Write line.

        Keyword arguments:
        x -- x-coordinate
        y -- y-coordinate
        line -- String to write
        """

        surface = pygame.display.get_surface()
        for i, char in enumerate(line):
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

    def write_lines(self, y, lines):
        """Write multiple lines of text.

        Keyword arguments:
        y -- y-coordinate
        message -- Message to write
        """
        for line in lines:
            self.write_centered(y, line)
            y += 10