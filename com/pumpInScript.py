#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

from AquariumLogger import AquariumLogger
from components.Switch import Switch

logger = AquariumLogger()

GPIO.setmode(GPIO.BCM)
channel = 23
GPIO.setup(channel, GPIO.OUT)

switch = Switch("test switch", channel)

for i in range(0, 1):
    logger.info("activating switch…")
    switch.on()
    time.sleep(10)
    logger.info("de-activating switch…")
    switch.off()

GPIO.cleanup(channel)
