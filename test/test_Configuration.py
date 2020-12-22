import os
import tempfile
from typing import Any, Union, IO
from unittest import TestCase

import yaml

from Configuration import Configuration


class TestConfiguration(TestCase):
    temp: Union[IO[bytes], IO[Any]]
    configuration: Configuration
    configuration_data = {
        'update_times': [':00', ':15', ':30', ':45'],
        'water_change_times': ['1', '2', '3'],
        'overfill_allowance': 2.5,
        'inner': {'value': 'inner-value'},
        'empty': []
    }

    @classmethod
    def setUpClass(cls):
        TestConfiguration.temp = tempfile.NamedTemporaryFile(delete=False)

        with open(TestConfiguration.temp.name, 'w') as file:
            yaml.dump(TestConfiguration.configuration_data, file)

        TestConfiguration.configuration = Configuration(TestConfiguration.temp.name)

    @classmethod
    def tearDownClass(cls):
        os.remove(TestConfiguration.temp.name)

    def test_update_time(self):
        self.assertEqual([':00', ':15', ':30', ':45'], self.configuration.update_times())

    def test_wc_times(self):
        self.assertEqual(['1', '2', '3'], self.configuration.water_change_times())

    def test_data(self):
        self.assertEqual(TestConfiguration.configuration_data, self.configuration.data())

    def test_data_get(self):
        self.assertEqual(2.5, self.configuration.data()['overfill_allowance'])

    def test_get(self):
        self.assertEqual(2.5, self.configuration.get('overfill_allowance'))

    def test_get_inner(self):
        self.assertEqual('inner-value', self.configuration.data()['inner']['value'])

    def test_get_empty(self):
        self.assertEqual([], self.configuration.data()['empty'])

    def test_get_file_path(self):
        self.assertEqual(TestConfiguration.temp.name, self.configuration.get_file_path())
