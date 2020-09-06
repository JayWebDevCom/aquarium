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

    def test_data(self):
        data = {
            'inner': {'value': 'inner-value'},
            'overfill_allowance': 2.5,
            'update_times': [':00', ':15', ':30', ':45'],
            'water_change_times': ['1', '2', '3'],
            'empty': []
        }
        self.assertEqual(data, self.configuration.data())

    def test_data_get(self):
        self.assertEqual(2.5, self.configuration.data()['overfill_allowance'])

    def test_get(self):
        self.assertEqual(2.5, self.configuration.get('overfill_allowance'))

    def test_get_inner(self):
        self.assertEqual('inner-value', self.configuration.data()['inner']['value'])

    def test_get_empty(self):
        self.assertEqual([], self.configuration.data()['empty'])
