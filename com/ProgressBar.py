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

    def write_ln(self, to_write):
        self.write(to_write)
        self.finish()


class Style:

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    ORANGE = '\033[33m'
    PURPLE = '\033[35m'
    LIGHT_GREY = '\033[37m'
    DARK_GREY = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_BLUE = '\033[94m'
    PINK = '\033[95m'
