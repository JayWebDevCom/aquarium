#!/usr/bin/env python3

import time

from components.LevelSensor import LevelSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy

level_sensor = LevelSensor("test level sensor", TimeOfFlightLevelStrategy())

num = 5
sum = 0

for i in range(0, num):
    time.sleep(1)
    temp = level_sensor.get_level()
    sum += temp

message = f"average level: {sum/num}\n\n"

with open("aquarium.txt", "a") as f:
    f.write(message)
