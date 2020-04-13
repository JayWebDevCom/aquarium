import RPi.GPIO as GPIO
import logging.config
import yaml

from components.CustomFormatter import CustomFormatter


class Switch:
    """A simple Switch example class"""
    name: str
    pin: int

    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        with open('log-config.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            self.logger = logging.getLogger(__name__)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(CustomFormatter())
            self.logger.addHandler(ch)

    def on(self):
        self.logger.info(f"switching on {self.name}")
        GPIO.output(self.pin, 1)

    def off(self):
        self.logger.info(f"switching off {self.name}")
        GPIO.output(self.pin, 0)
