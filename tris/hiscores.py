from collections import namedtuple

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

HiScore = namedtuple("HiScore", "name score")


class HiScores(object):
    def __init__(self, default_scores=None, max_scores=10):
        """Initialize instance.

        Keyword arguments:
        default_scores -- Default hiscore list
        max_scores -- Max numbers of scores in hiscore list
        """

        self.max_scores = max_scores
        self.hiscores = default_scores or []

    def is_hiscore(self, score):
        """Returns True if score is a hiscore, False otherwise."""

        if not self.hiscores:
            return True
        return (len(self.hiscores) < self.max_scores or
                score > self.hiscores[-1].score)

    def add(self, name, score):
        """Add new hiscore to hiscore_list.

        Keyword arguments:
        name -- Player name
        score -- Player Score
        """

        self.hiscores.append(HiScore(name, score))
        self.hiscores.sort(key=lambda n: n.score, reverse=True)
        if len(self.hiscores) > self.max_scores:
            self.hiscores.pop()

    @classmethod
    def get_default_hiscore_list(cls):
        default_scores = [HiScore("SUP", 1000),
                          HiScore("POR", 900),
                          HiScore("T Y", 800),
                          HiScore("OUR", 700),
                          HiScore("LOC", 600),
                          HiScore("AL ", 500),
                          HiScore("PYT", 400),
                          HiScore("HON", 300),
                          HiScore("IST", 200),
                          HiScore("A!!", 100)]

        return cls(default_scores=default_scores, max_scores=10)

    def __iter__(self):
        for score in self.hiscores:
            yield score