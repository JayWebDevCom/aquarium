from unittest import TestCase
from unittest.mock import MagicMock

from com.components.LevelDetector import LevelDetector, UnexpectedWaterLevel
from components.LevelsBoundary import LevelsBoundary
from components.LevelSensor import LevelSensor
from components.ReadingsSanitizer import ReadingsSanitizer


class TestWaterLevelDetector(TestCase):
    water_sensor = LevelSensor('water sensor')
    levels_boundary = LevelsBoundary(20, 60)
    levels_boundary_float_readings = LevelsBoundary(20.5, 60.5)
    sanitizer = ReadingsSanitizer(levels_boundary, 0.5)

    level_detector = LevelDetector('level detector [allowance 0]', water_sensor, levels_boundary, sanitizer,
                                   times_to_check_level=10, overfill_allowance=0)

    level_detector_with_allowance = LevelDetector('level detector [allowance 1]', water_sensor, levels_boundary,
                                                  sanitizer, times_to_check_level=10, overfill_allowance=1)

    level_detector_with_float_readings = LevelDetector('level detector [allowance 0]', water_sensor,
                                                       levels_boundary_float_readings,
                                                       sanitizer, times_to_check_level=10, overfill_allowance=0)

    def _level_detector(self, name, overfill_allowance) -> LevelDetector:
        return LevelDetector(name, self.water_sensor, self.levels_boundary, self.sanitizer,
                             times_to_check_level=10, overfill_allowance=overfill_allowance)

    def test_percentage_changed_parameterized(self):
        params = {30: 25.0, 40: 50.0, 55: 87.5, 34.56: 36.4, 37.43: 43.57}
        for water_level, percentage in params.items():
            self.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(percentage, self.level_detector.percentage_changed())

    def test_sump_is_full(self):
        params = {20.0: (True, '100%'), 20.1: (False, '99%'), 40: (False, '50%')}
        for water_level, expected in params.items():
            self.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(expected, self.level_detector.get_sump_state())

    def test_sump_is_full_allowance(self):
        params = {19.0: (True, '102%'), 20.0: (True, '100%'), 20.1: (False, '99%'), 40: (False, '50%')}
        for water_level, expected in params.items():
            self.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(expected, self.level_detector_with_allowance.get_sump_state())

    def test_sump_is_full_float_readings(self):
        params = {20.5: (True, '100%'), 20.6: (False, '99%'), 40: (False, '51%')}
        for water_level, expected in params.items():
            self.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(expected, self.level_detector_with_float_readings.get_sump_state())

    def test_unexpected_water_level_error_raised(self):
        too_high = [15, 16, 17, 18, 19, 19.9]
        too_low = [60.1, 62, 63]
        for level in too_high + too_low:
            self.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.level_detector.get_sump_state()

    def test_unexpected_water_level_error_raised_allowance(self):
        too_high = [15, 16, 17, 18, 18.9]
        too_low = [60.1, 62, 63]
        for level in too_high + too_low:
            self.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.level_detector_with_allowance.get_sump_state()

    def test_unexpected_water_level_error_raised_with_float_readings(self):
        too_high = [15, 16, 17, 18, 18.9, 19.5, 20.4]
        too_low = [60.6, 61, 62, 63]
        for level in too_high + too_low:
            self.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.level_detector_with_float_readings.get_sump_state()

    def test_percentage_full(self):
        params = {20: "100%", 40: "50%", 60: "0%"}
        for sump_level, expected in params.items():
            self.assertEqual(expected, self.level_detector.percent_full(sump_level))
