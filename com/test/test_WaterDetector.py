from unittest import TestCase
from unittest.mock import MagicMock

from com.components.LevelSensor import LevelSensor
from com.components.LevelDetector import LevelDetector, UnexpectedWaterLevel


class TestWaterLevelDetector(TestCase):

    water_sensor = LevelSensor('water sensor')
    water_detector = LevelDetector('water detector', water_sensor, 20, 60)

    def test_percentage_changed_parameterized(self):
        params = {30: 25.0, 40: 50.0, 55: 87.5}
        for water_level, percentage in params.items():
            self.water_sensor.get_level = MagicMock(return_value=water_level)
            self.assertEqual(percentage, self.water_detector.percentage_changed())

    def test_unexpected_water_level(self):
        for level in [0, 1, 19, 61, 100]:
            self.water_sensor.get_level = MagicMock(return_value=level)
            with self.assertRaises(UnexpectedWaterLevel):
                self.water_detector.percentage_changed()




