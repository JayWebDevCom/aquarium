import os
import time

import RPi.GPIO as GPIO
import schedule

from AquariumLogger import AquariumLogger
from Configuration import Configuration
from Controller import Controller
from Progress import ProgressTracker, Style
from components.LevelDetector import LevelDetector
from components.LevelSensor import LevelSensor
from components.LevelsBoundary import LevelsBoundary
from components.ReadingsSanitizer import ReadingsSanitizer
from components.Switch import Switch
from components.TemperatureDetector import TemperatureDetector
from components.TemperatureSensor import TemperatureSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = AquariumLogger()
progress_tracker = ProgressTracker()

current_dir = os.path.dirname(os.path.abspath(__file__))
configuration_file_name = "config.yaml"
configuration_file_path = f"{current_dir}/{configuration_file_name}"
config = Configuration(configuration_file_path)

full_level = config.get("full_level")
water_change_span = config.get("water_change_span")
empty_level = full_level + water_change_span

levels_boundary = LevelsBoundary(full_level, empty_level)
sanitizer = ReadingsSanitizer(levels_boundary, config.get("accuracy_allowance"))

level_sensor = LevelSensor("level sensor", TimeOfFlightLevelStrategy())
level_detector = LevelDetector("level sensor", level_sensor, levels_boundary, sanitizer,
                               times_to_check_level=config.get("times_to_check_level"),
                               overfill_allowance=config.get("overfill_allowance"))

pump_out_channel = config.get("pump_out_channel")
pump_in_channel = config.get("pump_in_channel")
sump_pump_channel = config.get("sump_pump_channel")

GPIO.setup([pump_out_channel, pump_in_channel, sump_pump_channel], GPIO.OUT)

sump_temp = TemperatureSensor("sump temperature sensor", config.get("sump_temp_device_id"))
tank_temp = TemperatureSensor("tank temperature sensor", config.get("tank_temp_device_id"))
temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp)

pump_out = Switch("pump_out", pump_out_channel, progress_tracker)
pump_in = Switch("pump_in", pump_in_channel, progress_tracker)
sump_pump = Switch("sump pump", sump_pump_channel, progress_tracker)

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts = [f"{current_dir}/temperatureScript_both.py", f"{current_dir}/levelSensorWithTofScript.py"]
controller = Controller(level_detector, temperature_detector,
                        pump_out, pump_in, sump_pump, scripts, configuration_file_path, progress_tracker)

logger.info(f"starting with full sump level: {full_level}, empty sump level: {empty_level}")


def reschedule():
    schedule.clear()
    schedule_updates()
    schedule_water_changes()


def schedule_water_changes():
    water_change_times = Configuration(configuration_file_path).water_change_times()
    progress_tracker.write_ln(
        f"{Style.YELLOW}scheduling water changes for: {Style.BOLD}{Style.WHITE}{water_change_times}")
    for water_change_time in water_change_times:
        schedule.every().day.at(water_change_time).do(controller.water_change).tag("water_change")


def update_and_schedule():
    reschedule()
    controller.update()


def schedule_updates():
    for value in Configuration(configuration_file_path).update_times():
        schedule.every().hour.at(value).do(update_and_schedule).tag("update")


def start():
    schedule_updates()
    schedule_water_changes()
    controller.start()
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    start()
