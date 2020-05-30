from AquariumLogger import AquariumLogger
from Controller import Controller
from components.InitialLevelReader import InitialLevelReader
from components.LevelsBoundary import LevelsBoundary
from components.LevelDetector import LevelDetector
from components.LevelSensor import LevelSensor
from components.ReadingsSanitizer import ReadingsSanitizer
from components.TemperatureSensor import TemperatureSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy
from components.Switch import Switch
from components.TemperatureDetector import TemperatureDetector
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

logger = AquariumLogger()

sensor = TimeOfFlightLevelStrategy()

initial_levels_boundary = LevelsBoundary(14, 20)
initial_level_sanitizer = ReadingsSanitizer(initial_levels_boundary, 0.1)
initial_level_reader = InitialLevelReader(sensor, initial_level_sanitizer)


full_level = initial_level_reader.get_initial_level()
logger.info(f"starting with a full sump level of {full_level}")

water_change_range = 25
empty_level = full_level + water_change_range

levels_boundary = LevelsBoundary(full_level, empty_level)
sanitizer = ReadingsSanitizer(levels_boundary, 0.1)

water_sensor = LevelSensor('water sensor', sensor)
water_detector = LevelDetector('water sensor', water_sensor, levels_boundary, sanitizer,
                               times_to_check_level=10, acceptable_temp_band=1)

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

# controller.water_change(10.0)
