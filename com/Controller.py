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
            config: Configuration,
            progress_tracker: ProgressTracker):
        self.sump = sump
        self.scripts = scripts
        self.config = config
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
            formatted_time = ended.strftime("%H:%M")
            interval = ended - started
            interval_minutes_seconds = divmod(interval.total_seconds(), 60)

            progress_tracker.write_ln(f"{Style.YELLOW}{decorated.__name__} complete: "
                                      f"{Style.BOLD}{Style.WHITE}{int(interval_minutes_seconds[0])}m "
                                      f"{int(interval_minutes_seconds[1])}s "
                                      f"{Style.RESET}{Style.YELLOW}at "
                                      f"{Style.BOLD}{Style.WHITE}{formatted_time} ")

        return wrapper

    def start(self):
        self.wait_for_temperature_equalization()
        self.sump.return_pump.on()
        self.update()

    def water_change(self):
        config = Configuration(self.config.get_file_path())
        try:
            self.water_change_process(config.get('water_change_level'))
        except Exception as error:
            logger.error(error)
            self.sump.refill_pump.off()
            self.sump.return_pump.off()
            self.sump.empty_pump.off()
            if config.get('environment') == 'production':
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
            self._write(f"{Style.WHITE}{Style.BOLD}{percent_full}% full{dots.__next__()}")

            if not is_full:
                time.sleep(self.level_check_interval)
            else:
                break

        self._write_finish()
        self.sump.refill_pump.off()

    @log_time_elapsed
    def wait_for_temperature_equalization(self):
        config = Configuration(self.config.get_file_path())
        band = config.get("temperature_difference_band")
        interval = config.get("temp_check_interval")
        yellow, white_bold, reset = Style.YELLOW, f"{Style.WHITE}{Style.BOLD}", Style.RESET

        while True:
            sump_update = self.sump.get_update()
            sump_temps = sump_update.sump_temps
            tank_temps = sump_update.tank_temps
            temperature_difference = sump_update.temp_difference

            self._write(f"{yellow}temp diff: {white_bold}{temperature_difference}c{reset} "
                        f"{yellow}band: {white_bold}{band}c{reset} "
                        f"{yellow}s_temps: {white_bold}{sump_temps}{reset}, "
                        f"{yellow}t_temps: {white_bold}{tank_temps}{reset}")
            if temperature_difference > band:
                for countdown in range(interval-1, -1, -1):
                    self._write(
                        f"{yellow}temp diff: {white_bold}{temperature_difference}c{reset} "
                        f"{yellow}band: {white_bold}{band}c {countdown}{reset} "
                        f"{yellow}s_temps: {white_bold}{sump_temps}{reset}, "
                        f"{yellow}t_temps: {white_bold}{tank_temps}{reset}")
                    time.sleep(1)
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

