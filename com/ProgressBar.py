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
    spaces = "            "

    def write(self, to_write):
        sys.stdout.write("\b" * (len(self.written_value) + (2 * len(self.spaces))))
        sys.stdout.write("\033[1;34m")
        write = f"->  {to_write}{self.spaces}"
        sys.stdout.write(write)
        self.written_value = write
        sys.stdout.flush()

    @staticmethod
    def finish():
        sys.stdout.write("\033[0;0m")
        sys.stdout.write("\n")