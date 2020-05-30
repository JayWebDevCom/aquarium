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
        self.times_to_check_level = kwargs.pop("times_to_check_level")
        acceptable_temp_band = kwargs.pop("acceptable_temp_band")
        self.upper_limit = self.levels_boundary.full_level - acceptable_temp_band
        self.lower_limit = self.levels_boundary.full_level + acceptable_temp_band

    def percentage_changed(self) -> float:
        total_level = self.levels_boundary.empty_level - self.levels_boundary.full_level
        current_level: int = self._get_checked_sump_level()

        difference = current_level - self.levels_boundary.full_level
        change: float = difference / total_level
        return change * 100

    def _check(self, level):
        grace = 1
        if level > self.levels_boundary.empty_level or level <= self.levels_boundary.full_level - grace:
            logger.error(f"raising UnexpectedWaterLevel: {level}")
            raise UnexpectedWaterLevel(level)
        pass

    def _get_checked_sump_level(self) -> int:
        sump_level_count_range = range(0, self.times_to_check_level)
        temperatures_returned = []

        for _ in sump_level_count_range:
            one_of_temp_readings = self.sensor.get_level()
            temperatures_returned.append(one_of_temp_readings)

        logger.info(f"level readings returned: {temperatures_returned}")
        sump_level = self.sanitizer.sanitize(temperatures_returned)
        self._check(sump_level)
        return sump_level

    def is_sump_full(self) -> bool:
        sump_level = self._get_checked_sump_level()

        logger.info(f"sump level is {sump_level}")
        logger.info(f"necessary full level is {self.levels_boundary.full_level}")

        return self.upper_limit < sump_level < self.lower_limit
