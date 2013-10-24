import sys
import pygame
from playfield import Playfield
from trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

BLOCK_SIZE = 16  # Block sprites are 16x6
SPLASH_WIDTH = 200
SPLASH_HEIGHT = 320
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
SCREEN_WIDTH = PLAYFIELD_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = PLAYFIELD_HEIGHT * BLOCK_SIZE
START_SPEED = 700  # milliseconds, initial falling speed


class Tris(object):
    splash_image = pygame.image.load('data/splash.gif')

    def __init__(self):
        """Initialize instance."""

        self.playfield = None
        pygame.init()
        pygame.display.set_caption("tris")


    def splash_screen(self):
        """Display splash screen. """

        surface = pygame.display.set_mode((SPLASH_WIDTH, SPLASH_HEIGHT))

        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    break
            surface.blit(self.splash_image, (0, 0))
            pygame.display.flip()

    def new_game(self):
        """Setup new game."""

        self.playfield = Playfield(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT)
        pygame.time.set_timer(pygame.USEREVENT, START_SPEED)

    def legal_move(self, playfield, trimino, displacement):
        """Returns True if move is legal, False otherwise.

        Keyword arguments:
        playfield -- Current playfield
        trimino -- Trimino that is being moved
        displacement -- Tuple containing x, y displacement i.e. the move
        """

        x1, y1 = displacement
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

        self.splash_screen()
        self.new_game()

        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill(0xC4CFA1)  # Same colour as splash screen
        pygame.key.set_repeat(50, 50)

        trimino = Trimino.spawn_random(5, 5)

        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.USEREVENT:
                print "timer"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.legal_move(self.playfield,
                                       trimino,
                                       (trimino.x - 1, trimino.y)):
                        trimino.x -= 1
                if event.key == pygame.K_RIGHT:
                    if self.legal_move(self.playfield,
                                       trimino,
                                       (trimino.x + 1, trimino.y)):
                        trimino.x += 1
                if event.key == pygame.K_DOWN:
                    if self.legal_move(self.playfield,
                                       trimino,
                                       (trimino.x, trimino.y + 1)):
                        trimino.y += 1
                if event.key == pygame.K_ESCAPE:
                    break
            trimino.draw(surface)
            pygame.display.flip()

        sys.exit(0)


if __name__ == "__main__":
    t = Tris()
    t.main()


