from components.LevelsBoundary import LevelsBoundary
from loguru import logger


class ReadingsSanitizer:
    levels_boundary: LevelsBoundary
    upper_bound: float
    lower_bound: float

    def __init__(self, levels_boundary: LevelsBoundary, percentage_bound: float):
        self.upper_bound = levels_boundary.empty_level * (1 + percentage_bound)
        self.lower_bound = levels_boundary.full_level * (1 - percentage_bound)

    def sanitize(self, readings_list) -> float:
        readings_list_copy = readings_list[:]
        accepted_readings_iterator = filter(lambda reading:
                                            self.lower_bound <= reading <= self.upper_bound,
                                            readings_list_copy)
        accepted_readings = list(accepted_readings_iterator)

        removed_readings = [item for item in readings_list_copy if item not in accepted_readings]

        logger.info(f"removed {len(removed_readings)} reading(s) {removed_readings}")
        return round(sum(accepted_readings) / len(accepted_readings), 2)
