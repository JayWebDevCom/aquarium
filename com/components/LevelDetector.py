from components.AquariumLevels import AquariumLevels
from components.CustomFormatter import CustomFormatter
from components.LevelSensor import LevelSensor
import logging.config
import yaml

from components.ReadingsSanitizer import ReadingsSanitizer


class UnexpectedWaterLevel(Exception):
    """Raised when the input value is too small or too large"""

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class LevelDetector:

    def __init__(
            self, name: str,
            sensor: LevelSensor,
            aquarium_levels: AquariumLevels,
            sanitizer: ReadingsSanitizer,
            times_to_check_level: int = 5,
            acceptable_band: int = 2):
        self.name = name
        self.sensor = sensor
        self.aquarium_levels = aquarium_levels
        self.sanitizer = sanitizer
        self.times_to_check_level = times_to_check_level
        self.acceptable_band = acceptable_band
        with open('log-config.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            self.logger = logging.getLogger(__name__)
            ch = logging.StreamHandler()
            ch.setFormatter(CustomFormatter())
            self.logger.addHandler(ch)

    def percentage_changed(self) -> float:
        total_level = self.aquarium_levels.empty_level - self.aquarium_levels.full_level
        current_level: int = self._get_checked_sump_level()

        difference = current_level - self.aquarium_levels.full_level
        change: float = difference / total_level
        return change * 100

    def _check(self, level):
        if level not in range(self.aquarium_levels.full_level, self.aquarium_levels.empty_level + 1):
            self.logger.error(f"raising UnexpectedWaterLevel: {level}")
            raise UnexpectedWaterLevel(level)
        pass

    def _get_checked_sump_level(self) -> int:
        sump_level_count_range = range(0, self.times_to_check_level)
        temperatures_returned = []

        for i in sump_level_count_range:
            one_of_temp_readings = self.sensor.get_level()
            temperatures_returned.append(one_of_temp_readings)

        self.logger.info(f"level readings returned: {temperatures_returned}")
        sump_level = self.sanitizer.sanitize(temperatures_returned)
        self._check(sump_level)
        return sump_level

    def is_sump_full(self) -> bool:
        acceptable_range = range(self.aquarium_levels.full_level - self.acceptable_band,
                                 self.aquarium_levels.full_level + self.acceptable_band)
        sump_level = self._get_checked_sump_level()

        self.logger.info(f"sump level is {sump_level}")
        self.logger.info(f"necessary full level is {self.aquarium_levels.full_level}")

        return sump_level in acceptable_range
