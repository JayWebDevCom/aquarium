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


class ProgressTracker:

    written_value = ""
    spaces = "   "

    def write(self, to_write):
        sys.stdout.write("\b" * (len(self.written_value) + len(self.spaces)))
        sys.stdout.write(to_write + self.spaces)
        self.written_value = to_write
        sys.stdout.flush()

    @staticmethod
    def finish():
        sys.stdout.write("\n")
