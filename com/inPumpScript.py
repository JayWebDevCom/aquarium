#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO
import click

from ProgressBar import ProgressBar
from components.Switch import Switch

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = 23
GPIO.setup(channel, GPIO.OUT)

switch = Switch("Pump in", channel)


@click.command()
@click.option('--time', '-t', 'time_', default=0, help='How long to turn the pump on for')
def pump_in(time_: int):
    switch.on()

    progress_bar = ProgressBar()
    progress_bar.initialize()

    for i in range(time_):
        percentage = (i + 1) / time_ * progress_bar.width
        progress_bar.update(percentage)
        time.sleep(1)

    progress_bar.finish()
    switch.off()


pump_in()

GPIO.cleanup(channel)
