#!/usr/bin/env python3
import os
from datetime import datetime
from functools import reduce

from Configuration import Configuration
from Progress import ProgressTracker, Style
from components.TemperatureSensor import TemperatureSensor

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = "config.yaml"
c_file = f"{current_dir}/{config_file}"
config = Configuration(c_file)

global tank_temp_sensor
global sump_temp_sensor
tank_temp_sensor = TemperatureSensor("tank sensor", config.get("tank_temp_device_id"))
sump_temp_sensor = TemperatureSensor("sump sensor", config.get("sump_temp_device_id"))

num = 1
tank_temps = [tank_temp_sensor.get_temp() for _ in range(num)]
sump_temps = [sump_temp_sensor.get_temp() for _ in range(num)]

tank_temp_average = reduce(lambda x, y: (x + y), tank_temps) / num
sump_temp_average = reduce(lambda x, y: (x + y), sump_temps) / num

date_time = datetime.now().strftime("%H:%M")
tank_average = f"tank average: {'{:.2f}c'.format(tank_temp_average)}"
sump_average = f"sump average: {'{:.2f}c'.format(sump_temp_average)}"
difference = f"difference: {'{:.2f}'.format(abs(tank_temp_average - sump_temp_average))}"

print("")
progress_tracker = ProgressTracker()
progress_tracker.write_ln(f"{Style.BOLD}{Style.WHITE}{date_time}: {tank_average}, {sump_average}, {difference}")
