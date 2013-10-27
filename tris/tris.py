import sys
import pygame
from playfield import Playfield
from trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

SPLASH_WIDTH = 200
SPLASH_HEIGHT = 320
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
BLOCK_SIZE = 16
SCREEN_WIDTH = PLAYFIELD_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = PLAYFIELD_HEIGHT * BLOCK_SIZE
START_SPEED = 700  # milliseconds, initial falling speed


class Tris(object):
    def setup(self):
        """Setup game."""

        pygame.init()
        pygame.display.set_caption("tris")
        pygame.key.set_repeat(50, 50)

        self.splash_image = pygame.image.load('data/splash.gif')
        self.block_sprites = {0: pygame.image.load('data/block0.gif'),
                              1: pygame.image.load('data/block1.gif'),
                              2: pygame.image.load('data/block2.gif'),
                              3: pygame.image.load('data/block3.gif'),
                              4: pygame.image.load('data/block4.gif'),
                              5: pygame.image.load('data/block5.gif'),
                              6: pygame.image.load('data/block6.gif'),
                              7: pygame.image.load('data/block7.gif'),
                              8: pygame.image.load('data/block8.gif')}

    def splash_screen(self):
        """Display splash screen. """

        surface = pygame.display.set_mode((SPLASH_WIDTH, SPLASH_HEIGHT))

        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    break
            surface.blit(self.splash_image, (0, 0))
            pygame.display.flip()

    def legal_move(self, playfield, trimino, delta):
        """Returns True if move is legal, False otherwise.

        Keyword arguments:
        playfield -- Current playfield
        trimino -- Trimino that is being moved
        delta -- Tuple containing x, y displacement i.e. the move
        """

        x1, y1 = delta
        for x0, y0 in trimino.keys():
            x2 = x0 + x1
            y2 = y0 + y1
            if (x2 < 0 or
                        x2 >= PLAYFIELD_WIDTH or
                        y2 >= PLAYFIELD_HEIGHT or
                    playfield[(x2, y2)]):
                return False
        return True

    def main(self):
        """Main loop."""

        self.setup()  # Load resources etc...

        while True:
            self.splash_screen()

            surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            surface.fill(0xC4CFA1)  # Same colour as splash screen

            playfield = Playfield(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT,
                                  self.block_sprites)
            trimino = Trimino.get_random(int(PLAYFIELD_WIDTH / 2), 0,
                                         self.block_sprites)

            pygame.time.set_timer(pygame.USEREVENT, START_SPEED)

            while True:
                event = pygame.event.poll()
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.USEREVENT:
                    if self.legal_move(playfield,
                                       trimino,
                                       (trimino.x, trimino.y + 1)):
                        trimino.y += 1
                    else:
                        playfield.place_trimino(trimino)
                        trimino = Trimino.get_random(int(PLAYFIELD_WIDTH / 2), 0,
                                                     self.block_sprites)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.legal_move(playfield,
                                           trimino,
                                           (trimino.x - 1, trimino.y)):
                            trimino.x -= 1
                    if event.key == pygame.K_RIGHT:
                        if self.legal_move(playfield,
                                           trimino,
                                           (trimino.x + 1, trimino.y)):
                            trimino.x += 1
                    if event.key == pygame.K_DOWN:
                        if self.legal_move(playfield,
                                           trimino,
                                           (trimino.x, trimino.y + 1)):
                            trimino.y += 1
                    if event.key == pygame.K_j:
                        trimino.rotate_left()
                        if not self.legal_move(playfield,
                                               trimino,
                                               (trimino.x, trimino.y)):
                            trimino.rotate_right()  # Revert rotation
                    if event.key == pygame.K_k:
                        trimino.rotate_right()
                        if not self.legal_move(playfield,
                                               trimino,
                                               (trimino.x, trimino.y)):
                            trimino.rotate_left()  # Revert rotation
                    if event.key == pygame.K_SPACE:
                        pass  # Drop and place block
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        break
                playfield.draw(surface)
                trimino.draw(surface)
                pygame.display.flip()

            pygame.time.set_timer(pygame.USEREVENT, 0)  # Disable timer

if __name__ == "__main__":
    t = Tris()
    t.main()


