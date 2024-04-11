#!/usr/bin/env python3
from datetime import datetime
from functools import reduce

from Progress import ProgressTracker, Style

global level_sensor

progress_tracker = ProgressTracker()

number_of_times_to_check_level = 7
full_level = 25
water_change_span = 20.5

levels = [level_sensor.get_level() for i in range(number_of_times_to_check_level)]
average_level = reduce(lambda x, y: (x + y), levels) / number_of_times_to_check_level

difference = average_level - full_level
percent_full = 100 - (difference / water_change_span) * 100

date_time = datetime.now().strftime("%H:%M")

progress_tracker.write_ln(f"{Style.WHITE}{Style.BOLD}{date_time}:{Style.RESET}{Style.GREEN} "
                          f"level: {Style.BOLD}{Style.WHITE}{'{:.2f}'.format(average_level)}{Style.RESET}{Style.GREEN} "
                          f"full percentage: {Style.BOLD}{Style.WHITE}{'{:.2f}'.format(percent_full)} ")
