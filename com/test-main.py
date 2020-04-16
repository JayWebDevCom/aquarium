from AquariumLogger import AquariumLogger
from Controller import Controller
from components.LevelDetector import LevelDetector
from components.LevelSensor import LevelSensor
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

water_sensor = LevelSensor('water sensor', TimeOfFlightLevelStrategy())
water_detector = LevelDetector('water sensor', water_sensor, 22, 22+15, 10)

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

#controller.water_change(10.0)

