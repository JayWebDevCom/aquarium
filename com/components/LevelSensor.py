__package__ = "components"


class LevelSensor:
    name: str

    def __init__(self, name):
        self.name = name
        self.level = 1000

    def get_level(self) -> int:
        print(f"{self.name} water level is {self.level}")
        return self.level
