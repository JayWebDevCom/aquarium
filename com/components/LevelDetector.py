from typing import Tuple

from components.LevelsBoundary import LevelsBoundary
from components.LevelSensor import LevelSensor
from components.ReadingsSanitizer import ReadingsSanitizer
from loguru import logger


class UnexpectedWaterLevel(Exception):
    """Raised when the input value is too small or too large"""

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class LevelDetector:

    def __init__(
            self, name: str,
            sensor: LevelSensor,
            levels_boundary: LevelsBoundary,
            sanitizer: ReadingsSanitizer,
            **kwargs):
        self.name = name
        self.sensor = sensor
        self.levels_boundary = levels_boundary
        self.sanitizer = sanitizer
        self.times_to_check_level = range(kwargs.pop("times_to_check_level"))
        self.full_limit = self.levels_boundary.full_level - kwargs.pop("overfill_allowance")
        self.total_level = self.levels_boundary.empty_level - self.levels_boundary.full_level

    def percentage_changed(self) -> float:
        current_level = self._get_checked_sump_level()
        difference = current_level - self.levels_boundary.full_level
        change: float = difference / self.total_level

        return round(change * 100, 2)

    def _check(self, level):
        if level > self.levels_boundary.empty_level or level < self.full_limit:
            logger.error(f"raising UnexpectedWaterLevel: {level}")
            raise UnexpectedWaterLevel(level)
        pass

    def _get_checked_sump_level(self) -> float:
        temperatures_returned = [self.sensor.get_level() for _ in self.times_to_check_level]
        sump_level = self.sanitizer.sanitize(temperatures_returned)
        # logger.info(f"current sump level: {'{:.2f}'.format(sump_level)}")
        self._check(sump_level)
        return sump_level

    def get_sump_state(self) -> Tuple[bool, str]:
        sump_level = self._get_checked_sump_level()
        # logger.info(f"necessary full level is {self.levels_boundary.full_level}, {self.percent_full(sump_level)} full")
        return sump_level <= self.levels_boundary.full_level, self.percent_full(sump_level)

    def percent_full(self, sump_level) -> str:
        difference = sump_level - self.levels_boundary.full_level
        full_span = self.levels_boundary.empty_level - self.levels_boundary.full_level
        percent_full = 100 - (difference / full_span * 100)
        return f"{int(percent_full)}%"
