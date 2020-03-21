__package__ = "components"

from components.LevelSensor import LevelSensor


class UnexpectedWaterLevel(Exception):
    """Raised when the input value is too small or too large"""

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class LevelDetector:

    def __init__(
            self, name: str,
            sensor: LevelSensor,
            full_level: int,
            empty_level: int,
            times_to_check_level: int = 5):
        self.name = name
        self.sensor = sensor
        self.full_level = full_level
        self.empty_level = empty_level
        self.times_to_check_level = times_to_check_level

    def percentage_changed(self) -> float:
        total_level = self.empty_level - self.full_level

        current_level: int = self._get_checked_sump_level()
        self._check(int(current_level))

        difference = current_level - self.full_level
        change: float = difference / total_level
        return change * 100

    def _check(self, level):
        if level not in range(self.full_level, self.empty_level):
            print(f"raising UnexpectedWaterLevel: {level}")
            raise UnexpectedWaterLevel(level)
        pass

    def _get_checked_sump_level(self) -> int:
        sump_level = 0
        sump_level_count_range = range(0, self.times_to_check_level)

        for i in sump_level_count_range:
            sump_level += self.sensor.get_level()

        sump_level = int(sump_level/len(sump_level_count_range))
        self._check(sump_level)
        return sump_level

    def is_sump_full(self) -> bool:
        acceptable_band = 2
        acceptable_range = range(self.full_level - acceptable_band, self.full_level + acceptable_band)
        sump_level = self._get_checked_sump_level()
        print(f"sump level is {sump_level}")
        print(f"necessary full level is {self.full_level}")
        return sump_level in acceptable_range
