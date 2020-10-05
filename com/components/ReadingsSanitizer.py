import statistics

from loguru import logger

from components.LevelsBoundary import LevelsBoundary


class ReadingsSanitizer:
    levels_boundary: LevelsBoundary
    upper_bound: float
    lower_bound: float

    def __init__(self, levels_boundary: LevelsBoundary, percentage_bound: float):
        self.upper_bound = levels_boundary.empty_level * (1 + percentage_bound)
        self.lower_bound = levels_boundary.full_level * (1 - percentage_bound)

    def sanitize(self, readings_list) -> float:
        # logger.info(f"sanitizing: {readings_list}")
        copy = readings_list[:]
        accepted_readings_iterator = filter(lambda reading: self.lower_bound <= reading <= self.upper_bound, copy)
        accepted_readings = list(accepted_readings_iterator)

        removed_readings = [item for item in copy if item not in accepted_readings]
        st_dev = '{:.2f}'.format(statistics.stdev(copy), 2)
        spread = '{:.2f}'.format(max(copy) - min(copy), 2)
        length_removed_readings = len(removed_readings)

        message = "{} {} {} {}, {} {}, {} {}".format("removed", length_removed_readings,
                                                     "reading" if length_removed_readings == 1 else "readings",
                                                     removed_readings,
                                                     "st-dev:", st_dev,
                                                     "spread:", spread)

        # logger.info(message)
        return round(sum(accepted_readings) / len(accepted_readings), 2)
