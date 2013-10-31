__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

BLOCK_SIZE = 16


class Playfield(object):
    def __init__(self, width, height, tileset):
        """Initialize instance."""

        self.width = width
        self.height = height
        self.tileset = tileset
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
        """Find and process lines. Returns number of lines."""

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

        Returns True on success, False on failure.
        """

        try:
            for coordinates, block_type in trimino.itertiems():
                x, y = coordinates
                x += trimino.x
                y += trimino.y
                self[(x, y)] = block_type
            return True
        except IndexError:
            return False  # GAME OVER!


    def draw(self, surface):
        for y in range(self.height):
            for x in range(self.width):
                self.tileset.draw(surface, self[(x, y)], x, y)


    def __getitem__(self, key):
        """Returns playfield tile at coordinates.

        Keyword arguments:
        key -- Tuple containing tile coordinates
        """

        x, y = key
        if (x < 0 or x >= self.width or
                    y >= self.height):
            raise IndexError("")
        return self.playfield.get(key, 0)


    def __setitem__(self, key, value):
        """Set block in playfield.

        Keyword arguments:
        key -- Tuple containing tile coordinates
        value -- Tile type
        """

        x, y = key
        if (x < 0 or x >= self.width or
                    y < 0 or y >= self.height):
            raise IndexError("")
        self.playfield[key] = value