import os
from unittest import TestCase

from Configuration import Configuration


class TestConfiguration(TestCase):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_config = "test-config.yaml"
    file_path = f"{current_dir}/{test_config}"

    configuration = Configuration(file_path)

    def test_update_time(self):
        self.assertEqual([':00', ':15', ':30', ':45'], self.configuration.update_times())

    def test_wc_times(self):
        self.assertEqual(['1', '2', '3'], self.configuration.water_change_times())
