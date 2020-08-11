import os
import time

import RPi.GPIO as GPIO
import schedule

from AquariumLogger import AquariumLogger
from Controller import Controller
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

full_level = 17
water_change_span = 15
accuracy_allowance = 0.1
times_to_check_level = 9
empty_level = full_level + water_change_span

logger.info(f"starting with full sump level: {full_level}, empty sump level: {empty_level}")

levels_boundary = LevelsBoundary(full_level, empty_level)
sanitizer = ReadingsSanitizer(levels_boundary, accuracy_allowance)

level_sensor = LevelSensor('level sensor', TimeOfFlightLevelStrategy())
level_detector = LevelDetector('level sensor', level_sensor, levels_boundary, sanitizer,
                               times_to_check_level=times_to_check_level, overfill_allowance=2)
sump_temp_device_id = "28-0300a2792070"
tank_temp_device_id = "28-0300a279088e"

pump_out_channel = 27
pump_in_channel = 23
sump_pump_channel = 17

GPIO.setup([pump_out_channel, pump_in_channel, sump_pump_channel], GPIO.OUT)

sump_temp = TemperatureSensor("sump temperature sensor", sump_temp_device_id)
tank_temp = TemperatureSensor("tank temperature sensor", tank_temp_device_id)
temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp)

pump_out = Switch('pump_out', pump_out_channel)
pump_in = Switch('pump_in', pump_in_channel)
sump_pump = Switch('sump pump', sump_pump_channel)

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts = [current_dir / "temperatureScript_both.py", current_dir / "levelSensorWithTofScript.py"]

controller = Controller("Aquarium Controller", level_detector, temperature_detector,
                        pump_out, pump_in, sump_pump, scripts,
                        level_check_interval=3, temp_check_interval=3, temperature_difference_limit=4.0)


def update():
    controller.update()


for minutes in [":00", ":15", ":30", ":45"]:
    schedule.every().hour.at(minutes).do(update).tag("aquarium")


def water_change():
    logger.info("Water change beginning...")
    controller.water_change(50.0)


schedule.every().day.at("20:00").do(water_change).tag("aquarium")

while True:
    schedule.run_pending()
    time.sleep(1)
