from unittest import TestCase
import tris.playfield

__author__ = 'Lars Djerf <lars.djerf@gmail.com'


class TestPlayfield(TestCase):
    def setUp(self):
        self.width = 10
        self.height = 20
        self.playfield = tris.playfield.Playfield(self.width, self.height)

    def test_playfield_empty(self):
        """Playfield should initially be empty."""

        for y in range(self.height):
            for x in range(self.width):
                self.assertEqual(self.playfield[(x, y)], 0)

    def test_set_playfield_value(self):
        """Playfield should support setting values."""

        self.playfield[(0, 0)] = 1
        self.assertEqual(self.playfield[(0, 0)], 1)

    def test_index_error_get(self):
        """Playfield should raise IndexError for invalid coordinates."""

        invalid_coordinates = ((-1, -1),
                               (self.width, self.height),
                               (self.width + 5, self.height + 7),
                               (0, self.width),
                               (self.height, 0))

        with self.assertRaises(IndexError):
            for coordinates in invalid_coordinates:
                tmp = self.playfield[coordinates]

    def test_index_error_set(self):
        """Playfield should raise IndexError for invalid coordinates."""

        invalid_coordinates = ((-1, -1),
                               (self.width, self.height),
                               (self.width + 5, self.height + 7),
                               (0, self.width),
                               (self.height, 0))

        with self.assertRaises(IndexError):
            for coordinates in invalid_coordinates:
                self.playfield[coordinates] = 1