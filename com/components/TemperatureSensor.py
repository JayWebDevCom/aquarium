__package__ = "components"


class TemperatureSensor:
    name: str
    level: int

    def __init__(self, name):
        self.name = name
        self.level = 20

    def get_temp(self) -> float:
        return 1.0
