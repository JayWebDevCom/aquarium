from components import TemperatureSensor
from components.CustomFormatter import CustomFormatter
import logging.config
import yaml


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
        with open('log-config.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            self.logger = logging.getLogger(__name__)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(CustomFormatter())
            self.logger.addHandler(ch)

    def within_range(self) -> bool:
        sump_temp = self.sump_temp.get_temp()
        tank_temp = self.tank_temp.get_temp()
        temp_difference = abs(sump_temp - tank_temp)

        self.logger.info(f"temp difference: {round(temp_difference, 1)} "
                         f"sump: {sump_temp} tank: {tank_temp}")
        return temp_difference <= self.limit
