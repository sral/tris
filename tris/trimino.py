import random

import pygame


__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class Trimino(object):
    shapes = {'O': ({(0, 0): 1,
                     (0, 1): 1,
                     (1, 0): 1,
                     (1, 1): 1}, ),
              'I': ({(0, 0): 2, # vertical
                     (1, 0): 2,
                     (2, 0): 2,
                     (3, 0): 2},
                    {(1, 0): 2, # horizontal
                     (1, 1): 2,
                     (1, 2): 2,
                     (1, 3): 2}),
              'J': ({(0, 2): 3, # vertical
                     (1, 0): 3,
                     (1, 1): 3,
                     (1, 2): 3},
                    {(0, 0): 3, # Rotated anti-clockwise 90 degrees
                     (1, 0): 3,
                     (2, 0): 3,
                     (2, 1): 3},
                    {(0, 0): 3, # Upside down
                     (0, 1): 3,
                     (0, 2): 3,
                     (1, 0): 3},
                    {(0, 0): 3, # Rotated clockwise 90 degrees
                     (0, 1): 3,
                     (1, 1): 3,
                     (2, 1): 3}),
              'L': ({(0, 0): 4, # Vertical
                     (0, 1): 4,
                     (0, 2): 4,
                     (1, 2): 4},
                    {(0, 1): 4, # Rotated anti-clockwise 90 degrees
                     (1, 1): 4,
                     (2, 1): 4,
                     (2, 0): 4},
                    {(0, 0): 4, # Upside down
                     (1, 0): 4,
                     (1, 1): 4,
                     (1, 2): 4},
                    {(0, 0): 4, # Rotated clockwise 90 degrees
                     (0, 1): 4,
                     (1, 0): 4,
                     (2, 0): 4}),
              'S': ({(1, 0): 5, # horizontal
                     (2, 0): 5,
                     (0, 1): 5,
                     (1, 1): 5},
                    {(0, 0): 5, # vertical
                     (0, 1): 5,
                     (1, 1): 5,
                     (1, 2): 5}),
              'T': ({(0, 0): 6, # down
                     (1, 0): 6,
                     (1, 1): 6,
                     (2, 0): 6},
                    {(0, 0): 6, # right
                     (0, 1): 6,
                     (1, 1): 6,
                     (0, 2): 6},
                    {(1, 0): 6, # up
                     (0, 1): 6,
                     (1, 1): 6,
                     (2, 1): 6},
                    {(1, 0): 6, #left
                     (1, 1): 6,
                     (0, 1): 6,
                     (1, 2): 6}),
              'Z': ({(0, 0): 7, # horizontal
                     (1, 0): 7,
                     (1, 1): 7,
                     (2, 1): 7},
                    {(1, 0): 7, # vertical
                     (0, 1): 7,
                     (1, 1): 7,
                     (0, 2): 7})}

    def __init__(self, x, y, rotations, tileset):
        """Initialize instance.

        Keyword arguments:
        x -- Initial x-coordinate
        y -- Initial y-coordinate
        rotations -- Dictionary containing rotations/shapes
        tileset -- Tileset
        """

        self.x = x
        self.y = y
        self.rotation = 0
        self.rotations = rotations
        self.max_rotation = len(rotations) - 1
        self.tileset = tileset

    @classmethod
    def get_random(cls, x, y, tileset):
        """Spawn random trimino.

        Keyword arguments:
        x -- Initial x-coordinate
        y -- Initial y-coordinate
        tileset -- Tileset
        """

        shapes = ('O', 'I', 'J', 'L', 'S', 'T', 'Z')
        return cls.get(random.choice(shapes), x, y, tileset)

    @classmethod
    def get(cls, shape, x, y, tileset):
        """Spawn new block.

        Keyword arguments:
        shape -- Trimino shape
        x -- Initial x-coordinate
        y -- Initial y-coordinate
        tileset -- Tileset
        """

        if shape in cls.shapes.keys():
            return cls(x, y, cls.shapes[shape], tileset)
        else:
            raise ValueError("Illegal trimino type: %s" % shape)

    def move_left(self):
        """Move block left."""

        self.x -= 1
        return self

    def move_right(self):
        """Move block right."""

        self.x += 1
        return self

    def move_down(self):
        """Move block down."""

        self.y += 1
        return self

    def move_up(self):
        """Move block up."""

        self.y -= 1
        return self


    def rotate_left(self):
        """Rotate block left."""

        if self.rotation > 0:
            self.rotation -= 1
        else:
            self.rotation = self.max_rotation
        return self

    def rotate_right(self):
        """Rotate block right."""

        if self.rotation < self.max_rotation:
            self.rotation += 1
        else:
            self.rotation = 0
        return self

    def get_height(self):
        """Returns triminio height."""

        return max([y for x, y in self.keys()])

    def draw(self):
        """Draw trimino."""

        surface = pygame.display.get_surface()
        for coordinates, tile in self.itertiems():
            x0, y0 = coordinates
            self.tileset.draw(surface, tile, x0 + self.x, y0 + self.y)

    def keys(self):
        return self.rotations[self.rotation].keys()

    def itertiems(self):
        return self.rotations[self.rotation].iteritems()

    def __getitem__(self, key):
        return self.rotations[self.rotation].get(key, 0)

    def __setitem__(self, key, value):
        raise TypeError("Trimino modification not allowed.")