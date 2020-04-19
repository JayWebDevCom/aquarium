import time
from components.Switch import Switch
from components.LevelDetector import LevelDetector, UnexpectedWaterLevel
from components.TemperatureDetector import TemperatureDetector
from loguru import logger


class Controller:
    """A simple Controller class"""
    name: str
    pump_out: Switch
    pump_in: Switch
    sump_return: Switch
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
            sump_return: Switch,
            level_delay: int = 1,
            temperature_delay: int = 1):
        self.name = name
        self.water_detector = level_detector
        self.temperature_detector = temperature_detector
        self.pump_out = pump_out
        self.pump_in = pump_in
        self.sump_return = sump_return
        self.level_delay = level_delay
        self.temperature_delay = temperature_delay

    def get_name(self):
        return self.name

    def water_change(self, percentage: float):
        # if x := isBig(y): return x
        self.empty_by_percentage(percentage)
        self.refill()

    def empty_by_percentage(self, percentage):
        self.sump_return.off()
        self.pump_out.on()
        try:
            while True:
                percentage_changed = self.water_detector.percentage_changed()
                logger.info(f"percentage changed is {round(percentage_changed, 2)}%")
                if percentage_changed < percentage:
                    time.sleep(self.level_delay)
                else:
                    break
        except UnexpectedWaterLevel:
            logger.error("UnexpectedWaterLevel ex caught")
            self.pump_in.off()
            self.pump_out.off()
            exit(1)
        self.pump_out.off()

    def refill(self):
        logger.info("refilling")

        self.pump_in.on()

        try:
            while not self.water_detector.is_sump_full():
                time.sleep(self.level_delay)
        except UnexpectedWaterLevel:
            logger.error("UnexpectedWaterLevel ex caught while refilling")
            self.pump_in.off()
            self.pump_out.off()
            exit(1)

        self.pump_in.off()

        while not self.temperature_detector.within_range():
            time.sleep(self.temperature_delay)

        self.sump_return.on()
