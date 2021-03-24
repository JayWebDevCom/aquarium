from typing import List
from unittest import TestCase
from unittest.mock import MagicMock

from numpy import average

from com.components.TemperatureDetector import TemperatureDetector
from com.components.TemperatureSensor import TemperatureSensor


class TestTemperatureDetector(TestCase):

    def test_within_range(self):
        sump_temp = TemperatureSensor("sump", "foo")
        tank_temp = TemperatureSensor("tank", "bar")
        temperature_detector = TemperatureDetector("test temperature detector", sump_temp, tank_temp)

        params = {
            TestTemperatures([30.0], [25.0]): 5.0,
            TestTemperatures([40.0], [50.0]): 10.0,
            TestTemperatures([51.0], [87.5]): 36.5,
            TestTemperatures([28.0], [30.1]): 2.1,
            TestTemperatures([0], [0]): 0,
            TestTemperatures([0], [1]): 1,
            TestTemperatures([1], [1]): 0,
            TestTemperatures([26.0], [28.0]): 2.0,
            TestTemperatures([26.34345], [28.45]): 2.11
        }

        for temps, result in params.items():
            sump_temp.get_temp = MagicMock(return_value=average(temps.sump))
            tank_temp.get_temp = MagicMock(return_value=average(temps.tank))

            self.assertEqual(result, temperature_detector.temperature_difference())

    def test_breakdown(self):
        sump_temp = TemperatureSensor("sump", "foo")
        tank_temp = TemperatureSensor("tank", "bar")
        temperature_detector = TemperatureDetector("test temperature detector", sump_temp, tank_temp)

        params = {
            TestTemperatures([30.0], [25.0]): ([30.0], [25.0], 5.0),
            TestTemperatures([40.0], [50.0]): ([40.0], [50.0], 10.0),
            TestTemperatures([51.0], [87.5]): ([51.0], [87.5], 36.5),
            TestTemperatures([28.0], [30.1]): ([28.0], [30.1], 2.1),
            TestTemperatures([0], [0]): ([0], [0], 0),
            TestTemperatures([0], [1]): ([0], [1], 1),
            TestTemperatures([1], [1]): ([1], [1], 0),
            TestTemperatures([26.0], [28.0]): ([26.0], [28.0], 2.0),
            TestTemperatures([26.34345], [28.45]): ([26.34345], [28.45], 2.11),
            TestTemperatures([26.34345, 28.4567], [28.45, 24.765]): ([27.400075], [26.6075], 0.79)
        }

        for temps, result in params.items():
            sump_temp.get_temp = MagicMock(return_value=average(temps.sump))
            tank_temp.get_temp = MagicMock(return_value=average(temps.tank))

            self.assertEqual(result, temperature_detector.temperature_breakdown())


class TestTemperatures:
    sump: List[float]
    tank: List[float]

    def __init__(self, sump: List[float], tank: List[float]):
        self.sump = sump
        self.tank = tank

