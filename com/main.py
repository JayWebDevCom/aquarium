from AquariumLogger import AquariumLogger
from Controller import Controller
from components.AquariumLevels import AquariumLevels
from components.LevelDetector import LevelDetector
from components.LevelSensor import LevelSensor
from components.ReadingsSanitizer import ReadingsSanitizer
from components.TemperatureSensor import TemperatureSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy
from components.Switch import Switch
from components.TemperatureDetector import TemperatureDetector
import RPi.GPIO as GPIO
import time
import schedule

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = AquariumLogger()

full_level = 27
empty_level = 27+15

aquarium_levels = AquariumLevels(full_level, empty_level)
sanitizer = ReadingsSanitizer(aquarium_levels, 0.1)

water_sensor = LevelSensor('water sensor', TimeOfFlightLevelStrategy())
water_detector = LevelDetector('water sensor', water_sensor, aquarium_levels, sanitizer, 5)

sump_temp_device_id = "28-0300a2792070"
tank_temp_device_id = "28-0300a279088e"

pump_out_channel = 27
pump_in_channel = 23
sump_pump_channel = 17

GPIO.setup([pump_out_channel, pump_in_channel, sump_pump_channel], GPIO.OUT)

sump_temp = TemperatureSensor("sump temperature sensor", sump_temp_device_id)
tank_temp = TemperatureSensor("tank temperature sensor", tank_temp_device_id)
temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp, 1.0)

pump_out = Switch('pump_out', pump_out_channel)
pump_in = Switch('pump_in', pump_in_channel)
sump_pump = Switch('sump pump', sump_pump_channel)

controller = Controller("some name", water_detector, temperature_detector, pump_out, pump_in, sump_pump)


def job():
    logger.info("Water change beginning...")
    controller.water_change(50.0)


schedule.every().day.at("20:00").do(job).tag("aquarium")

while True:
    schedule.run_pending()
    time.sleep(1)
