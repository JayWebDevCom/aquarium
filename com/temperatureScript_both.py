#!/usr/bin/env python3


import time
from components.TemperatureSensor import TemperatureSensor
from AquariumLogger import AquariumLogger

logger = AquariumLogger()

device_id_1 = "28-0300a279088e"
device_id_2 = "28-0300a2792070"

temperature_sensor_1 = TemperatureSensor("test sensor", device_id_1)
temperature_sensor_2 = TemperatureSensor("test sensor", device_id_2)

num = 5
tank_temps_total = 0
sump_temps_total = 0

for i in range(0, num):
    tank_temp = temperature_sensor_1.get_temp()
    sump_temp = temperature_sensor_2.get_temp()

    tank_temps_total += tank_temp
    sump_temps_total += sump_temp
    
    logger.info("tank: " + str(tank_temp))
    logger.info("sump: " + str(sump_temp))

logger.info(f"tank average: {round(tank_temps_total/num, 2)}")
logger.info(f"sump average: {round(sump_temps_total/num, 2)}")
logger.info(f"difference: {round(abs(tank_temp-sump_temp), 2)}")
