from functools import reduce
from typing import Tuple, List

from loguru import logger

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
            num_readings: int = 1,
            num_sensor_readings: int = 5):
        self.name = name
        self.sump_temp = sump_temp
        self.tank_temp = tank_temp
        self.num_readings = num_readings
        self.num_sensor_readings = num_sensor_readings

    def temperature_breakdown(self) -> Tuple[List[int], List[int], float]:
        sump_temps = [self._get_temp(self.sump_temp) for _ in range(self.num_readings)]
        tank_temps = [self._get_temp(self.tank_temp) for _ in range(self.num_readings)]

        ave_sump_temp = reduce(lambda a, b: a + b, sump_temps) / self.num_readings
        ave_tank_temp = reduce(lambda a, b: a + b, tank_temps) / self.num_readings
        temp_difference = abs(ave_sump_temp - ave_tank_temp)

        return sump_temps, tank_temps, round(temp_difference, 2)

    def temperature_difference(self) -> float:
        return self.temperature_breakdown()[2]

    def get_temp(self, sensor: TemperatureSensor):
        attempt = 1
        while attempt <= self.num_sensor_readings:
            try:
                return sensor.get_temp()
            except IndexError as _:
                logger.error(f"Unable to get temp from {sensor.name} at attempt {attempt}")
                attempt += 1
                pass
        raise IndexError(f"Couldn't get reading from {sensor.name}")
