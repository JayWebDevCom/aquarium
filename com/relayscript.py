#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
channel = 3
GPIO.setup(channel, GPIO.OUT)

print("activating 1…")
GPIO.output(channel, 1)

time.sleep(1)

print("de-activating 1…")
GPIO.output(channel, 0)

time.sleep(1)

print("activating 2…")
GPIO.output(channel, 1)

time.sleep(1)

print("de-activating 2…")
GPIO.output(channel, 0)

time.sleep(1)

print("activating 3…")
GPIO.output(channel, 1)

time.sleep(1)

print("de-activating 3…")
GPIO.output(channel, 0)

GPIO.cleanup(channel)
