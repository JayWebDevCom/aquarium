import RPi.GPIO as GPIO


class Switch:
    """A simple Switch example class"""
    name: str
    pin: int

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

    def on(self):
        print(f"switching on {self.name}")
        GPIO.output(self.pin, 1)

    def off(self):
        print(f"switching off {self.name}")
        GPIO.output(self.pin, 0)
