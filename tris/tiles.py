import pygame

__author__ = 'Lars Djerf <lars.djerf@gmail.com'


class Tiles(object):
    TILE_WIDTH = 16
    TILE_HEIGHT = 16

    tiles = {0: pygame.image.load('data/block0.gif'),
             1: pygame.image.load('data/block1.gif'),
             2: pygame.image.load('data/block2.gif'),
             3: pygame.image.load('data/block3.gif'),
             4: pygame.image.load('data/block4.gif'),
             5: pygame.image.load('data/block5.gif'),
             6: pygame.image.load('data/block6.gif'),
             7: pygame.image.load('data/block7.gif'),
             8: pygame.image.load('data/block8.gif')}

    def draw(self, surface, tile, x, y):
        """Draw tile on surface.

        Keyword arguments:
        surface -- Target surface
        tile -- Tile type
        x -- x-coordinate
        y -- y-coordinate
        """

        surface.blit(self.tiles[tile],
                     (x * self.TILE_WIDTH,
                      y * self.TILE_HEIGHT))
