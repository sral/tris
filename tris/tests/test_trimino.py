import unittest
from tris.trimino import Trimino

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class TestTrimino(unittest.TestCase):
    def test_get_value(self):
        """Triminos should support reading values from matrix.

        1. Spawn trimino 'O' i.e. square
        => Fetching (0, 0) from matrix should yield 1.
        """

        trimino = Trimino.get('O', 0, 0, None)
        self.assertEqual(trimino[(0, 0)], 1)

    def test_trimino_modification(self):
        """Assignment should raise TypeError.

        1.) Modify trimino matrix
        => TypeError is raised.
        """

        with self.assertRaises(TypeError):
            trimino = Trimino.get('S', 0, 0, None)
            trimino[(0, 0)] = 1

    def test_get_legal_trimino(self):
        """It should be possible to get all know trimino-types.
        Prerequisites:
        - Legal triminos are I, J, L, O, S, T and Z.

        1.) Get all legal triminos
        => Triminos are returned, no exceptions are raised.
        """

        legal_triminos = ('I', 'J', 'L', 'O', 'S', 'T', 'Z')

        for shape in legal_triminos:
            self.assertIsInstance(Trimino.get(shape, 0, 0, None), Trimino)


    def test_get_illegal_trimino(self):
        """Getting unknown trimino should raise ValueError.

         Prerequisites:
         - Legal triminos are I, J, L, O, S, T and Z.

         1.) Get trimino 'G' which does not exist
         => ValueError is raised.
        """

        with self.assertRaises(ValueError):
            Trimino.get('G', 0, 0, None)


if __name__ == '__main__':
    unittest.main()
