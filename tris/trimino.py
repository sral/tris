import random

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

BLOCK_SIZE = 16


class Trimino(object):
    def __init__(self, x, y, rotations, block_sprites):
        """Initialize instance.

        Keyword arguments:
        x --
        y --
        rotations --
        max_rotation --
        block_sprites --
        """

        self.x = x
        self.y = y
        self.rotation = 0
        self.rotations = rotations
        self.max_rotation = len(rotations) - 1
        self.block_sprites = block_sprites

    @classmethod
    def get_random(cls, x, y, block_sprites):
        """Spawn random trimino."""

        triminos = {0: TriminoO,
                    1: TriminoI,
                    2: TriminoJ,
                    3: TriminoL,
                    4: TriminoS,
                    5: TriminoT,
                    6: TriminoZ}

        return triminos[random.randint(0, 6)](x, y, block_sprites)

    @classmethod
    def get(cls, trimino_type, x, y, block_sprites):
        """Spawn new block."""

        triminos = {'O': TriminoO,
                    'I': TriminoI,
                    'J': TriminoJ,
                    'L': TriminoL,
                    'S': TriminoS,
                    'T': TriminoT,
                    'Z': TriminoZ}

        if trimino_type in triminos.keys():
            return triminos[trimino_type](x, y, block_sprites)
        else:
            raise ValueError("Illegal trimino type: %s" % trimino_type)

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

    def keys(self):
        return self.rotations[self.rotation].keys()

    def itertiems(self):
        return self.rotations[self.rotation].iteritems()

    def draw(self, surface):
        """Draw trimino.

        Keyword arguments:
        surface -- Surface instance
        """
        for coordinates, block_type in self.itertiems():
            x0, y0 = coordinates
            surface.blit(self.block_sprites[block_type],
                         ((x0 + self.x) * BLOCK_SIZE,
                          (y0 + self.y) * BLOCK_SIZE))

    def __getitem__(self, key):
        return self.rotations[self.rotation].get(key, 0)

    def __setitem__(self, key, value):
        raise TypeError("Trimino modification not allowed.")


class TriminoO(Trimino):
    rotations = ({(0, 0): 1,
                  (0, 1): 1,
                  (1, 0): 1,
                  (1, 1): 1}, )

    def __init__(self, x, y, block_sprites):
        Trimino.__init__(self, x, y, self.rotations, block_sprites)


class TriminoI(Trimino):
    rotations = ({(0, 0): 2, # vertical
                  (1, 0): 2,
                  (2, 0): 2,
                  (3, 0): 2},
                 {(0, 0): 2, # horizontal
                  (0, 1): 2,
                  (0, 2): 2,
                  (0, 3): 2})

    def __init__(self, x, y, block_sprites):
        Trimino.__init__(self, x, y, self.rotations, block_sprites)


class TriminoJ(Trimino):
    rotations = ({(0, 2): 3, # vertical
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
                  (2, 1): 3})

    def __init__(self, x, y, block_sprites):
        Trimino.__init__(self, x, y, self.rotations, block_sprites)


class TriminoL(Trimino):
    rotations = ({(0, 0): 4, # Vertical
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
                  (2, 0): 4})

    def __init__(self, x, y, block_sprites):
        Trimino.__init__(self, x, y, self.rotations, block_sprites)


class TriminoS(Trimino):
    rotations = ({(1, 0): 5, # horizontal
                  (2, 0): 5,
                  (0, 1): 5,
                  (1, 1): 5},
                 {(0, 0): 5, # vertical
                  (0, 1): 5,
                  (1, 1): 5,
                  (1, 2): 5})

    def __init__(self, x, y, block_sprites):
        Trimino.__init__(self, x, y, self.rotations, block_sprites)


class TriminoT(Trimino):
    rotations = ({(0, 0): 6, # down
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
                  (1, 2): 6})

    def __init__(self, x, y, block_sprites):
        Trimino.__init__(self, x, y, self.rotations, block_sprites)


class TriminoZ(Trimino):
    rotations = ({(0, 0): 7, # horizontal
                  (1, 0): 7,
                  (1, 1): 7,
                  (2, 1): 7},
                 {(1, 0): 7, # vertical
                  (0, 1): 7,
                  (1, 1): 7,
                  (0, 2): 7})

    def __init__(self, x, y, block_sprites):
        Trimino.__init__(self, x, y, self.rotations, block_sprites)

