import random

import pygame.image


__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

BLOCK_SIZE = 16  # Block sprites are 16x6


class Trimino(object):
    sprites = {1: pygame.image.load('data/block0.gif'),
               2: pygame.image.load('data/block1.gif'),
               3: pygame.image.load('data/block2.gif'),
               4: pygame.image.load('data/block3.gif'),
               5: pygame.image.load('data/block4.gif'),
               6: pygame.image.load('data/block5.gif'),
               7: pygame.image.load('data/block6.gif'),
               8: pygame.image.load('data/block7.gif')}

    def __init__(self, x, y, rotations, max_rotation):
        """Initialize instance."""

        self.x = x
        self.y = y
        self.max_rotation = max_rotation
        self.rotation = 0
        self.rotations = rotations

    @classmethod
    def get_random(cls, x, y):
        """Spawn random trimino."""

        triminos = {0: TriminoO,
                    1: TriminoI,
                    2: TriminoJ,
                    3: TriminoL,
                    4: TriminoS,
                    5: TriminoT,
                    6: TriminoZ}

        return triminos[random.randint(0, 6)](x, y)

    @classmethod
    def get(cls, trimino_type, x, y):
        """Spawn new block."""

        triminos = {'O': TriminoO,
                    'I': TriminoI,
                    'J': TriminoJ,
                    'L': TriminoL,
                    'S': TriminoS,
                    'T': TriminoT,
                    'Z': TriminoZ}

        if trimino_type in triminos.keys():
            return triminos[trimino_type](x, y)
        else:
            raise ValueError("Illegal trimino type: %s" % trimino_type)

    def rotate_left(self):
        """Rotate block left."""

        if self.rotation > 0:
            self.rotation -= 1
        else:
            self.rotation = self.max_rotation

    def rotate_right(self):
        """Rotate block right."""

        if self.rotation < self.max_rotation:
            self.rotation += 1
        else:
            self.rotation = self.max_rotation

    def keys(self):
        return self.rotations[self.rotation].keys()

    def itertiems(self):
        return self.rotations[self.rotation].iteritems()

    def draw(self, screen):
        for coordinates, block_type in self.itertiems():
            x0, y0 = coordinates
            screen.blit(self.sprites[block_type],
                        ((x0 + self.x) * BLOCK_SIZE, (y0 + self.y) * BLOCK_SIZE))

    def __getitem__(self, key):
        return self.rotations[self.rotation].get(key, 0)

    def __setitem__(self, key, value):
        raise TypeError("Trimino modification not allowed.")


class TriminoO(Trimino):
    rotations = ({(0, 0): 1,
                  (0, 1): 1,
                  (1, 0): 1,
                  (1, 1): 1}, )

    def __init__(self, x, y):
        Trimino.__init__(self, x, y, self.rotations, max_rotation=0)


class TriminoI(Trimino):
    rotations = ({(0, 0): 2, # vertical
                  (1, 0): 2,
                  (2, 0): 2,
                  (3, 0): 2},
                 {(0, 0): 2, # horizontal
                  (0, 1): 2,
                  (0, 2): 2,
                  (0, 3): 2})

    def __init__(self, x, y):
        Trimino.__init__(self, x, y, self.rotations, max_rotation=1)


class TriminoJ(Trimino):
    rotations = ({(0, 0): 3, # horizontal
                  (0, 1): 3,
                  (1, 1): 3,
                  (2, 1): 3},
                 {(1, 0): 3, # vertical
                  (1, 1): 3,
                  (1, 2): 3,
                  (0, 2): 3})

    def __init__(self, x, y):
        Trimino.__init__(self, x, y, self.rotations, max_rotation=1)


class TriminoL(Trimino):
    rotations = ({(0, 1): 4, # vertical
                  (1, 1): 4,
                  (2, 1): 4,
                  (2, 0): 4},
                 {(0, 0): 4, # horizontal
                  (0, 1): 4,
                  (0, 2): 4,
                  (1, 2): 4})

    def __init__(self, x, y):
        Trimino.__init__(self, x, y, self.rotations, max_rotation=1)


class TriminoS(Trimino):
    rotations = ({(1, 0): 5, # horizontal
                  (2, 0): 5,
                  (0, 1): 5,
                  (1, 1): 5},
                 {(1, 0): 5, # vertical
                  (0, 1): 5,
                  (1, 1): 5,
                  (0, 2): 5})

    def __init__(self, x, y):
        Trimino.__init__(self, x, y, self.rotations, max_rotation=1)


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

    def __init__(self, x, y):
        Trimino.__init__(self, x, y, self.rotations, max_rotation=3)


class TriminoZ(Trimino):
    rotations = ({(0, 0): 7,  # horizontal
                  (1, 0): 7,
                  (1, 1): 7,
                  (2, 1): 7},
                 {(1, 0): 7,  # vertical
                  (0, 1): 7,
                  (1, 1): 7,
                  (0, 2): 7})

    def __init__(self, x, y):
        Trimino.__init__(self, x, y, self.rotations, max_rotation=2)

