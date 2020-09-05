from yaml import load


class Configuration:
    aquarium: dict = {}

    def __init__(self, file_path: str):
        with open(file_path, 'r') as stream:
            try:
                from yaml import CLoader as Loader, CDumper as Dumper
                self.aquarium = load(stream, Loader=Loader)
            except ImportError:
                from yaml import Loader, Dumper

    def water_change_times(self):
        return self.aquarium['water_change_times']

    def update_times(self):
        return self.aquarium['update_times']
