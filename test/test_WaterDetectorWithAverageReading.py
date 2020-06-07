from unittest import TestCase, mock

from com.components.LevelDetector import LevelDetector
from com.components.LevelSensor import LevelSensor
from components.LevelsBoundary import LevelsBoundary
from components.ReadingsSanitizer import ReadingsSanitizer


class TestWaterLevelDetectorWithAverage(TestCase):
    water_sensor = LevelSensor('water sensor')
    levels_boundary = LevelsBoundary(20, 60)
    sanitizer = ReadingsSanitizer(levels_boundary, 0.1)
    water_detector = LevelDetector('water detector', water_sensor, levels_boundary, sanitizer,
                                   times_to_check_level=5, acceptable_level_band=2)

    @mock.patch("com.components.LevelSensor.LevelSensor.get_level")
    def test_water_level_with_average(self, water_sensor):
        params = {
            25.6: [25, 26, 20, 28, 29],
            30: [25, 26, 30, 31, 38],
            40: [37, 38, 40, 35, 50],
            40.34: [37.12, 38.23, 40.34, 35.45, 50.56]
        }

        for water_level, side_effect in params.items():
            water_sensor.side_effect = side_effect
            self.assertEqual(water_level, self.water_detector._get_checked_sump_level())
