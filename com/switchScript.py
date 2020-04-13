#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

from AquariumLogger import AquariumLogger
from components.Switch import Switch

logger = AquariumLogger()

GPIO.setmode(GPIO.BCM)
# BCM mode GPIO channels 17, 27, 23
channel = 17
GPIO.setup(channel, GPIO.OUT)

switch = Switch("test switch", channel)

for i in range(0, 5):
    logger.info("activating switch…")
    switch.on()
    time.sleep(1)
    logger.info("de-activating switch…")
    switch.off()
    time.sleep(1)

GPIO.cleanup(channel)
