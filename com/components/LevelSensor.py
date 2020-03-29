from components import LevelStrategy
from components.DefaultLevelStrategy import DefaultLevelStrategy


class LevelSensor:
    name: str
    level_strategy: LevelStrategy

    def __init__(self, name: str, level_strategy: LevelStrategy = DefaultLevelStrategy()):
        self.name = name
        self.strategy = level_strategy

    def get_level(self) -> int:
        return self.strategy.get_level()
