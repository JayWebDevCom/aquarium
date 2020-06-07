from components.LevelStrategy import LevelStrategy


class DefaultLevelStrategy(LevelStrategy):

    def __init__(self, name: str = "default level strategy"):
        super().__init__(name)

    def get_level(self) -> float:
        pass
