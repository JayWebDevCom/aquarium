import RPi.GPIO as GPIO

from ProgressBar import ProgressTracker, Style


class Switch:
    """A simple Switch example class"""
    name: str
    pin: int

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.progress_tracker = ProgressTracker(Style.RED)

    def on(self):
        self.progress_tracker.write_ln(f"switching on {self.name}")
        GPIO.output(self.pin, 1)

    def off(self):
        self.progress_tracker.write_ln(f"switching off {self.name}")
        GPIO.output(self.pin, 0)
