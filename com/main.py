import os
import time

import atexit
import RPi.GPIO as GPIO
import signal
import schedule

from AquariumLogger import AquariumLogger
from Configuration import Configuration
from Controller import Controller
from Progress import ProgressTracker, Style
from components.LevelSensor import LevelSensor
from components.LevelsBoundary import LevelsBoundary
from components.ReadingsSanitizer import ReadingsSanitizer
from components.Sump import Sump
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

empty_channel = config.get("pump_out_channel")
refill_channel = config.get("pump_in_channel")
return_channel = config.get("sump_pump_channel")

GPIO.setup([empty_channel, refill_channel, return_channel], GPIO.OUT)

sump_temp = TemperatureSensor("sump temperature sensor", config.get("sump_temp_device_id"))
tank_temp = TemperatureSensor("tank temperature sensor", config.get("tank_temp_device_id"))
temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp,
                                           config.get("times_to_check_temp"))

empty_pump = Switch("empty", empty_channel, progress_tracker)
refill_pump = Switch("refill", refill_channel, progress_tracker)
return_pump = Switch("return", return_channel, progress_tracker)

sump = Sump(empty_pump, refill_pump, return_pump,
            level_sensor, temperature_detector, levels_boundary, sanitizer,
            times_to_check_level=config.get("times_to_check_level"),
            overfill_allowance=config.get("overfill_allowance"))

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts = [f"{current_dir}/temperatureScript_both.py", f"{current_dir}/levelSensorWithTofScript.py"]
controller = Controller(sump, scripts, config, progress_tracker)

logger.info(f"starting with full sump level: {full_level}, empty sump level: {empty_level}")


def schedule_updates():
    for value in Configuration(configuration_file_path).update_times():
        schedule.every().hour.at(value).do(clear_and_schedule).tag("update")


def clear_and_schedule():
    schedule.clear()
    controller.update()
    schedule_updates()
    schedule_water_changes()


def clear_and_water_change():
    schedule.clear("update")
    controller.water_change()
    schedule_updates()


def schedule_water_changes():
    water_change_times = Configuration(configuration_file_path).water_change_times()
    progress_tracker.write_ln(
        f"{Style.YELLOW}scheduling water changes for: {Style.BOLD}{Style.WHITE}{water_change_times}")
    for water_change_time in water_change_times:
        schedule.every().day.at(water_change_time).do(clear_and_water_change).tag("water_change")


def start():
    schedule_updates()
    schedule_water_changes()
    controller.start()
    while True:
        schedule.run_pending()
        time.sleep(1)


def handle_exit(*args):
    empty_pump.off()
    refill_pump.off()
    return_pump.off()


atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)


if __name__ == '__main__':
    start()

