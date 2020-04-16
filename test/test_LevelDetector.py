from unittest import TestCase
from unittest.mock import MagicMock

from com.components.LevelDetector import LevelDetector, UnexpectedWaterLevel
from components.AquariumLevels import AquariumLevels
from components.LevelSensor import LevelSensor
from components.ReadingsSanitizer import ReadingsSanitizer


class TestWaterLevelDetector(TestCase):
    water_sensor = LevelSensor('water sensor')
    aquarium_levels = AquariumLevels(20, 60)
    sanitizer = ReadingsSanitizer(aquarium_levels, 0.1)
    water_detector = LevelDetector('water detector', water_sensor, aquarium_levels, sanitizer, 1, 2)

    def test_percentage_changed_parameterized(self):
        params = {30: 25.0, 40: 50.0, 55: 87.5}
        for water_level, percentage in params.items():
            self.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(percentage, self.water_detector.percentage_changed())

    def test_sump_is_full(self):
        params = {20: True, 21: True, 22: False, 40: False, 50: False, 59: False}
        for water_level, expected in params.items():
            self.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(expected, self.water_detector.is_sump_full())

    def test_unexpected_water_level_error_raised(self):
        too_high = [18, 19]
        too_low = [62, 63]
        for level in too_high + too_low:
            self.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.water_detector.is_sump_full()
