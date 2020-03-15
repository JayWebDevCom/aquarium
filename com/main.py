from Controller import Controller
from components.LevelDetector import LevelDetector
from components.mocks.MockLevelSensor import MockLevelSensor
from components.Switch import Switch
from components.TemperatureDetector import TemperatureDetector
from components.mocks.MockSumpTemperatureSensor import MockSumpTemperatureSensor
from components.mocks.MockTankTemperatureSensor import MockTankTemperatureSensor
import time
import schedule

water_sensor = MockLevelSensor('water sensor')
water_detector = LevelDetector('water sensor', water_sensor, 20, 60)

sump_temp = MockSumpTemperatureSensor('mock sump temperature')
tank_temp = MockTankTemperatureSensor('mock tank temperature')
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
