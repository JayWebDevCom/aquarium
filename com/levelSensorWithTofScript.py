#!/usr/bin/env python3
import os
from datetime import datetime
from functools import reduce

from Progress import ProgressTracker, Style
from components.LevelSensor import LevelSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy
from com.Configuration import Configuration

global level_sensor

level_sensor = LevelSensor("test level sensor", TimeOfFlightLevelStrategy())
progress_tracker = ProgressTracker()

current_dir = os.path.dirname(os.path.abspath(__file__))
configuration_file_name = "config.yaml"
configuration_file_path = f"{current_dir}/{configuration_file_name}"
config = Configuration(configuration_file_path)

times_to_check_level = config.get("times_to_check_level")
full_level = config.get("full_level")
water_change_span = config.get("water_change_span")

levels = [level_sensor.get_level() for i in range(times_to_check_level)]
average_level = reduce(lambda x, y: (x + y), levels) / times_to_check_level

difference = average_level - full_level
percent_full = 100 - (difference / water_change_span) * 100

date_time = datetime.now().strftime("%H:%M")

progress_tracker.write_ln(f"{Style.WHITE}{Style.BOLD}{date_time}:{Style.RESET}{Style.GREEN} "
                          f"level: {Style.BOLD}{Style.WHITE}{'{:.2f}'.format(average_level)}{Style.RESET}{Style.GREEN} "
                          f"full: {Style.BOLD}{Style.WHITE}{'{:.2f}'.format(percent_full)}{Style.RESET}%")
