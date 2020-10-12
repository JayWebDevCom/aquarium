import math
import sys


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
    line_length = 30
    space = " "
    prompt = f"{Style.DARK_GREY}{Style.BOLD}->{Style.RESET} "

    def write(self, to_write):
        sys.stdout.write("\b" * len(self.written_value))
        write = f"{self.prompt}{to_write}{self.space * (self.line_length - len(to_write))}"
        sys.stdout.write(write)
        self.written_value = write
        sys.stdout.flush()

    @staticmethod
    def finish():
        sys.stdout.write(Style.RESET)
        sys.stdout.write("\n")

    def write_ln(self, to_write):
        self.write(to_write)
        self.finish()



