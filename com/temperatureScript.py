#!/usr/bin/env python3

import time
from components.TemperatureSensor import TemperatureSensor
from AquariumLogger import AquariumLogger

logger = AquariumLogger()
device_id = "28-0300a279088e"
# device_id = "28-0300a2792070"

temperature_sensor = TemperatureSensor("test sensor", device_id)

for i in range(0, 10):
    time.sleep(1)
    logger.info(temperature_sensor.get_temp())
