import os

import RPi.GPIO as GPIO

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
config_file = "config.yaml"
c_file = f"{current_dir}/{config_file}"
config = Configuration(c_file)

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

pump_out = Switch("pump_out", pump_out_channel, Style.LIGHT_RED, progress_tracker)
pump_in = Switch("pump_in", pump_in_channel, Style.LIGHT_RED, progress_tracker)
sump_pump = Switch("sump pump", sump_pump_channel, Style.LIGHT_RED, progress_tracker)

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts = [f"{current_dir}/temperatureScript_both.py", f"{current_dir}/levelSensorWithTofScript.py"]
controller = Controller(level_detector, temperature_detector,
                        pump_out, pump_in, sump_pump, scripts, c_file,
                        Style.YELLOW, progress_tracker)

logger.info(f"starting with full sump level: {full_level}, empty sump level: {empty_level}")
controller.start()
