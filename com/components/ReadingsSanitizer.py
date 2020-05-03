from components.LevelsBoundary import LevelsBoundary
from loguru import logger


class ReadingsSanitizer:
    levels_boundary: LevelsBoundary
    upper_bound: int
    lower_bound: int

    def __init__(self, levels_boundary: LevelsBoundary, percentage_bound: float):
        upper_bound = int(levels_boundary.empty_level * (1 + percentage_bound))
        lower_bound = int(levels_boundary.full_level * (1 - percentage_bound))
        self.acceptable_range = range(lower_bound, upper_bound)

    def sanitize(self, readings_list) -> int:
        readings_list_copy = readings_list[:]
        accepted_readings_iterator = filter(lambda reading: reading in self.acceptable_range, readings_list_copy)
        accepted_readings = list(accepted_readings_iterator)

        removed_readings = [item for item in readings_list_copy if item not in accepted_readings]

        logger.info(f"removed {len(removed_readings)} reading(s) {removed_readings}")
        return int(sum(accepted_readings) / len(accepted_readings))
