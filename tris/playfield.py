__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class Playfield(object):
    playfield = {}

    def __init__(self, width, height):
        """Initialize instance."""

        self.width = width
        self.height = height


    def place_trimino(self):
        pass


    def __getitem__(self, key):
        """Get playfield value
         key -- Tuple containing x and y coordinates"""

        x, y = key
        if (x < 0 or x >= self.width or
            y < 0 or y >= self.height):
            raise IndexError("")
        return self.playfield.get(key, 0)

    def __setitem__(self, key, value):
        """Set playfield value.

        Keyword arguments:
        key -- Tuple containing x and y coordinates
        value -- Block type"""

        x, y = key
        if (x < 0 or x >= self.width or
            y < 0 or y >= self.height):
            raise IndexError("")
        self.playfield[key] = value