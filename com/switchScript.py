#!/usr/bin/env python3

import time

import RPi.GPIO as GPIO
import click

from Progress import ProgressBar, ProgressTracker
from components.Switch import Switch

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


@click.command()
@click.option('--time', '-t', 'time_', default=0, help='How long to turn the switch on for')
@click.option('--switch', '-s', 'switch_name', required=True, help='Which switch to activate [pump_out, pump_in, tank_drain]')
@click.option('--cleanup', '-c', is_flag=True, help='Whether to run `GPIO.cleanup(channel)`')
def switch(time_: int, switch_name: str, cleanup: str):
    switches = {
        'pump_out': 27,
        'pump_in': 23,
        'tank_drain': 5
    }

    channel = switches[switch_name]
    GPIO.setup(channel, GPIO.OUT)
    s = Switch(switch_name, channel, ProgressTracker())
    s.on()

    progress_bar = ProgressBar()
    progress_bar.initialize()

    for i in range(time_):
        time.sleep(1)
        percentage = (i + 1) / time_ * progress_bar.width
        progress_bar.update(percentage)

    progress_bar.finish()

    s.off()

    if cleanup:
        print(f'cleaning up {channel}')
        GPIO.cleanup(channel)


switch()
