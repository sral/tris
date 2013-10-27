from unittest import TestCase
from tris.playfield import Playfield
from tris.tris import Tris
from tris.trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com'


class TestTris(TestCase):
    def setUp(self):
        self.playfield = Playfield(10, 20)
        self.tris = Tris()

    def test_make_legal_move(self):
        """Legal moves should return True."""

        trimino = Trimino.get("O", 0, 0)
        moves = ((1, 0), (0, 1), (1, 0))
        for x, y in moves:
            self.assertTrue(self.tris.legal_move(self.playfield,
                                                 trimino,
                                                 (trimino.x + x, trimino.y + y)))

    def test_move_outside_of_playfield(self):
        """Illegal moves should return False."""

        # Move outside of left edge
        trimino = Trimino.get("O", 0, 0)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino,
                                              (trimino.x - 1, trimino.y)))

        # Move outside of right edge
        trimino = Trimino.get("O", 9, 0)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino,
                                              (trimino.x + 1, trimino.y)))

        # Move outside of bottom edge
        trimino = Trimino.get("O", 0, 19)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino,
                                              (trimino.x, trimino.y + 1)))