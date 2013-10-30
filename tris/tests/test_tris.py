from unittest import TestCase
from tris.playfield import Playfield
from tris.tris import Tris
from tris.trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com'


class TestTris(TestCase):
    def setUp(self):
        self.playfield = Playfield(10, 20, None)
        self.tris = Tris()

    def test_move_trimino_on_playfield(self):
        """Moving trimino inside of playfield is legal.

        Prerequisites:
        - Triminio is in top right corner (0, 0)

        1.) Move trimino right
        2.) Move trimino left
        3.) Move trimino down
        4.) Move trimino up
        => legal_move() returns True for all moves.
        """

        trimino = Trimino.get("O", 0, 0, None)
        self.assertTrue(self.tris.legal_move(self.playfield,
                                             trimino.move_right()))
        self.assertTrue(self.tris.legal_move(self.playfield,
                                             trimino.move_left()))
        self.assertTrue(self.tris.legal_move(self.playfield,
                                             trimino.move_down()))
        self.assertTrue(self.tris.legal_move(self.playfield,
                                             trimino.move_up()))

    def test_move_trimino_outside_of_playfield(self):
        """Moving trimino outside of playfield is not allowed.

        1.) Move trimino outside of left edge
        2.) Move trimino outside of right edge
        3.) Move trimino outside of bottom edge
        => legal_move() return False for all moves.
        """

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

    def test_move_right_is_blocked(self):
        """Movement right is blocked.

        Prerequisites:
        - Trimino is in top left corner (0, 0)
        - Playfield to the right is all ready occupied

        1.) Move trimino right
        => Move not allowed, legal_move() returns False
        """

        self.playfield.place_trimino(Trimino.get("O", 2, 0, None))
        trimino = Trimino.get("O", 0, 0, None)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino.move_right()))

    def test_move_left_is_blocked(self):
        """Movement left is blocked.

        Prerequisites:
        - Trimino is two moves to the right (2, 0)
        - Playfield to the left is all ready occupied

        1.) Move trimino left
        => Move not allowed, legal_move() returns False
        """

        self.playfield.place_trimino(Trimino.get("O", 0, 0, None))
        trimino = Trimino.get("O", 2, 0, None)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino.move_left()))

    def test_move_down_is_blocked(self):
        """Movement down is blocked.

        Prerequisites:
        - Trimino is in top left corner (0, 0)
        - Playfield below trimino is all ready occupied

        1.) Move trimino down
        => Move not allowed, legal_move() returns False
        """

        self.playfield.place_trimino(Trimino.get("O", 0, 2, None))
        trimino = Trimino.get("O", 0, 0, None)
        self.assertFalse(self.tris.legal_move(self.playfield,
                                              trimino.move_down()))