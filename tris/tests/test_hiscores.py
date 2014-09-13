import unittest
from tris.hiscores import HiScores

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class TestHiScores(unittest.TestCase):
    def setUp(self):
        self.max_scores = 5
        self.hiscores = HiScores(max_scores=self.max_scores)

    def test_add_score(self):
        """It should be possible to add a new hiscore.

        1.) Add score
        => List contains score
        """

        self.hiscores.add("LTD", 42)

        expected_hiscore_list = [("LTD", 42)]
        self.assertEqual(self.hiscores.scores, expected_hiscore_list)

    def test_add_score_drops_lowest_score(self):
        """IF the list is full the lowest score is dropped

        1.) Fill the list with scores
        2.) Add new score
        => The lowest score is dropped from the list
        """

        for score in range(self.max_scores):
            self.hiscores.add("LTD", score)
        self.hiscores.add("LTD", 42)

        expected_lowest_score = ("LTD", 1)

        self.assertEqual(self.hiscores.scores[-1], expected_lowest_score)

    def test_add_score_sorts_list(self):
        """HiScores list should accept and sort scores.

        1.) Add score 1234 for "LTD"
        2.) Add score 42 for "LTD"
        3.) Add score 4321 for "LTD"
        => All scores are added, the list is sorted (high to low)
        """

        self.hiscores.add("LTD", 1234)
        self.hiscores.add("LTD", 42)
        self.hiscores.add("LTD", 4231)

        expected_hiscore_list = [("LTD", 4231), ("LTD", 1234), ("LTD", 42)]

        self.assertEqual(self.hiscores.scores, expected_hiscore_list)

    def test_is_hiscore(self):
        """New scores should be correctly compared to the hiscore list

        1.) Fill the list with scores [2, 7)
        2.) Compare scores 1 and 7 to the list
        => The first score (1) is not a a hiscore.
           The second score (7) is a hiscore.
        """

        for score in range(2, 7):
            self.hiscores.add("LTD", score)

        self.assertTrue(self.hiscores.is_hiscore(7))
        self.assertFalse(self.hiscores.is_hiscore(1))

    def test_is_hiscore_empty_list(self):
        """A score is a hiscore if the list is empty.

        1.) Create new empty list
        2.) Check if a score is a hiscore
        => The score is considered a hiscore
        """

        self.assertTrue(self.hiscores.is_hiscore(9))

    def test_hiscore_list_should_be_iterable(self):
        """HiScore list should be iterable.

         1.) Add scores
         2.) Iterate over list
         => Iteration is successful
        """
        expected_scores = [("LTD", 3), ("LTD", 2), ("LTD", 1)]

        for name, score in expected_scores:
            self.hiscores.add(name, score)

        for hiscore, expected_score in zip(self.hiscores, expected_scores):
            self.assertEqual(hiscore, expected_score)
