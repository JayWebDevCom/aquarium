from Controller import Controller
from components.LevelDetector import LevelDetector
from components.LevelSensor import LevelSensor
from components.TemperatureSensor import TemperatureSensor
from components.TimeOfFlightLevelStrategy import TimeOfFlightLevelStrategy
from components.Switch import Switch
from components.TemperatureDetector import TemperatureDetector
import time
import schedule

water_sensor = LevelSensor('water sensor', TimeOfFlightLevelStrategy())
water_detector = LevelDetector('water sensor', water_sensor, 20, 60, 2)

sump_temp_device_id = "28-0300a279088e"
tank_temp_device_id = "28-0300a2792070"

sump_temp = TemperatureSensor("sump temperature sensor", sump_temp_device_id)
tank_temp = TemperatureSensor("tank temperature sensor", tank_temp_device_id)
temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp, 1.0)

pump_out = Switch('pump_out', 1)
pump_in = Switch('pump_in', 2)
sump_pump = Switch('sump pump', 2)

controller = Controller("some name", water_detector, temperature_detector, pump_out, pump_in, sump_pump)


def job():
    print("Water change beginning...")
    controller.water_change(50.0)


schedule.every().day.at("20:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
