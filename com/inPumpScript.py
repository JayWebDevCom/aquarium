#!/usr/bin/env python3

import sys
import time

import RPi.GPIO as GPIO
import click
from ipython_genutils.py3compat import xrange

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
    sleep = time_ / progress_bar.width

    for progress in xrange(progress_bar.width):
        progress_bar.update(progress)
        time.sleep(sleep)

    progress_bar.finish()
    switch.off()


pump_in()

GPIO.cleanup(channel)
