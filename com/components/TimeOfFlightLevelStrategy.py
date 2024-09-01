from components.LevelStrategy import LevelStrategy
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_vl53l0x


class TimeOfFlightLevelStrategy(LevelStrategy):
    name: str

    def __init__(self, name: str = "time of flight VL53L0X adafruit"):
        super().__init__(name)
        i2c = I2C(1)
        self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        self.vl53.measurement_timing_budget = 40000

    def get_level(self) -> float:
        return self.vl53.range / 10
