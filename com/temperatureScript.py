#!/usr/bin/env python3

import time

from AquariumLogger import AquariumLogger
from components.TemperatureSensor import TemperatureSensor

logger = AquariumLogger()
device_id = "28-0300a279088e"
# device_id = "28-0300a2792070"

db_device_filepath = f"/sys/bus/w1/devices/{device_id}/w1_slave"

temperature_sensor = TemperatureSensor("test sensor", db_device_filepath)

for i in range(0, 10):
    time.sleep(1)
    logger.info(temperature_sensor.get_temp())
