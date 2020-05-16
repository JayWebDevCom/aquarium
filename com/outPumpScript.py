#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import click

from AquariumLogger import AquariumLogger
from components.Switch import Switch

logger = AquariumLogger()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = 27
GPIO.setup(channel, GPIO.OUT)

switch = Switch("pump out", channel)

@click.command()
@click.option('--time', '-t', 'time_', default=0, help='how long to turn the pump on for')
def pump_out(time_: int):
    logger.info(f"activating {switch.name} for {time_} seconds")
    switch.on()
    time.sleep(time_)
    logger.info("de-activating switch…")
    switch.off()

pump_out()

GPIO.cleanup(channel)
