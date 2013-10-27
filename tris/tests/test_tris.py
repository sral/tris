from unittest import TestCase
from tris.playfield import Playfield
from tris.tris import Tris
from tris.trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com'


class TestTris(TestCase):
    def setUp(self):
        self.playfield = Playfield(10, 20, None)
        self.tris = Tris()

    def test_make_legal_move(self):
        """Legal moves should return True."""

        trimino = Trimino.get("O", 0, 0, None)
        #moves = (move_right, trimino.move_down, trimino.move_left)
        #for move in moves:
        #    self.assertTrue(self.tris.legal_move(self.playfield,
        #                                         move()))

    def test_move_outside_of_playfield(self):
        """Illegal moves should return False."""

        # Move outside of left edge
        trimino = Trimino.get("O", 0, 0, None)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino.move_left()))

        # Move outside of right edge
        trimino = Trimino.get("O", 9, 0, None)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino.move_right()))

        # Move outside of bottom edge
        trimino = Trimino.get("O", 0, 19, None)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino.move_down()))