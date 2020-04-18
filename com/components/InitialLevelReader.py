import time

from components.LevelStrategy import LevelStrategy
from components.ReadingsSanitizer import ReadingsSanitizer


class InitialLevelReader:

    def __init__(self, sensor: LevelStrategy, sanitizer: ReadingsSanitizer, num_readings: int = 10):
        self.sensor = sensor
        self.sanitizer = sanitizer
        self.range_of_readings_to_take = range(0, num_readings)

    def get_initial_level(self):
        readings_list = []

        for _ in self.range_of_readings_to_take:
            reading = self.sensor.get_level()
            readings_list.append(reading)
            time.sleep(0.2)

        return self.sanitizer.sanitize(readings_list)
