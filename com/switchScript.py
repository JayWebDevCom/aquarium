#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

from components.Switch import Switch

GPIO.setmode(GPIO.BOARD)
channel = 6
GPIO.setup(channel, GPIO.OUT)

switch = Switch("test switch", channel)

for i in range(0, 5):
    print("activating switch…")
    switch.on()
    time.sleep(1)
    print("de-activating switch…")
    switch.off()
    time.sleep(1)

GPIO.cleanup(channel)
