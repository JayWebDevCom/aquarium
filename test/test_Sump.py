from unittest import TestCase
from unittest.mock import MagicMock, call

from components.LevelSensor import LevelSensor
from components.LevelsBoundary import LevelsBoundary
from components.ReadingsSanitizer import ReadingsSanitizer
from components.Sump import Sump, UnexpectedWaterLevel


class Helper:
    def __init__(self):
        self.water_sensor = LevelSensor('water sensor')
        self.empty_pump = MagicMock()
        self.refill_pump = MagicMock()
        self.return_pump = MagicMock()
        self.temperature_detector = MagicMock()

    def sump_of(self, levels_boundary, overfill_allowance) -> Sump:
        return Sump(
            self.empty_pump,
            self.refill_pump,
            self.return_pump,
            self.water_sensor,
            self.temperature_detector,
            levels_boundary,
            ReadingsSanitizer(levels_boundary, 0.5),
            times_to_check_level=10,
            overfill_allowance=overfill_allowance
        )


class TestSump(TestCase):

    helper = Helper()
    levels_boundary = LevelsBoundary(20, 60)
    levels_boundary_float_readings = LevelsBoundary(20.5, 60.5)

    sump = helper.sump_of(levels_boundary, 0)
    sump_with_allowance = helper.sump_of(levels_boundary, 1)
    sump_with_float_readings = helper.sump_of(levels_boundary_float_readings, 0)

    def test_calls_to_switches(self):
        self.sump.empty_pump.on()
        self.helper.empty_pump.assert_has_calls([call.on()])

    def test_calls_to_temperature_sensor(self):
        self.sump.temperature_difference()
        self.helper.temperature_detector.assert_has_calls([call.temperature_difference()])

    def test_percentage_changed_parameterized(self):
        params = {30: 25.0, 40: 50.0, 55: 87.5, 34.56: 36.4, 37.43: 43.57}
        for water_level, percentage in params.items():
            self.helper.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(percentage, self.sump.percentage_changed())

    def test_sump_is_full(self):
        params = {20.0: True, 20.1: False, 40: False}
        for water_level, expected in params.items():
            self.helper.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(expected, self.sump.get_state()[0])

    def test_sump_is_full_allowance(self):
        params = {19.0: True, 20.0: True, 20.1: False, 40: False}
        for water_level, expected in params.items():
            self.helper.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(expected, self.sump_with_allowance.get_state()[0])

    def test_unexpected_water_level_error_raised(self):
        too_high = [15, 16, 17, 18, 19, 19.9]
        too_low = [60.1, 62, 63]
        for level in too_high + too_low:
            self.helper.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.sump.get_state()

    def test_unexpected_water_level_error_raised_allowance(self):
        too_high = [15, 16, 17, 18, 18.9]
        too_low = [60.1, 62, 63]
        for level in too_high + too_low:
            self.helper.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.sump_with_allowance.get_state()

    def test_unexpected_water_level_error_raised_with_float_readings(self):
        too_high = [15, 16, 17, 18, 18.9, 19.5, 20.4]
        too_low = [60.6, 61, 62, 63]
        for level in too_high + too_low:
            self.helper.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.sump_with_float_readings.get_state()

    def test_percentage_full(self):
        params = {20: 100, 30.1: 74.75, 40: 50, 60: 0}
        for sump_level, expected in params.items():
            self.assertEqual(expected, self.sump.percent_full(sump_level))
