#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import click

from AquariumLogger import AquariumLogger
from components.Switch import Switch

logger = AquariumLogger()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = 23
GPIO.setup(channel, GPIO.OUT)

switch = Switch("Pump in", channel)

@click.command()
@click.option('--time', '-t', 'time_', default=0, help='How long to turn the pump on for')
def pump_in(time_: int):
    logger.info(f"activating {switch.name} for {time_} seconds")
    switch.on()
    time.sleep(time_)
    logger.info("de-activating switch…")
    switch.off()

pump_in()

GPIO.cleanup(channel)
