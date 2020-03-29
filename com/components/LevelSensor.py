#__package__ = "components"

from components.dependencies import VL53L0X

class LevelSensor:
    name: str

    def __init__(self, name):
        self.name = name
        self.tof = VL53L0X.VL53L0X()
        self.tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    def get_level(self) -> int:
        return int(self.tof.get_distance()/10)
