from components import TemperatureSensor
from loguru import logger


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
        sump_temp = self.sump_temp.get_temp()
        tank_temp = self.tank_temp.get_temp()
        temp_difference = abs(sump_temp - tank_temp)

        logger.info(f"temp difference: {'{:.2f}'.format(temp_difference)}, "
                    f"sump: {sump_temp}, tank: {tank_temp}")
        return temp_difference <= self.limit
