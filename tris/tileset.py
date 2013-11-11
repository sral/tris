import pygame

__author__ = 'Lars Djerf <lars.djerf@gmail.com'

class Tileset(object):

    def __init__(self, image, tile_width, tile_height):
        """Initialize instance.

        Keyword arguments:
        image -- Bitmap containing tiles
        tile_width -- Tile width
        tile_height -- Tile height
        """

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles = {}

        image = pygame.image.load(image)

        for i in range(image.get_width() / tile_width):
            area = pygame.Rect(i * tile_width, 0, tile_width, tile_height)
            tile = pygame.Surface((tile_width, tile_height))
            tile.blit(image, (0, 0), area)
            self.tiles[i] = tile

    def draw(self, surface, tile, x, y):
        """Draw tile on surface.

        Keyword arguments:
        surface -- Target surface
        tile -- Tile type
        x -- x-coordinate
        y -- y-coordinate
        """

        surface.blit(self.tiles[tile],
                     (x * self.tile_width,
                      y * self.tile_height))
