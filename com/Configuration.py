from yaml import safe_load


class Configuration:

    def __init__(self, file_path: str):
        with open(file_path, 'r') as stream:
            try:
                self.aquarium = safe_load(stream)
            except ImportError:
                from yaml import Loader, Dumper

    def water_change_times(self):
        return self.aquarium['water_change_times']

    def update_times(self):
        return self.aquarium['update_times']
