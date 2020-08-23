#!/usr/bin/env python3

import sys
import time

import RPi.GPIO as GPIO
import click
from ipython_genutils.py3compat import xrange

from components.Switch import Switch

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
channel = 27
GPIO.setup(channel, GPIO.OUT)

switch = Switch("pump out", channel)


@click.command()
@click.option('--time', '-t', 'time_', default=0, help='how long to turn the pump on for')
def pump_out(time_: int):
    switch.on()

    progress_bar_width = 100

    sys.stdout.write("[%s]" % (" " * progress_bar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (progress_bar_width + 1))

    for _ in xrange(progress_bar_width):
        time.sleep(time_ / progress_bar_width)
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")
    switch.off()


pump_out()

GPIO.cleanup(channel)
