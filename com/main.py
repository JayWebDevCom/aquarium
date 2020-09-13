import os
import time

import RPi.GPIO as GPIO
import schedule

from AquariumLogger import AquariumLogger
from Configuration import Configuration
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

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = "config.yaml"
cfile = f"{current_dir}/{config_file}"
config = Configuration(cfile)
data = config.data()

full_level = data['full_level']
water_change_span = data['water_change_span']
empty_level = full_level + water_change_span

logger.info(f"starting with full sump level: {full_level}, empty sump level: {empty_level}")

levels_boundary = LevelsBoundary(full_level, empty_level)
sanitizer = ReadingsSanitizer(levels_boundary, data['accuracy_allowance'])

level_sensor = LevelSensor('level sensor', TimeOfFlightLevelStrategy())
level_detector = LevelDetector('level sensor', level_sensor, levels_boundary, sanitizer,
                               times_to_check_level=data['times_to_check_level'], 
                               overfill_allowance=data['overfill_allowance'])

pump_out_channel = data['pump_out_channel']
pump_in_channel = data['pump_in_channel']
sump_pump_channel = data['sump_pump_channel']

GPIO.setup([pump_out_channel, pump_in_channel, sump_pump_channel], GPIO.OUT)

sump_temp = TemperatureSensor("sump temperature sensor", data['sump_temp_device_id'])
tank_temp = TemperatureSensor("tank temperature sensor", data['tank_temp_device_id'])
temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp)

pump_out = Switch('pump_out', pump_out_channel)
pump_in = Switch('pump_in', pump_in_channel)
sump_pump = Switch('sump pump', sump_pump_channel)

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts = [f"{current_dir}/temperatureScript_both.py", f"{current_dir}/levelSensorWithTofScript.py"]
controller = Controller("Aquarium Controller", level_detector, temperature_detector,
                        pump_out, pump_in, sump_pump, scripts,
                        level_check_interval=data['level_check_interval'], 
                        temp_check_interval=data['temp_check_interval'], 
                        temperature_difference_limit=data['temperature_difference_limit'])

sump_pump.on()

def updates():
    schedule.clear("update")
    schedule.clear("water_change")
    controller.update()
    schedule_updates()
    schedule_water_changes()

def schedule_updates():
    config = Configuration(cfile)
    for minutes in config.update_times():
        schedule.every().hour.at(minutes).do(updates).tag("update")

def schedule_water_changes():
    config = Configuration(cfile)
    logger.info(f"scheduling water changes for: {config.water_change_times()}")
    for minutes in config.water_change_times():
        schedule.every().day.at(minutes).do(water_change).tag("water_change")

def water_change():
    config = Configuration(cfile)
    schedule.clear("update")
    logger.info("")
    logger.info("Water change beginning...")
    controller.water_change(config.get('water_change_level'))
    schedule_updates()

schedule_updates()
schedule_water_changes()

while True:
    schedule.run_pending()
    time.sleep(1)

