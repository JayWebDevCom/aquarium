__package__ = "components.mocks"


class MockSumpTemperatureSensor:
    name: str
    test_temp = 18

    def __init__(self, name):
        self.name = name

    def get_temp(self) -> float:
        print(f"{self.name} temperature is {self.test_temp}")
        self.test_temp += 1
        return self.test_temp
