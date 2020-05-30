from unittest import TestCase

from components.LevelsBoundary import LevelsBoundary
from components.ReadingsSanitizer import ReadingsSanitizer


class TestReadingsSanitizer(TestCase):
    percentage_boundary = 0.1
    sanitizer = ReadingsSanitizer(LevelsBoundary(20.1, 40.7), percentage_boundary)

    def test_sanitize_basic(self):
        readings = [30, 30, 30, 30, 30, 30, 30, 30]
        self.assertEqual(30, self.sanitizer.sanitize(readings))

    def test_sanitize_int(self):
        params = [
            TestReadings(30, [30, 30, 30, 501, 30, 30, 30, 600, 30, 30, 500, 30, 30, 30, 700, 78, 30, 30, 30]),
            TestReadings(31, [0, 0, 0, 0, 1, 1, 1, 1, 3, 4, 5, 20, 30, 40, 34, 66]),
            TestReadings(30, [30, 30, 30, 30, 30, 30, 30, 30, 500, 819, 819]),
            TestReadings(30, [30, 30, 30, 30, 30, 30, 30, 30]),
            TestReadings(35, [28, 39, 40, 34])
        ]

        for reading in params:
            self.assertEqual(reading.expected, self.sanitizer.sanitize(reading.readings))

    def test_sanitize_float(self):
        params = [
            TestReadings(30, [30.0, 30.1, 30.2, 30.3, 30.4, 30.5, 30.6]),
            TestReadings(31, [30.4, 30.5, 30.6, 30.7, 30.8]),
            TestReadings(31, [30.4, 30.5, 30.6, 30.7, 30.8, 45.76]),
        ]

        for reading in params:
            self.assertEqual(reading.expected, self.sanitizer.sanitize(reading.readings))


class TestReadings:
    def __init__(self, expected, readings):
        self.expected = expected
        self.readings = readings
