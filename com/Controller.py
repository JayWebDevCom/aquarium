import os
import time
from datetime import datetime
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
    level_detector: LevelDetector
    level_check_interval: int
    temp_check_interval: int

    def __init__(
            self,
            name: str,
            level_detector: LevelDetector,
            temperature_detector: TemperatureDetector,
            pump_out: Switch,
            pump_in: Switch,
            sump_return: Switch,
            **kwargs):
        self.name = name
        self.level_detector = level_detector
        self.temperature_detector = temperature_detector
        self.pump_out = pump_out
        self.pump_in = pump_in
        self.sump_return = sump_return
        self.level_check_interval = kwargs.pop("level_check_interval")
        self.temp_check_interval = kwargs.pop("temp_check_interval")
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

    def log_time_elapsed(decorated):
        def wrapper(*args):
            started = datetime.now()

            decorated(*args)

            ended = datetime.now()
            interval = ended - started
            interval_minutes_seconds = divmod(interval.total_seconds(), 60)
            logger.info(f"{decorated.__name__} complete: {int(interval_minutes_seconds[0])}m "
                        f"{int(interval_minutes_seconds[1])}s")

        return wrapper

    @log_time_elapsed
    def water_change(self, percentage: float):
        # if x := isBig(y): return x
        self.empty_by_percentage(percentage)
        self.refill()
        self.wait_for_temperature_equalization()

    @log_time_elapsed
    def empty_by_percentage(self, percentage):
        self.sump_return.off()
        self.pump_out.on()
        try:
            while True:
                percentage_changed = self.level_detector.percentage_changed()
                formatted_percentage_changed = "{:.2f}".format(percentage_changed)
                logger.info(f"percentage changed is {formatted_percentage_changed}")
                if percentage_changed < percentage:
                    time.sleep(self.level_check_interval)
                else:
                    break
        except UnexpectedWaterLevel:
            logger.error("UnexpectedWaterLevel ex caught")
            self.pump_in.off()
            self.pump_out.off()
            exit(1)
        self.pump_out.off()

    @log_time_elapsed
    def refill(self):
        logger.info("refilling")

        self.pump_in.on()

        try:
            while not self.level_detector.is_sump_full():
                time.sleep(self.level_check_interval)
        except UnexpectedWaterLevel:
            logger.error("UnexpectedWaterLevel ex caught while refilling")
            self.pump_in.off()
            self.pump_out.off()
            exit(1)

        self.pump_in.off()

    @log_time_elapsed
    def wait_for_temperature_equalization(self):
        logger.info("waiting for sump and tank temperatures to equalize")
        while not self.temperature_detector.within_range():
            time.sleep(self.temp_check_interval)

        self.sump_return.on()

    def update(self):
        with open(f"{self.current_dir}/temperatureScript_both.py", "r") as f:
            exec(f.read())
        with open(f"{self.current_dir}/levelSensorWithTofScript.py", "r") as f:
            exec(f.read())
