__package__ = "components"


class MockLevelSensor:
    name: str
    level: int

    def __init__(self, name):
        self.name = name
        self.level = 20

    def get_level(self):
        print(f"{self.name} water level is {self.level}")
        self.level += 1
        return self.level
