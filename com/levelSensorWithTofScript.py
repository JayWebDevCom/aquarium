#!/usr/bin/env python3

import time

from AquariumLogger import AquariumLogger
from components.LevelSensor import LevelSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy

logger = AquariumLogger()

level_sensor = LevelSensor("test level sensor", TimeOfFlightLevelStrategy())

num = 15; sum = 0

for i in range(0, num):
    time.sleep(1)
    temp = level_sensor.get_level()
    sum += temp

logger.info(f"average level: {round(sum/num, 2)}")
