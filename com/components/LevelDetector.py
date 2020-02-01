__package__ = "components"

from components import LevelSensor


class UnexpectedWaterLevel(Exception):
    """Raised when the input value is too small or too large"""

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class LevelDetector:

    def __init__(self, name: str, sensor: LevelSensor, full_level: int, empty_level: int):
        self.name = name
        self.sensor = sensor
        self.full_level = full_level
        self.empty_level = empty_level

    def percentage_changed(self) -> float:
        total_level = self.empty_level - self.full_level

        current_level: int = self.sensor.get_level()
        self.check(int(current_level))

        difference = current_level - self.full_level
        change: float = difference / total_level
        return change * 100

    def check(self, level):
        if level not in range(self.full_level, self.empty_level):
            raise UnexpectedWaterLevel(level)
        pass
