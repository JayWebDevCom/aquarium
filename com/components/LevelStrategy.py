class LevelStrategy:
    name: str

    def __init__(self, name: str):
        self.name = name

    def get_level(self) -> float:
        raise IllegalArgumentError


class IllegalArgumentError(ValueError):
    pass
