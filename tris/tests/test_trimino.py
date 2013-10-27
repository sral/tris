import unittest
from tris.trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class TestTrimino(unittest.TestCase):

    def test_get_value(self):
        trimino = Trimino.get('O', 0, 0, None)
        self.assertEqual(trimino[(0, 0)], 1)

    def test_trimino_modification(self):
        """Assignment should raise TypeError."""

        with self.assertRaises(TypeError):
            trimino = Trimino.get('S', 0, 0)
            trimino[(0, 0)] = 1


if __name__ == '__main__':
    unittest.main()
