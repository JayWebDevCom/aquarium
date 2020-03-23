from com.components.Switch import Switch
from com.Controller import Controller
from com.components.LevelDetector import LevelDetector
from components.mocks.MockLevelSensor import MockLevelSensor
from components.mocks.MockSumpTemperatureSensor import MockSumpTemperatureSensor
from components.mocks.MockTankTemperatureSensor import MockTankTemperatureSensor
from com.components.TemperatureDetector import TemperatureDetector


def main():
    mock_level_sensor = MockLevelSensor('mock water sensor')
    water_detector = LevelDetector('water sensor', mock_level_sensor, 20, 60)

    sump_temp = MockSumpTemperatureSensor('mock sump temperature')
    tank_temp = MockTankTemperatureSensor('mock tank temperature')
    temperature_detector = TemperatureDetector("temperature detector", sump_temp, tank_temp, 2.0)

    pump_out = Switch('pump_out', 1)
    pump_in = Switch('pump_in', 2)
    sump_pump = Switch('sump pump', 2)

    controller = Controller("some name", water_detector, temperature_detector, pump_out, pump_in, sump_pump)
    controller.water_change(50.0)


if __name__ == "__main__":
    main()
