from yaml import safe_load


class Configuration:

    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(self.file_path, 'r') as stream:
            try:
                self.aquarium = safe_load(stream)
            except ImportError:
                from yaml import Loader, Dumper

    def water_change_times(self):
        return self.aquarium['water_change_times']

    def tank_drain_times(self):
        return self.aquarium['tank_drain_times']

    def update_times(self):
        return self.aquarium['update_times']

    def data(self):
        return self.aquarium

    def get(self, value):
        return self.aquarium[value]

    def get_file_path(self):
        return self.file_path

    def write_data(self, data: dict):
        with open(self.file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
