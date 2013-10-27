from unittest import TestCase
from tris.playfield import Playfield

__author__ = 'Lars Djerf <lars.djerf@gmail.com'


class TestPlayfield(TestCase):
    def setUp(self):
        self.width = 10
        self.height = 20
        self.playfield = Playfield(self.width,
                                   self.height,
                                   None)

    def test_playfield_empty(self):
        """Playfield should initially be empty.

        1.) Create new playfield
        => Playfield should be empty
        """

        for y in range(self.height):
            for x in range(self.width):
                self.assertEqual(self.playfield[(x, y)], 0)

    def test_set_playfield_value(self):
        """Playfield should support setting values.

        1.) Set value in playfield
        => Get should return same value

        """

        self.playfield[(0, 0)] = 1
        self.assertEqual(self.playfield[(0, 0)], 1)

    def test_index_error_get(self):
        """Playfield should raise IndexError for invalid coordinates.

        1.) Get value outside of Playfield
        => IndexError is raised
        """

        invalid_coordinates = ((-1, -1),
                               (self.width, self.height),
                               (self.width + 5, self.height + 7),
                               (0, self.width),
                               (self.height, 0))

        with self.assertRaises(IndexError):
            for coordinates in invalid_coordinates:
                tmp = self.playfield[coordinates]

    def test_index_error_set(self):
        """Playfield should raise IndexError for invalid coordinates.

        1.) Set value outside of Playfield
        => IndexError is raised
        """

        invalid_coordinates = ((-1, -1),
                               (self.width, self.height),
                               (self.width + 5, self.height + 7),
                               (0, self.width),
                               (self.height, 0))

        with self.assertRaises(IndexError):
            for coordinates in invalid_coordinates:
                self.playfield[coordinates] = 1

    def test_find_single_line(self):
        """Playfield should return single line found.

        1.) Fill last line
        => find_lines() should return 1 line found
        """

        for x in range(self.width):
            self.playfield[(x, self.height-1)] = 1

        self.assertEqual(self.playfield.find_lines(), 1)


    def test_find_multiple_lines(self):
        """Playfield should return correct number of lines found.

        1.) Fill last three line
        => find_lines() should return 3 lines found
        """

        for y in range(self.height-1, self.height-4, -1):
            for x in range(self.width):
                self.playfield[(x, y)] = 1

        self.assertEqual(self.playfield.find_lines(), 3)