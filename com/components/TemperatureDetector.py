from components import TemperatureSensor


class TemperatureDetector:
    """A simple TemperatureDetector class"""
    name: str
    sump_temp: TemperatureSensor
    tank_temp: TemperatureSensor
    limit: float

    def __init__(
            self, name: str,
            sump_temp: TemperatureSensor,
            tank_temp: TemperatureSensor):
        self.name = name
        self.sump_temp = sump_temp
        self.tank_temp = tank_temp

    def temperature_difference(self) -> float:
        sump_temp = self.sump_temp.get_temp()
        tank_temp = self.tank_temp.get_temp()
        temp_difference = abs(sump_temp - tank_temp)

        return round(temp_difference, 2)
