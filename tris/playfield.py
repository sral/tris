__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

import pygame

BLOCK_SIZE = 16


class Playfield(object):
    sprites = {0: pygame.image.load('data/block0.gif'),
               1: pygame.image.load('data/block1.gif'),
               2: pygame.image.load('data/block2.gif'),
               3: pygame.image.load('data/block3.gif'),
               4: pygame.image.load('data/block4.gif'),
               5: pygame.image.load('data/block5.gif'),
               6: pygame.image.load('data/block6.gif'),
               7: pygame.image.load('data/block7.gif'),
               8: pygame.image.load('data/block8.gif')}
    playfield = {}

    def __init__(self, width, height):
        """Initialize instance."""

        self.width = width
        self.height = height

    def place_trimino(self):
        pass

    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                surface.blit(self.sprites[self[(x, y)]],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE))

    def __getitem__(self, key):
        """Get playfield value

        Keyword arguments:

        key -- Tuple containing x and y coordinates
        """

        x, y = key
        if (x < 0 or x >= self.width or
                    y < 0 or y >= self.height):
            raise IndexError("")
        return self.playfield.get(key, 0)

    def __setitem__(self, key, value):
        """Set playfield value.

        Keyword arguments:
        key -- Tuple containing x and y coordinates
        value -- Block type
        """

        x, y = key
        if (x < 0 or x >= self.width or
                    y < 0 or y >= self.height):
            raise IndexError("")
        self.playfield[key] = value