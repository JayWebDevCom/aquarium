import math
import sys


class ProgressBar:

    def __init__(self, width: int = 100):
        self.width = width

    def initialize(self):
        sys.stdout.write("[%s]" % (" " * self.width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.width + 1))

    @staticmethod
    def update(progress_level: float):
        sys.stdout.write("-" * math.ceil(progress_level))
        sys.stdout.flush()

    @staticmethod
    def finish():
        sys.stdout.write("]\n")
