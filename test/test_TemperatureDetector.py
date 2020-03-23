from unittest import TestCase
from unittest.mock import MagicMock

from com.components.TemperatureDetector import TemperatureDetector
from com.components.TemperatureSensor import TemperatureSensor


class TestTemperatureDetector(TestCase):

    def test_within_range(self):
        sump_temp = TemperatureSensor("sump", "foo")
        tank_temp = TemperatureSensor("tank", "bar")
        temperature_detector = TemperatureDetector("test temperature detector", sump_temp, tank_temp)

        params = {
            TestTemperatures(30.0, 25.0): False,
            TestTemperatures(40.0, 50.0): False,
            TestTemperatures(51.0, 87.5): False,
            TestTemperatures(28.0, 30.1): False,
            TestTemperatures(0, 0): True,
            TestTemperatures(0, 1): True,
            TestTemperatures(1, 1): True,
            TestTemperatures(26.0, 28.0): True
        }

        for temps, result in params.items():
            sump_temp.get_temp = MagicMock(return_value=temps.sump)
            tank_temp.get_temp = MagicMock(return_value=temps.tank)

            self.assertEqual(result, temperature_detector.within_range())


class TestTemperatures:
    sump: float
    tank: float

    def __init__(self, sump, tank):
        self.sump = sump
        self.tank = tank
