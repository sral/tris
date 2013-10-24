import unittest
from tris.trimino import TriminoO

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class TestTrimino(unittest.TestCase):
    def setUp(self):
        self.trimino = TriminoO(4, 4)

    def test_get_value(self):
        self.assertEqual(self.trimino[(0, 0)], 1)

    def test_trimino_modification(self):
        """Assignment should raise TypeError."""

        with self.assertRaises(TypeError):
            self.trimino[(0, 0)] = 1


if __name__ == '__main__':
    unittest.main()
