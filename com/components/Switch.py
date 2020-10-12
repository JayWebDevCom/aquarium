import RPi.GPIO as GPIO

from Progress import ProgressTracker, Style


class Switch:
    """A simple Switch example class"""
    name: str
    pin: int

    def __init__(self, name, pin, progress_tracker: ProgressTracker):
        self.name = name
        self.pin = pin
        self.progress_tracker = progress_tracker

    def on(self):
        self._log("switching on")
        GPIO.output(self.pin, 1)

    def off(self):
        self._log("switching off")
        GPIO.output(self.pin, 0)

    def _log(self, message):
        self.progress_tracker.write_ln(f"{Style.LIGHT_RED}{message} {self.name}")
