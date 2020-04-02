from unittest import TestCase

from components.LevelSensor import LevelSensor
from components.LevelStrategy import LevelStrategy, IllegalArgumentError


class TestLevelSensor(TestCase):
    level_sensor = LevelSensor('water sensor', LevelStrategy("should throw"))

    def test_unexpected_water_level_error_raised(self):
        with self.assertRaises(IllegalArgumentError):
            self.level_sensor.get_level()
