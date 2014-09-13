import pickle

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'


class Persistor(object):

    @staticmethod
    def save(path, obj):
        """Persist object.

        Keyword arguments:
        path -- Target path
        obj -- The object
        """

        with open(path, "w+b") as f:
            pickle.dump(obj, f)

    @staticmethod
    def load(path):
        """Load object.

        Keyword arguments:
        path -- Source path
        """

        with open(path, "rb") as f:
            return pickle.load(f)
