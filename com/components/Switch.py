import RPi.GPIO as GPIO


class Switch:
    """A simple Switch example class"""
    name: str
    pin: int

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin

    def on(self):
        GPIO.setmode(GPIO.BCM)
        print(f"switching on {self.name}")
        GPIO.output(self.pin, 1)
        GPIO.setmode(GPIO.BOARD)

    def off(self):
        GPIO.setmode(GPIO.BCM)
        print(f"switching off {self.name}")
        GPIO.output(self.pin, 0)
        GPIO.setmode(GPIO.BOARD)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Switch):
            return self.name == other.name and self.pin == other.pin
        return False
