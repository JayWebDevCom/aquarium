#!/usr/bin/env python3

from AquariumLogger import AquariumLogger
from components.LevelSensor import LevelSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy
from functools import reduce

global level_sensor

logger = AquariumLogger()

level_sensor = LevelSensor("test level sensor", TimeOfFlightLevelStrategy())

num = 7
levels = [level_sensor.get_level() for i in range(num)]

average_level = reduce(lambda x, y: (x + y), levels) / num 

logger.info(f"average level: {'{:.2f}'.format(average_level)}")

