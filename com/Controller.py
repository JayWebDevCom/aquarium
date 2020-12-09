import time
from datetime import datetime
from typing import List

from loguru import logger

from Configuration import Configuration
from Progress import ProgressTracker, Style
from components.Sump import Sump


class Controller:
    def __init__(
            self,
            sump: Sump,
            scripts: List[str],
            configuration_file_path: str,
            progress_tracker: ProgressTracker):
        self.sump = sump
        self.scripts = scripts
        self.configuration_file = configuration_file_path
        self.config = Configuration(configuration_file_path)
        self.level_check_interval = self.config.get("level_check_interval")
        self.progress_tracker = progress_tracker

    def log_time_elapsed(decorated):
        def wrapper(*args):
            progress_tracker = ProgressTracker()
            print("")
            progress_tracker.write_ln(f"{Style.YELLOW}{decorated.__name__} starting:")
            started = datetime.now()

            decorated(*args)

            ended = datetime.now()
            interval = ended - started
            interval_minutes_seconds = divmod(interval.total_seconds(), 60)
            progress_tracker.write_ln(f"{Style.YELLOW}{decorated.__name__} complete: "
                                      f"{Style.BOLD}{Style.WHITE}{int(interval_minutes_seconds[0])}m "
                                      f"{int(interval_minutes_seconds[1])}s")

        return wrapper

    def start(self):
        self.sump.return_pump.on()
        self.update()

    def water_change(self):
        config = Configuration(self.configuration_file)
        try:
            self.water_change_process(config.get('water_change_level'))
        except Exception as error:
            logger.error(f"{error.__class__.__name__} ex caught")
            self.sump.return_pump.off()
            self.sump.empty_pump.off()
            exit(1)

    @log_time_elapsed
    def water_change_process(self, percentage: float):
        self.sump.return_pump.off()
        self.empty_by_percentage(percentage)
        self.refill()
        self.wait_for_temperature_equalization()
        self.sump.return_pump.on()

    @log_time_elapsed
    def empty_by_percentage(self, percentage):
        self.sump.empty_pump.on()

        while True:
            percentage_changed = self.sump.percentage_changed()
            self._write(f"{Style.WHITE}{Style.BOLD}{percentage_changed}% changed of {percentage}%")

            if percentage_changed < percentage:
                time.sleep(self.level_check_interval)
            else:
                break

        self._write_finish()
        self.sump.empty_pump.off()

    @log_time_elapsed
    def refill(self):
        self.sump.refill_pump.on()
        dots = self._generator([".  ", ".. ", "..."])

        while True:
            (is_full, percent_full) = self.sump.get_state()
            self._write(f"{Style.WHITE}{Style.BOLD}{percent_full} full{dots.__next__()}")

            if not is_full:
                time.sleep(self.level_check_interval)
            else:
                break

        self._write_finish()
        self.sump.refill_pump.off()

    @log_time_elapsed
    def wait_for_temperature_equalization(self):
        config = Configuration(self.configuration_file)
        band = config.get("temperature_difference_band")
        interval = config.get("temp_check_interval")

        while True:
            temperature_difference = self.sump.temperature_difference()
            self._write(f"{Style.WHITE}{Style.BOLD}temperature difference: {temperature_difference}c of band: {band}c")

            if temperature_difference > band:
                time.sleep(interval)
            else:
                break

        self._write_finish()

    def update(self):
        for script in self.scripts:
            with open(script, "r") as f:
                exec(f.read())

    @staticmethod
    def _generator(lst: List):
        while 1:
            for i in lst:
                yield i

    def _write(self, message):
        self.progress_tracker.write(message)

    def _write_ln(self, message):
        self.progress_tracker.write_ln(message)

    def _write_finish(self):
        self.progress_tracker.finish()
