#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO
import click

from Progress import ProgressBar, ProgressTracker
from components.Switch import Switch

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = 23
GPIO.setup(channel, GPIO.OUT)

switch = Switch("Pump in", channel, ProgressTracker())


@click.command()
@click.option('--time', '-t', 'time_', default=0, help='How long to turn the pump on for')
def pump_in(time_: int):
    switch.on()

    progress_bar = ProgressBar()
    progress_bar.initialize()

    for i in range(time_):
        time.sleep(1)
        percentage = (i + 1) / time_ * progress_bar.width
        progress_bar.update(percentage)

    progress_bar.finish()
    switch.off()


pump_in()

GPIO.cleanup(channel)
