from unittest import TestCase

from components.AquariumLevels import AquariumLevels
from components.ReadingsSanitizer import ReadingsSanitizer


class TestReadingsSanitizer(TestCase):
    percentage_boundary = 0.1
    sanitizer = ReadingsSanitizer(AquariumLevels(20, 40), percentage_boundary)

    def test_sanitize_basic(self):
        readings = [30, 30, 30, 30, 30, 30, 30, 30]
        self.assertEqual(30, self.sanitizer.sanitize(readings))

    def test_sanitize(self):
        params = [
            TestReadings(30, [30, 30, 30, 501, 30, 30, 30, 600, 30, 30, 500, 30, 30, 30, 700, 78, 30, 30, 30]),
            TestReadings(31, [0, 0, 0, 0, 1, 1, 1, 1, 3, 4, 5, 20, 30, 40, 34, 66]),
            TestReadings(30, [30, 30, 30, 30, 30, 30, 30, 30, 500, 819, 819]),
            TestReadings(30, [30, 30, 30, 30, 30, 30, 30, 30]),
            TestReadings(35, [28, 39, 40, 34])
        ]

        for reading in params:
            self.assertEqual(reading.expected, self.sanitizer.sanitize(reading.readings))


class TestReadings:
    def __init__(self, expected, readings):
        self.expected = expected
        self.readings = readings
