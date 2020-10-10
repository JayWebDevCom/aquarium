import math
import sys


class ProgressBar:

    written = 0

    def __init__(self, width: int = 100):
        self.width = width

    def initialize(self):
        sys.stdout.write("[%s]" % (" " * self.width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (self.width + 1))

    def update(self, progress_level: float):
        sys.stdout.write("\b" * math.ceil(self.written))
        sys.stdout.write("-" * math.ceil(progress_level))
        self.written = progress_level
        sys.stdout.flush()

    @staticmethod
    def finish():
        sys.stdout.write("]\n")


class ProgressTracker:

    written_value = ""
    spaces = " " * 25

    def __init__(self, colour_code: str = "\033[1;34m"):
        self.colour_code = colour_code

    def write(self, to_write):
        sys.stdout.write("\b" * (len(self.written_value) + (len(self.spaces))))
        sys.stdout.write(f"{self.colour_code}")
        write = f"->  {to_write}{self.spaces}"
        sys.stdout.write(write)
        self.written_value = write
        sys.stdout.flush()

    @staticmethod
    def finish():
        sys.stdout.write("\033[0;0m")
        sys.stdout.write("\n")
