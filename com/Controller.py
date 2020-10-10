import time
import schedule
from datetime import datetime
from typing import List

from loguru import logger

from Configuration import Configuration
from ProgressBar import ProgressTracker
from components.LevelDetector import LevelDetector
from components.Switch import Switch
from components.TemperatureDetector import TemperatureDetector


class Controller:
    def __init__(
            self,
            level_detector: LevelDetector,
            temperature_detector: TemperatureDetector,
            pump_out: Switch,
            pump_in: Switch,
            sump_pump: Switch,
            scripts: List[str],
            configuration_file: str):
        self.level_detector = level_detector
        self.temperature_detector = temperature_detector
        self.pump_out = pump_out
        self.pump_in = pump_in
        self.sump_pump = sump_pump
        self.scripts = scripts
        self.configuration_file = configuration_file
        self.config = Configuration(configuration_file)
        self.level_check_interval = self.config.get("level_check_interval")
        self.progress_tracker = ProgressTracker("\033[33m")

    def log_time_elapsed(self, decorated):
        def wrapper(*args):
            started = datetime.now()

            decorated(*args)

            ended = datetime.now()
            interval = ended - started
            interval_minutes_seconds = divmod(interval.total_seconds(), 60)
            self.progress_tracker.write_ln(f"{decorated.__name__} complete: {int(interval_minutes_seconds[0])}m "
                                           f"{int(interval_minutes_seconds[1])}s")

        return wrapper

    def start(self):
        self.sump_pump.on()
        self.schedule_updates()
        self.schedule_water_changes()

        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_updates(self):
        for value in self.config.update_times():
            schedule.every().hour.at(value).do(self.updates).tag("update")

    def updates(self):
        schedule.clear("water_change")
        self.update()
        self.schedule_water_changes()

    def schedule_water_changes(self):
        water_change_times = Configuration(self.configuration_file).water_change_times()
        self.progress_tracker.write_ln(f"scheduling water changes for: {water_change_times}")
        for value in water_change_times:
            schedule.every().day.at(value).do(self.water_change).tag("water_change")

    def water_change(self):
        config = Configuration(self.configuration_file)
        schedule.clear("update")
        self.progress_tracker.write_ln("")
        self.progress_tracker.write_ln("Water change beginning...")
        self.water_change_process(config.get('water_change_level'))
        self.schedule_updates()

    @log_time_elapsed
    def water_change_process(self, percentage: float):
        self.sump_pump.off()
        self.empty_by_percentage(percentage)
        self.refill()
        self.wait_for_temperature_equalization()
        self.sump_pump.on()

    @log_time_elapsed
    def empty_by_percentage(self, percentage):
        self.pump_out.on()
        progress_tracker = ProgressTracker()

        try:
            while True:
                percentage_changed = self.level_detector.percentage_changed()
                self.progress_tracker.write_ln(f"{percentage_changed}% changed of {percentage}%")

                if percentage_changed < percentage:
                    time.sleep(self.level_check_interval)
                else:
                    break
        except Exception as error:
            self._shutdown(error)

        progress_tracker.finish()
        self.pump_out.off()

    @log_time_elapsed
    def refill(self):
        self.progress_tracker.write_ln("refilling")
        self.pump_in.on()
        progress_tracker = ProgressTracker()
        dots = self._generator([".  ", ".. ", "..."])

        try:
            while True:
                (is_full, percent_full) = self.level_detector.get_sump_state()
                self.progress_tracker.write_ln(f"{percent_full} full{dots.__next__()}")

                if not is_full:
                    time.sleep(self.level_check_interval)
                else:
                    break
        except Exception as error:
            self._shutdown(error)

        progress_tracker.finish()
        self.pump_in.off()

    @log_time_elapsed
    def wait_for_temperature_equalization(self):
        config = Configuration(self.configuration_file)
        band = config.get("temperature_difference_band")
        interval = config.get("temp_check_interval")

        progress_tracker = ProgressTracker()
        try:
            while True:
                temperature_difference = self.temperature_detector.temperature_difference()
                self.progress_tracker.write_ln(f"temperature difference: {temperature_difference}c of band: {band}c")

                if temperature_difference > band:
                    time.sleep(interval)
                else:
                    break
        except Exception as error:
            self._shutdown(error)

        progress_tracker.finish()

    def update(self):
        for script in self.scripts:
            with open(script, "r") as f:
                exec(f.read())

    def _shutdown(self, error):
        logger.error(f"{error.__class__.__name__} ex caught")
        self.pump_in.off()
        self.pump_out.off()
        exit(1)

    @staticmethod
    def _generator(lst: List):
        while 1:
            for i in lst:
                yield i
