__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

BLOCK_SIZE = 16


class Playfield(object):

    playfield = {}

    def __init__(self, width, height, block_sprites):
        """Initialize instance."""

        self.width = width
        self.height = height
        self.block_sprites = block_sprites

    def place_trimino(self, trimino):
        """Place trimino onto playfield.

        Keyword arguments:
        trimino -- Trimino to be placed
        """

        for coordinates, block_type in trimino.itertiems():
            x, y = coordinates
            x += trimino.x
            y += trimino.y
            self[(x, y)] = block_type

    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                surface.blit(self.block_sprites[self[(x, y)]],
                             (x * BLOCK_SIZE,
                              y * BLOCK_SIZE))

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