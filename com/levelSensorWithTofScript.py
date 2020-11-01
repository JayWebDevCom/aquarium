#!/usr/bin/env python3
from datetime import datetime
from functools import reduce

from Progress import ProgressTracker, Style
from components.LevelSensor import LevelSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy

global level_sensor

level_sensor = LevelSensor("test level sensor", TimeOfFlightLevelStrategy())
progress_tracker = ProgressTracker()

num = 7
levels = [level_sensor.get_level() for i in range(num)]

average_level = reduce(lambda x, y: (x + y), levels) / num
date_time = datetime.now().strftime("%H:%M")

progress_tracker.write_ln(f"{Style.WHITE}{Style.BOLD}{date_time}:{Style.RESET}{Style.GREEN} "
                          f"level: {Style.BOLD}{Style.WHITE}{'{:.2f}'.format(average_level)}")

