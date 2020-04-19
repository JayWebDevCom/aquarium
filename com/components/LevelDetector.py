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
            times_to_check_level: int = 5,
            acceptable_band: int = 2):
        self.name = name
        self.sensor = sensor
        self.aquarium_levels = levels_boundary
        self.sanitizer = sanitizer
        self.times_to_check_level = times_to_check_level
        self.acceptable_band = acceptable_band

    def percentage_changed(self) -> float:
        total_level = self.aquarium_levels.empty_level - self.aquarium_levels.full_level
        current_level: int = self._get_checked_sump_level()

        difference = current_level - self.aquarium_levels.full_level
        change: float = difference / total_level
        return change * 100

    def _check(self, level):
        if level not in range(self.aquarium_levels.full_level, self.aquarium_levels.empty_level + 1):
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
        acceptable_range = range(self.aquarium_levels.full_level - self.acceptable_band,
                                 self.aquarium_levels.full_level + self.acceptable_band)
        sump_level = self._get_checked_sump_level()

        logger.info(f"sump level is {sump_level}")
        logger.info(f"necessary full level is {self.aquarium_levels.full_level}")

        return sump_level in acceptable_range
