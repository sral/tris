import sys
import pygame
from font import Font
from player import Player
from playfield import Playfield
from tileset import Tileset
from trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

SPLASH_WIDTH = 200
SPLASH_HEIGHT = 320
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
TILE_WIDTH = 16
TILE_HEIGHT = 16
SCREEN_WIDTH = PLAYFIELD_WIDTH * TILE_WIDTH
SCREEN_HEIGHT = PLAYFIELD_HEIGHT * TILE_HEIGHT
START_SPEED = 700  # milliseconds, initial falling speed


class Tris(object):
    def __init__(self):
        """Initialize instance."""

        self.level = 0
        self.lines = 0
        self.player = None
        self.font = None
        self.splash_image = None
        self.tileset = None

    def setup(self):
        """Setup game."""

        pygame.init()
        pygame.display.set_icon(pygame.image.load('data/icon.gif'))
        pygame.display.set_caption("tris")

        self.tileset = Tileset('data/blocks.gif', 16, 16)
        self.splash_image = pygame.image.load('data/splash.gif')
        self.font = Font()

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
                if event.key == pygame.K_RETURN:
                    break
            surface.blit(self.splash_image, (0, 0))
            pygame.display.flip()

    def game_over(self):
        """Game over."""

        surface = pygame.display.get_surface()
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    break
            self.font.write_centered(100, "GAME OVER !!!")
            pygame.display.flip()

    def new_game(self):
        """Initialize new game."""

        self.player = Player()
        self.lines = 0
        self.level = 0

    def update_level(self):
        """Update game level i.e. falling speed. """

        self.level = int(self.lines / 10)
        speed = START_SPEED - self.level * 70
        if speed <= 0:
            speed = 10
        pygame.time.set_timer(pygame.USEREVENT, speed)

    def process_lines(self, playfield):
        """Process playfield lines.

        Keyword arguments:
        playfield -- Playfield
        """

        lines = playfield.find_lines()
        if lines:
            self.player.score += 2 ** (lines - 1) * 100
            self.lines += lines
            self.update_level()

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
        """Returns new trimino."""

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
        pygame.time.set_timer(pygame.USEREVENT, START_SPEED)
        clock = pygame.time.Clock()
        trimino = self.spawn_trimino()
        game_over = False

        while not game_over:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
                if event.key == pygame.K_j:
                    if not self.legal_move(playfield, trimino.rotate_left()):
                        trimino.rotate_right()  # Revert rotation
                if event.key == pygame.K_k:
                    if not self.legal_move(playfield, trimino.rotate_right()):
                        trimino.rotate_left()  # Revert rotation
                if event.key == pygame.K_SPACE:  # Hard drop
                    while self.legal_move(playfield, trimino.move_down()):
                        pass
                    if playfield.place_trimino(trimino.move_up()):
                        trimino = self.spawn_trimino()
                        self.process_lines(playfield)
                    else:
                        game_over = True
            elif event.type == pygame.USEREVENT:
                if not self.legal_move(playfield, trimino.move_down()):
                    if playfield.place_trimino(trimino.move_up()):
                        trimino = self.spawn_trimino()
                        self.process_lines(playfield)
                    else:
                        game_over = True

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                if not self.legal_move(playfield, trimino.move_left()):
                    trimino.move_right()  # Revert move
            if pressed[pygame.K_RIGHT]:
                if not self.legal_move(playfield, trimino.move_right()):
                    trimino.move_left()  # Revert move
            if pressed[pygame.K_DOWN]:
                if not self.legal_move(playfield, trimino.move_down()):
                    trimino.move_up()  # Revert move

            playfield.draw()
            trimino.draw()
            self.font.write(0, 1, "SCORE: %d" % self.player.score)
            self.font.write(0, 10, "LEVEL: %d" % self.level)
            pygame.display.flip()
            clock.tick(30)

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


