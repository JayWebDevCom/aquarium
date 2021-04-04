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

num = 2
tank_temps = [round(tank_temp_sensor.get_temp(), 2) for _ in range(num)]
sump_temps = [round(sump_temp_sensor.get_temp(), 2) for _ in range(num)]

tank_temp_average = reduce(lambda x, y: (x + y), tank_temps) / num
sump_temp_average = reduce(lambda x, y: (x + y), sump_temps) / num

tank_average = f"{'{:.2f}'.format(tank_temp_average)}"
sump_average = f"{'{:.2f}'.format(sump_temp_average)}"
difference = f"{'{:.2f}'.format(abs(tank_temp_average - sump_temp_average))}"

date_time = datetime.now().strftime("%H:%M")
progress_tracker = ProgressTracker()

print("")
progress_tracker.write_ln(f"{Style.WHITE}{Style.BOLD}{date_time}: {Style.RESET}"
                          f"{Style.GREEN}tank temp:{Style.RESET}{Style.BOLD}{Style.WHITE} {tank_average}{Style.RESET}°c, "
                          f"{Style.GREEN}sump temp:{Style.RESET}{Style.BOLD}{Style.WHITE} {sump_average}{Style.RESET}°c, "
                          f"{Style.GREEN}difference:{Style.RESET}{Style.BOLD}{Style.WHITE} {difference}{Style.RESET}°c")

progress_tracker.write_ln(f"{Style.WHITE}{Style.BOLD}{date_time}: {Style.RESET}"
                          f"{Style.GREEN}tank temps: {Style.WHITE}{Style.BOLD}{tank_temps},{Style.RESET} "
                          f"{Style.GREEN}sump temps {Style.WHITE}{Style.BOLD}{sump_temps}{Style.RESET}")

