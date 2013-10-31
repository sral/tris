import sys
import pygame
from player import Player
from playfield import Playfield
from tiles import Tiles, TILE_WIDTH, TILE_HEIGHT
from trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

SPLASH_WIDTH = 200
SPLASH_HEIGHT = 320
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
SCREEN_WIDTH = PLAYFIELD_WIDTH * TILE_WIDTH
SCREEN_HEIGHT = PLAYFIELD_HEIGHT * TILE_HEIGHT
START_SPEED = 700  # milliseconds, initial falling speed


class Tris(object):
    def __init__(self):
        """Initialize instance."""

        self.tileset = None
        self.splash_image = None
        self.player = None
        self.lines = 0

    def setup(self):
        """Setup game."""

        pygame.init()
        pygame.display.set_icon(pygame.image.load('data/icon.gif'))
        pygame.display.set_caption("tris")
        pygame.key.set_repeat(50, 50)

        self.tileset = Tiles()
        self.splash_image = pygame.image.load('data/splash.gif')

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

    def new_game(self):
        """Initialize new game."""

        self.player = Player()
        self.lines = 0

    def game_over(self):
        """Game over."""

        pass

    def calculate_score(self, lines):
        """Calculates score.

        Keyword arguments:
        lines -- Number of cleared lines
        """

        scores = {0: 0,
                  1: 100,
                  2: 200,
                  3: 400,
                  4: 800}

        return scores[lines]

    def legal_move(self, playfield, trimino):
        """Returns True if move is legal, False otherwise.

        Keyword arguments:
        playfield -- Current playfield
        trimino -- Trimino that is being moved
        """

        for x, y in trimino.keys():
            x += trimino.x
            y += trimino.y
            if (x < 0 or
                        x >= PLAYFIELD_WIDTH or
                        y >= PLAYFIELD_HEIGHT or
                    playfield[(x, y)]):
                return False
        return True

    def spawn_trimino(self):
        """Spawn new trimino."""

        trimino = Trimino.get_random(int(PLAYFIELD_WIDTH / 2), 0,
                                     self.tileset)
        trimino.y = -trimino.get_height() - 1
        return trimino


    def main(self):
        """Main loop."""

        surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill(0xC4CFA1)  # Same colour as splash screen

        playfield = Playfield(PLAYFIELD_WIDTH, PLAYFIELD_HEIGHT,
                              self.tileset)
        trimino = self.spawn_trimino()
        pygame.time.set_timer(pygame.USEREVENT, START_SPEED)

        while True:
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not self.legal_move(playfield,
                                           trimino.move_left()):
                        trimino.move_right()  # Revert move
                if event.key == pygame.K_RIGHT:
                    if not self.legal_move(playfield,
                                           trimino.move_right()):
                        trimino.move_left()  # Revert move
                if event.key == pygame.K_DOWN:  # Soft drop
                    if not self.legal_move(playfield,
                                           trimino.move_down()):
                        trimino.move_up()  # Revert move
                if event.key == pygame.K_j:
                    if not self.legal_move(playfield,
                                           trimino.rotate_left()):
                        trimino.rotate_right()  # Revert rotation
                if event.key == pygame.K_k:
                    if not self.legal_move(playfield,
                                           trimino.rotate_right()):
                        trimino.rotate_left()  # Revert rotation
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:  # Hard drop
                    while self.legal_move(playfield, trimino.move_down()):
                        pass
                    if not playfield.place_trimino(trimino.move_up()):
                        break  # GAME OVER!
                    else:
                        lines = playfield.find_lines()
                        self.player.score += self.calculate_score(lines)
                        trimino = self.spawn_trimino()
                if event.key == pygame.K_ESCAPE:
                    break
            elif event.type == pygame.USEREVENT:
                if not self.legal_move(playfield, trimino.move_down()):
                    if not playfield.place_trimino(trimino.move_up()):
                        break  # GAME OVER
                    else:
                        lines = playfield.find_lines()
                        self.player.score += self.calculate_score(lines)
                        trimino = self.spawn_trimino()
            elif event.type == pygame.QUIT:
                sys.exit(0)
            playfield.draw(surface)
            trimino.draw(surface)
            pygame.display.flip()

        pygame.time.set_timer(pygame.USEREVENT, 0)  # Disable timer

    def run(self):
        self.setup()
        while True:
            self.splash_screen()
            self.new_game()
            self.main()
            self.game_over()


if __name__ == "__main__":
    tris = Tris()
    tris.run()


