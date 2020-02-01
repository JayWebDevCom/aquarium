from Controller import Controller
from components.LevelDetector import LevelDetector
from components.LevelSensor import LevelSensor
from components.Switch import Switch
from components.TemperatureDetector import TemperatureDetector
from components.mocks.MockSumpTemperatureSensor import MockSumpTemperatureSensor
from components.mocks.MockTankTemperatureSensor import MockTankTemperatureSensor

water_sensor = LevelSensor('water sensor')
water_detector = LevelDetector('water sensor', water_sensor, 20, 60)

sump_temp = MockSumpTemperatureSensor('mock sump temperature')
tank_temp = MockTankTemperatureSensor('mock tank temperature')
temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp, 2.0)

pump_out = Switch('pump_out', 1)
pump_in = Switch('pump_in', 2)

controller = Controller("some name", water_detector, temperature_detector, pump_out, pump_in)
controller.water_change(50.0)
