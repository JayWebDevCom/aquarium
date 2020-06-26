#!/usr/bin/env python3

from AquariumLogger import AquariumLogger
from components.TemperatureSensor import TemperatureSensor
from datetime import datetime

logger = AquariumLogger()

tank_device = "28-0300a279088e"
sump_device = "28-0300a2792070"

tank_temp_sensor = TemperatureSensor("test sensor", tank_device)
sump_temp_sensor = TemperatureSensor("test sensor", sump_device)

num = 3
tank_temps_total = 0
sump_temps_total = 0

tank_temp, sump_temp = 0, 0

for i in range(0, num):
    tank_temp = tank_temp_sensor.get_temp()
    sump_temp = sump_temp_sensor.get_temp()

    tank_temps_total += tank_temp
    sump_temps_total += sump_temp

print("")
logger.info(datetime.now().strftime("%H:%M"))
logger.info(f"tank average: {'{:.2f}'.format(tank_temps_total/num)}")
logger.info(f"sump average: {'{:.2f}'.format(sump_temps_total/num)}")
logger.info(f"difference: {'{:.2f}'.format(abs(tank_temp-sump_temp))}")

