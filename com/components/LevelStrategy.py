class LevelStrategy:
    name: str

    def __init__(self, name: str):
        self.name = name

    def get_level(self) -> int:
        raise IllegalArgumentError


class IllegalArgumentError(ValueError):
    pass
