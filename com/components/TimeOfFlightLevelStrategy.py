from components.LevelStrategy import LevelStrategy
import board
import busio
import adafruit_vl53l0x


class TimeOfFlightLevelStrategy(LevelStrategy):
    name: str

    def __init__(self, name: str = "time of flight VL53L0X adafruit"):
        super().__init__(name)
        i2c = busio.I2C(board.SCL, board.SDA)
        self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        self.vl53.measurement_timing_budget = 40000

    def get_level(self) -> float:
        return self.vl53.range / 10
