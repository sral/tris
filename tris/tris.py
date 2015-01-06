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

SPLASH_WIDTH = 200
SPLASH_HEIGHT = 320
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20
TILE_WIDTH = 16
TILE_HEIGHT = 16
SCREEN_WIDTH = PLAYFIELD_WIDTH * TILE_WIDTH
SCREEN_HEIGHT = PLAYFIELD_HEIGHT * TILE_HEIGHT
START_SPEED = 700  # milliseconds, initial falling speed
MIN_ALPHA = 0
MAX_ALPHA = 255
BACKGROUND_COLOR = (195, 206, 160)


class Tris(object):
    INFO_TEXT = ["CONTROLS",
                 "--------",
                 "",
                 "MOVE -- ARROW KEYS",
                 "ROTATE -- J/K     ",
                 "HARD DROP -- SPACE",
                 "QUIT -- ESCAPE    "]

    HISCORES_TEXT = ["HISCORES",
                     "--------",
                     ""]

    CREDITS_TEXT = ["CREDITS",
                    "-------",
                    "",
                    "ORIGNAL CONCEPT AND",
                    "DESIGN BY          ",
                    "ALEXEY PAJITNOV    ",
                    "",
                    "FEVER CODE AND     ",
                    "ART BY             ",
                    "SRAL               ",
                    "",
                    "",
                    "",
                    "WWW.GITHUB.COM/SRAL"]

    GAME_OVER_TEXT = ["GAME OVER !!!"]

    ENTER_HISCORE_TEXT = ["HISCORE",
                          "-------",
                          "ENTER INITIALS:",
                          ""]

    def __init__(self):
        """Initialize instance."""

        self.level = 0
        self.lines = 0
        self.player = None
        self.font = None
        self.splash_image = None
        self.tileset = None
        self.hiscores = None

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

        self.hiscores = Persistor.load()
        if not self.hiscores:
            self.hiscores = HiScores.get_default_hiscore_list()

    @staticmethod
    def smoothstep(n):
        """Smoothstep interpolation.

        Keyword arguments:
        n -- Value to smooth
        """

        # TODO: Sprinkle this on scrollers
        return n * n * (3 - 2 * n)

    @staticmethod
    def lerp(start, stop, steps):
        """Linear interpolation between two values.

        Keyword arguments:
        start -- Start from
        stop -- Stop at
        steps -- Number of discreet steps
        """
        i = 0.0
        while i <= steps:
            v = i / steps
            yield (stop * v) + (start * (1 - v))
            i += 1

    @staticmethod
    def get_ordinal(n):
        """Returns ordinal (1st, 2nd, 3th, 4th, ...)

        Keyword arguments:
        n -- Number
        """
        if not 0 <= n < 1000:
            raise ValueError("Domain error")

        ordinal_suffix = {1: "ST",
                          2: "ND",
                          3: "RD"}
        unit_digit = n % 10
        tens_digit = (n / 10) % 10
        if tens_digit == 1:
            return "{0}TH".format(n)
        else:
            return "{0}{1}".format(
                n, ordinal_suffix.get(unit_digit, "TH"))

    def fade(self, fade_surface, start_alpha=MIN_ALPHA, stop_alpha=MAX_ALPHA):
        """Fade surface.

        Keyword arguments:
        fade_surface -- Surface to fade in/out
        start_alpha -- Value to start fade from
        stop_alpha -- Value to stop fade at
        """

        surface = pygame.display.get_surface()
        for alpha in self.lerp(start_alpha, stop_alpha, 50):
            surface.fill((0, 0, 0))
            fade_surface.set_alpha(alpha)
            surface.blit(fade_surface, (0, 0))
            pygame.display.flip()
            pygame.time.delay(5)

    def new_game(self):
        """Initialize new game."""

        self.player = Player()
        self.lines = 0
        self.level = 0

    def exit_game(self):
        """Exit game."""

        Persistor.save(self.hiscores)
        fade_surface = pygame.display.get_surface().copy()
        self.fade(fade_surface, MAX_ALPHA, MIN_ALPHA)
        sys.exit(0)

    def splash_screen(self):
        """Display splash screen."""

        pygame.time.set_timer(pygame.USEREVENT, 5000)
        surface = pygame.display.set_mode((SPLASH_WIDTH, SPLASH_HEIGHT))

        fade_surface = pygame.Surface((SPLASH_WIDTH, SPLASH_HEIGHT))
        fade_surface.blit(self.splash_image, (0, 0))
        self.fade(fade_surface, MIN_ALPHA, MAX_ALPHA)

        hiscore_list = list(self.HISCORES_TEXT)
        for n, hiscore in enumerate(self.hiscores):
            hiscore_list.append(
                "{0:>4} {1.name:>5} {1.score:>10}".format(
                    self.get_ordinal(n + 1), hiscore)
            )

        texts = (self.INFO_TEXT,
                 hiscore_list,
                 self.CREDITS_TEXT)
        text_index = 0

        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_game()
                if event.key == pygame.K_RETURN:
                    break
            elif event.type == pygame.USEREVENT:
                if text_index < len(texts) - 1:
                    text_index += 1
                else:
                    text_index = 0
            surface.blit(self.splash_image, (0, 0))
            self.font.write_lines(100, texts[text_index])
            pygame.display.flip()

    def game_over(self):
        """Display Game Over screen."""

        surface = pygame.display.get_surface()
        fade_surface = surface.copy()
        self.fade(fade_surface, MAX_ALPHA, MAX_ALPHA / 4)

        width = surface.get_width()
        clear_surface = pygame.Surface((width, 8))
        clear_surface.blit(surface, (0, 0), area=(0, 160, width, 8))

        is_hiscore = self.hiscores.is_hiscore(self.player.score)
        initials = []
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.exit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    break
            elif is_hiscore and event.type == pygame.KEYUP:
                if (pygame.K_a <= event.key <= pygame.K_z and
                            len(initials) < 3):
                    initials.append(pygame.key.name(event.key))
                elif initials and event.key in (pygame.K_BACKSPACE,
                                                pygame.K_DELETE):
                    initials.pop()
            self.font.write_lines(100, self.GAME_OVER_TEXT)
            if is_hiscore:
                self.font.write_lines(120, self.ENTER_HISCORE_TEXT)
                surface.blit(clear_surface, (0, 160))
                self.font.write(
                    56, 160, " ".join([n.upper() for n in initials]))
            pygame.display.flip()

        if is_hiscore:
            self.hiscores.add("".join(initials).upper(), self.player.score)
        fade_surface = pygame.display.get_surface().copy()
        self.fade(fade_surface, MAX_ALPHA, MIN_ALPHA)

    def update_level(self):
        """Update game level i.e. falling speed."""

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
        """Game loop."""

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
                self.exit_game()
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
        """Main loop."""

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