#!/usr/bin/env python3
import time
from components.LevelSensor import LevelSensor

level_sensor = LevelSensor("test level sensor")

for i in range(0, 10):
    time.sleep(1)
    print(level_sensor.get_level())


