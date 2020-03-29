from components.LevelStrategy import LevelStrategy
from components.dependencies import VL53L0X


class TimeOfFlightLevelStrategy(LevelStrategy):
    name: str

    def __init__(self, name: str = "time of flight VL53L0X"):
        super().__init__(name)
        self.tof = VL53L0X.VL53L0X()
        self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    def get_level(self) -> int:
        return int(self.tof.get_distance()/10)
