from components.LevelsBoundary import LevelsBoundary
from components.CustomFormatter import CustomFormatter
import logging.config
import yaml


class ReadingsSanitizer:
    levels_boundary: LevelsBoundary
    upper_bound: int
    lower_bound: int

    def __init__(self, levels_boundary: LevelsBoundary, percentage_bound: float):
        upper_bound = int(levels_boundary.empty_level * (1 + percentage_bound))
        lower_bound = int(levels_boundary.full_level * (1 - percentage_bound))
        self.acceptable_range = range(lower_bound, upper_bound)
        with open('log-config.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            self.logger = logging.getLogger(__name__)
            ch = logging.StreamHandler()
            ch.setFormatter(CustomFormatter())
            self.logger.addHandler(ch)

    def sanitize(self, readings_list) -> int:
        removed_readings = []

        for item in readings_list[:]:
            if item not in self.acceptable_range:
                readings_list.remove(item)
                removed_readings.append(item)

        self.logger.info(f"removed {len(removed_readings)} reading(s) {removed_readings}")
        return int(sum(readings_list) / len(readings_list))
