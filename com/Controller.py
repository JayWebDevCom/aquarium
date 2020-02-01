import time

from components.Switch import Switch
from components.LevelDetector import LevelDetector
from components.TemperatureDetector import TemperatureDetector


class Controller:
    """A simple Controller class"""
    name: str
    pump_out: Switch
    pump_in: Switch
    water_detector: LevelDetector
    level_delay: int
    temperature_delay: int

    def __init__(
            self,
            name: str,
            level_detector: LevelDetector,
            temperature_detector: TemperatureDetector,
            pump_out: Switch,
            pump_in: Switch,
            level_delay: int = 1,
            temperature_delay: int = 1):
        self.name = name
        self.water_detector = level_detector
        self.temperature_detector = temperature_detector
        self.pump_out = pump_out
        self.pump_in = pump_in
        self.level_delay = level_delay
        self.temperature_delay = temperature_delay

    def get_name(self):
        return self.name

    def water_change(self, percentage: float):
        # if x := isBig(y): return x
        while self.water_detector.percentage_changed() < percentage:
            print(f"percentage changed is {round(self.water_detector.percentage_changed(), 2)}%")
            time.sleep(self.level_delay)
        self.pump_out.off()

        while not self.temperature_detector.within_range():
            time.sleep(self.temperature_delay)

        self.pump_in.on()
