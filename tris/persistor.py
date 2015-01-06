import pickle
import os.path

__author__ = 'Lars Djerf <lars.djerf@gmail.com>'

HISCORE_PATH = os.path.join(os.path.expanduser("~"), ".trisscores")


class Persistor(object):
    @staticmethod
    def save(obj):
        """Persist object.

        Keyword arguments:
        obj -- The object to persist
        """

        try:
            with open(HISCORE_PATH, "w+b") as f:
                pickle.dump(obj, f)
        except (IOError, pickle.PickleError):
            pass

    @staticmethod
    def load():
        """Load object."""

        try:
            with open(HISCORE_PATH, "rb") as f:
                return pickle.load(f)
        except (IOError, pickle.PickleError):
            return False
