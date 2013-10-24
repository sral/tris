import sys
import pygame
from playfield import Playfield
from trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256
SPLASH_X_SIZE = 200
SPLASH_Y_SIZE = 320
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
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

        surface = pygame.display.set_mode((SPLASH_X_SIZE, SPLASH_Y_SIZE))

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

    def legal_move(self, playfield, trimino, coordinates):
        """Returns True if move is legal, False otherwise."""

        return True

    def main(self):
        """Main loop."""

        self.splash_screen()

        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_WIDTH))

        self.new_game()

        trimino = Trimino.spawn(5, 5)

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
                                       trimino.x - 1):
                        trimino.x -= 1
                if event.key == pygame.K_RIGHT:
                    if self.legal_move(self.playfield,
                                       trimino,
                                       trimino.x + 1):
                        trimino.x += 1
                if event.key == pygame.K_DOWN:
                    if self.legal_move(self.playfield,
                                       trimino,
                                       trimino.y + 1):
                        trimino.y += 1
                if event.key == pygame.K_ESCAPE:
                    break
            trimino.draw(surface)
            pygame.display.flip()

        sys.exit(0)


if __name__ == "__main__":
    t = Tris()
    t.main()


