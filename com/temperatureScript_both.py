#!/usr/bin/env python3
from functools import reduce

from AquariumLogger import AquariumLogger
from components.TemperatureSensor import TemperatureSensor
from datetime import datetime

logger = AquariumLogger()

tank_device = "28-01191c5f02ae"
sump_device = "28-01191c6c5b42"

global tank_temp_sensor
global sump_temp_sensor

tank_temp_sensor = TemperatureSensor("test sensor", tank_device)
sump_temp_sensor = TemperatureSensor("test sensor", sump_device)

num = 1
tank_temps = [tank_temp_sensor.get_temp() for i in range(num)]
sump_temps = [sump_temp_sensor.get_temp() for i in range(num)]

tank_temp_average = reduce(lambda x, y: (x + y), tank_temps) / num
sump_temp_average = reduce(lambda x, y: (x + y), sump_temps) / num

print("")
logger.info(datetime.now().strftime("%H:%M"))
logger.info(f"tank average: {'{:.2f}'.format(tank_temp_average)}")
logger.info(f"sump average: {'{:.2f}'.format(sump_temp_average)}")
logger.info(f"difference: {'{:.2f}'.format(abs(tank_temp_average - sump_temp_average))}")

