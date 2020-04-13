#!/usr/bin/env python3

import time

from AquariumLogger import AquariumLogger
from components.LevelSensor import LevelSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy

level_sensor = LevelSensor("test level sensor", TimeOfFlightLevelStrategy())
logger = AquariumLogger()

for i in range(0, 10):
    time.sleep(1)
    logger.info(level_sensor.get_level())
