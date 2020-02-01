from components import TemperatureSensor


class TemperatureDetector:
    """A simple TemperatureDetector class"""
    name: str
    sump_temp: TemperatureSensor
    tank_temp: TemperatureSensor
    limit: float

    def __init__(
            self, name: str,
            sump_temp: TemperatureSensor,
            tank_temp: TemperatureSensor,
            temperature_difference_limit: float = 2.0):
        self.name = name
        self.sump_temp = sump_temp
        self.tank_temp = tank_temp
        self.limit = temperature_difference_limit

    def within_range(self) -> bool:
        temp_difference = self.sump_temp.get_temp() - self.tank_temp.get_temp()
        return abs(temp_difference) <= self.limit
