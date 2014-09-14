import os
import sys
import pkg_resources
import pygame
from font import Font
from hiscores import HiScores
from player import Player
from playfield import Playfield
from persistor import Persistor
from tileset import Tileset
from trimino import Trimino


__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

HISCORE_PATH = os.path.expanduser("~")
HISCORE_FILE = ".trisscore"
MAX_HISCORES = 10
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
    INFO_TEXT = ["CONTROLS",
                 "--------",
                 "",
                 "MOVE -- ARROW KEYS",
                 "ROTATE -- J/K     ",
                 "HARD DROP -- SPACE",
                 "QUIT -- ESCAPE    "]

    HISCORE_TEXT = ["HISCORES",
                    "--------"]

    CREDITS_TEXT = ["CREDITS",
                    "-------",
                    "ORIGNAL CONCEPT AND",
                    "DESIGN BY          ",
                    "ALEXEY PAJITNOV    ",
                    "",
                    "FEVER CODE AND     ",
                    "ART BY             ",
                    "SRAL               ",
                    "",
                    "",
                    "WWW.GITHUB.COM/SRAL"]

    def __init__(self):
        """Initialize instance."""

        self.level = 0
        self.lines = 0
        self.player = None
        self.font = None
        self.splash_image = None
        self.tileset = None
        self.hiscores = HiScores(max_scores=MAX_HISCORES)

    def setup(self):
        """Setup game."""

        pygame.init()
        image = pkg_resources.resource_filename(__name__, 'data/icon.gif')
        pygame.display.set_icon(pygame.image.load(image))
        pygame.display.set_caption("tris")

        self.tileset = Tileset('data/blocks.gif', 16, 16)
        image = pkg_resources.resource_filename(__name__, 'data/splash.gif')
        self.splash_image = pygame.image.load(image)
        self.font = Font()

    def splash_screen(self):
        """Display splash screen."""

        def draw_text(height, text):
            for line in text:
                self.font.write_centered(height, line)
                height += 10

        pygame.time.set_timer(pygame.USEREVENT, 5000)
        surface = pygame.display.set_mode((SPLASH_WIDTH, SPLASH_HEIGHT))

        hiscore_list = list(self.HISCORE_TEXT)
        for name, score in self.hiscores:
            hiscore_list.append(
                "{0:>3}: {1:>10} ".format(name, score)
            )
        texts = (self.INFO_TEXT,
                 hiscore_list,
                self.CREDITS_TEXT)
        text_index = 0

        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if event.key == pygame.K_RETURN:
                    break
            elif event.type == pygame.USEREVENT:
                if text_index < len(texts) - 1:
                    text_index += 1
                else:
                    text_index = 0
            surface.blit(self.splash_image, (0, 0))
            draw_text(100, texts[text_index])
            pygame.display.flip()

    def game_over(self):
        """Game over."""

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

    @staticmethod
    def legal_move(playfield, trimino):
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

    def game_loop(self):
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
        if self.hiscores.is_hiscore(self.player.score):
            self.hiscores.add("LTD", self.player.score)  # TODO: Get initials
        pygame.time.set_timer(pygame.USEREVENT, 0)  # Disable timer

    def run(self):
        self.setup()
        while True:
            self.splash_screen()
            self.new_game()
            self.game_loop()
            self.game_over()


def main_func():
    tris = Tris()
    tris.run()


if __name__ == "__main__":
    main_func()