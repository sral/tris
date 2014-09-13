from collections import namedtuple

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class HiScores(object):

    HiScore = namedtuple("HiScore", "name score")

    def __init__(self, max_scores=10):
        """Initialize instance.

        Keyword arguments:
        max_scores -- Max numbers of scores in hiscore list
        """
        self.max_scores = max_scores
        self.scores = []

    def is_hiscore(self, score):
        """Returns True if score is a hiscore, False otherwise."""

        if not self.scores:
            return True
        return score > self.scores[-1].score

    def add(self, name, score):
        """Add new hiscore to hiscore_list.

        Keyword arguments:
        name -- Player name
        score -- Player Score
        """

        self.scores.append(self.HiScore(name, score))
        self.scores.sort(key=lambda n: n.score, reverse=True)
        if len(self.scores) > self.max_scores:
            self.scores.pop()

    def __iter__(self):
        for score in self.scores:
            yield score