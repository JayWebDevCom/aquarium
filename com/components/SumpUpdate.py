from typing import List


class SumpUpdate(object):
    def __init__(self,
                 sump_temps: List[int],
                 tank_temps: List[int],
                 temp_difference: float,
                 sump_level: float):
        self.sump_temps = sump_temps
        self.tank_temps = tank_temps
        self.temp_difference = temp_difference
        self.sump_level = sump_level

    def __eq__(self, other):
        if isinstance(other, SumpUpdate):
            return self.sump_temps == other.sump_temps and \
                   self.tank_temps == other.tank_temps and \
                   self.temp_difference == other.temp_difference and \
                   self.sump_level == other.sump_level
        return False
