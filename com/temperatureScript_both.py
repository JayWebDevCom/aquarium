#!/usr/bin/env python3

from components.TemperatureSensor import TemperatureSensor

tank_device = "28-0300a279088e"
sump_device = "28-0300a2792070"

tank_temp_sensor = TemperatureSensor("test sensor", tank_device)
sump_temp_sensor = TemperatureSensor("test sensor", sump_device)

num = 5
tank_temps_total = 0
sump_temps_total = 0

tank_temp, sump_temp = 0, 0

for i in range(0, num):
    tank_temp = tank_temp_sensor.get_temp()
    sump_temp = sump_temp_sensor.get_temp()

    tank_temps_total += tank_temp
    sump_temps_total += sump_temp

message = f"tank average: {round(tank_temps_total/num, 2)}\n"
message += f"sump average: {round(sump_temps_total/num, 2)}\n"
message += f"difference: {round(abs(tank_temp-sump_temp), 2)}\n"

with open("aquarium.txt", "a") as f:
    f.write(message)
