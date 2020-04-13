#!/usr/bin/env python3

import time
from components.TemperatureSensor import TemperatureSensor
from AquariumLogger import AquariumLogger

logger = AquariumLogger()

device_id_1 = "28-0300a279088e"
device_id_2 = "28-0300a2792070"

temperature_sensor_1 = TemperatureSensor("test sensor", device_id_1)
temperature_sensor_2 = TemperatureSensor("test sensor", device_id_2)

for i in range(0, 10):
    time.sleep(1)
    logger.info(device_id_1 + ": " + str(temperature_sensor_1.get_temp()))
    logger.info(device_id_2 + ": " + str(temperature_sensor_2.get_temp()))
