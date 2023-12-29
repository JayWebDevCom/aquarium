import time
from datetime import datetime, timedelta
from typing import List, Tuple

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
            progress_tracker: ProgressTracker,
            tank_drain_valve):
        self.sump = sump
        self.scripts = scripts
        self.config = config
        self.progress_tracker = progress_tracker
        self.tank_drain_valve = tank_drain_valve

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
            self.tank_drain_valve.off()
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
        interval = Configuration(self.config.file_path).get("level_check_interval")

        while True:
            percentage_changed = self.sump.percentage_changed()
            self._write(f"{Style.WHITE}{Style.BOLD}{percentage_changed}% changed of {percentage}%")

            if percentage_changed < percentage:
                time.sleep(interval)
            else:
                break

        self._write_finish()
        self.sump.empty_pump.off()

    @log_time_elapsed
    def refill(self):
        self.sump.refill_pump.on()
        dots = self._generator([".  ", ".. ", "..."])

        interval = Configuration(self.config.file_path).get("level_check_interval")

        while True:
            (is_full, percent_full) = self.sump.get_state()
            self._write(f"{Style.WHITE}{Style.BOLD}{percent_full}% full{dots.__next__()}")

            if not is_full:
                time.sleep(interval)
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
            (sump_temps, tank_temps, temperature_difference) = self.sump.temperature_breakdown()
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

    @log_time_elapsed
    def drain_tank(self):
        config = Configuration(self.config.get_file_path())
        tank_drain_duration = config.get('tank_drain_duration')
        yellow, white_bold, reset = Style.YELLOW, f"{Style.WHITE}{Style.BOLD}", Style.RESET
        try:
            self.tank_drain_valve.on()
            for countdown in range(tank_drain_duration - 1, -1, -1):
                self._write(f"{yellow}drain time remaining: {white_bold}{countdown}{reset} "
                            f"{yellow}of duration: {white_bold}{tank_drain_duration}{reset}")
                time.sleep(1)
            self._write_finish()
            self.tank_drain_valve.off()
        except Exception as error:
            logger.error(error)
            self.sump.refill_pump.off()
            self.sump.return_pump.off()
            self.sump.empty_pump.off()
            self.tank_drain_valve.off()
            if config.get('environment') == 'production':
                exit(1)

    @log_time_elapsed
    def refill_tank_process(self):
        try:
            self.sump.return_pump.off()
            self.refill()
            self.wait_for_temperature_equalization()
            self.sump.return_pump.on()
        except Exception as error:
            logger.error(error)
            self.sump.refill_pump.off()
            self.sump.return_pump.off()
            self.sump.empty_pump.off()
            self.tank_drain_valve.off()
            if self.config.get('environment') == 'production':
                exit(1)

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

    def calculate_sump_refill_times(self, drain_times: List[str]) -> List[str]:
        config = Configuration(self.config.get_file_path())
        simple_time_format = '%H:%M'
        drain_duration, multiplier = config.get('tank_drain_multiplier'), config.get('tank_drain_duration')
        formatted_drain_times = [datetime.strptime(t, simple_time_format) for t in drain_times]
        formatted_refill_times = [t + timedelta(seconds=drain_duration * multiplier) for t in formatted_drain_times]
        refill_times = [datetime.strftime(t, simple_time_format) for t in formatted_refill_times]
        return refill_times

    def times(self) -> List[str]:
        return []

    def breakdown(self) -> Tuple[float, float, float]:
        return self.sump.temperature_breakdown()
