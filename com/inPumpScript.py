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

    sys.stdout.write("[%s]" % (" " * time_))
    sys.stdout.flush()
    sys.stdout.write("\b" * (time_ + 1))

    for _ in xrange(time_):
        time.sleep(1)
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")
    switch.off()


pump_in()

GPIO.cleanup(channel)
