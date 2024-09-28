from typing import Tuple

from components.LevelsBoundary import LevelsBoundary
from components.LevelSensor import LevelSensor
from components.ReadingsSanitizer import ReadingsSanitizer


class UnexpectedWaterLevel(Exception):
    """Raised when the input value is too small or too large"""

    def __init__(self, message):
        super().__init__(message)


class Sump:

    def __init__(
            self,
            empty_pump,
            refill_pump,
            return_pump,
            sensor: LevelSensor,
            temperature_detector,
            levels_boundary: LevelsBoundary,
            sanitizer: ReadingsSanitizer,
            **kwargs):
        self.empty_pump = empty_pump
        self.refill_pump = refill_pump
        self.return_pump = return_pump
        self.sensor = sensor
        self.temperature_detector = temperature_detector
        self.levels_boundary = levels_boundary
        self.sanitizer = sanitizer
        self.times_to_check_level = range(kwargs.pop("times_to_check_level"))
        self.full_limit = self.levels_boundary.full_level - kwargs.pop("overfill_allowance")
        self.total_level = self.levels_boundary.empty_level - self.levels_boundary.full_level

    def percentage_changed(self) -> float:
        current_level = self._get_checked_level()
        difference = current_level - self.levels_boundary.full_level
        change: float = difference / self.total_level

        return round(change * 100, 2)

    def _check(self, level):
        if level > self.levels_boundary.empty_level or level < self.full_limit:
            message = f"level: {level}, {self.percent_full(level)}% full"
            raise UnexpectedWaterLevel(message)
        pass

    def _get_checked_level(self) -> float:
        sump_levels = [self.sensor.get_level() for _ in self.times_to_check_level]
        sump_level = self.sanitizer.sanitize(sump_levels)
        self._check(sump_level)
        return sump_level

    def get_state(self) -> Tuple[bool, float]:
        sump_level = self._get_checked_level()
        return sump_level <= self.levels_boundary.full_level, self.percent_full(sump_level)

    def percent_full(self, sump_level) -> float:
        difference = sump_level - self.levels_boundary.full_level
        full_span = self.levels_boundary.empty_level - self.levels_boundary.full_level
        percent_full = 100 - (difference / full_span) * 100
        return round(float(percent_full), 2)

    def temperature_difference(self) -> float:
        return self.temperature_detector.temperature_difference()

    def temperature_breakdown(self) -> Tuple[float, float, float]:
        return self.temperature_detector.temperature_breakdown()

    def get_full_limit(self) -> float:
        overfill_delta = self.levels_boundary.full_level - self.full_limit
        overfill_height = overfill_delta + self.levels_boundary.full_level
        percentage_full_limit = overfill_height / self.levels_boundary.full_level * 100
        return round(float(percentage_full_limit), 2)
