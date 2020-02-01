__package__ = "components.mocks"


class MockTankTemperatureSensor:
    name: str
    test_temp: float

    def __init__(self, name):
        self.name = name
        self.test_temp = 28.0

    def get_temp(self) -> float:
        print(f"{self.name} temperature is {self.test_temp}")
        return self.test_temp

