#!/usr/bin/env python3

import time

from AquariumLogger import AquariumLogger
from components.dependencies import VL53L0X 

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
logger = AquariumLogger()

while True:
    d = tof.get_distance()
    logger.info(d)
    time.sleep(1)
