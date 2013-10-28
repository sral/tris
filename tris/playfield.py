__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

BLOCK_SIZE = 16


class Playfield(object):
    def __init__(self, width, height, block_sprites):
        """Initialize instance."""

        self.width = width
        self.height = height
        self.block_sprites = block_sprites
        self.playfield = {}

    def scroll_field(self, y):
        """Scroll playfield down.

        Keyword arguments:
        y -- y-coordinate from which to scroll down
        """

        for y in reversed(range(y)):
            for x in range(self.width):
                if self[(x, y)]:
                    self[(x, y + 1)] = self[(x, y)]
                    del self.playfield[(x, y)]
                elif self.playfield.has_key((x, y + 1)):
                    del self.playfield[(x, y + 1)]

    def find_lines(self):
        """Find and process lines."""

        lines = 0
        for y in range(self.height):
            line = True
            for x in range(self.width):
                if not self[(x, y)]:
                    line = False
                    break
            if line:
                self.scroll_field(y)
                lines += 1
        return lines

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
        """Get playfield block.

        Keyword arguments:
        key -- Tuple containing block coordinates
        """

        x, y = key
        if (x < 0 or x >= self.width or
                    y < 0 or y >= self.height):
            raise IndexError("")
        return self.playfield.get(key, 0)

    def __setitem__(self, key, value):
        """Set block in playfield.

        Keyword arguments:
        key -- Tuple containing block coordinates
        value -- Block type
        """

        x, y = key
        if (x < 0 or x >= self.width or
                    y < 0 or y >= self.height):
            raise IndexError("")
        self.playfield[key] = value