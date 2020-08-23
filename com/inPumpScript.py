#!/usr/bin/env python3

import sys
import time

import RPi.GPIO as GPIO
import click
from ipython_genutils.py3compat import xrange

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

    progress_bar_width = 100

    sys.stdout.write("[%s]" % (" " * progress_bar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (progress_bar_width + 1))

    sleep = time_ / progress_bar_width
    for _ in xrange(progress_bar_width):
        time.sleep(sleep)
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")
    switch.off()


pump_in()

GPIO.cleanup(channel)
