import adafruit_vl53l0x
from adafruit_extended_bus import ExtendedI2C as I2C
from loguru import logger

from components.LevelStrategy import LevelStrategy


class TimeOfFlightLevelStrategy(LevelStrategy):
    name: str

    def __init__(self, name: str = "time of flight VL53L0X adafruit"):
        super().__init__(name)
        i2c = I2C(1)
        self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        self.vl53.measurement_timing_budget = 40000

    def get_level(self) -> float:
        try:
            return self.vl53.range / 10
        except Exception as error:
            logger.error(error)
