import os
import tempfile
from typing import Union, IO, Any
from unittest import TestCase
from unittest.mock import call, MagicMock, Mock

import yaml

from Configuration import Configuration
from Controller import Controller
from Progress import ProgressTracker
from components.Sump import UnexpectedWaterLevel


class TestController(TestCase):
    temp: Union[IO[bytes], IO[Any]]
    configuration: Configuration
    configuration_data = {
        'level_check_interval': 1,
        'temperature_difference_band': 1,
        'water_change_level': 50,
        'temp_check_interval': 1,
        'environment': 'not-production'
    }

    @classmethod
    def setUpClass(cls):
        TestController.temp = tempfile.NamedTemporaryFile(delete=False)

        with open(TestController.temp.name, 'w') as file:
            yaml.dump(TestController.configuration_data, file)

        TestController.configuration = Configuration(TestController.temp.name)

    @classmethod
    def tearDownClass(cls):
        os.remove(TestController.temp.name)

    level_detector = MagicMock()
    temperature_detector = MagicMock()
    sump = MagicMock()
    scripts = []

    def test_executes_water_change(self):
        self.sump.percentage_changed = Mock(return_value=100)
        self.sump.get_state = Mock(return_value=(True, 100))
        self.sump.temperature_difference = Mock(return_value=0)

        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker())
        controller.water_change()

        sump_calls = [
            call.return_pump.off(),
            call.empty_pump.on(),
            call.percentage_changed(),
            call.empty_pump.off(),
            call.refill_pump.on(),
            call.get_state(),
            call.refill_pump.off(),
            call.temperature_difference(),
            call.return_pump.on()
        ]

        self.sump.assert_has_calls(sump_calls, any_order=False)

    def test_catches_exception_and_stops_pumps(self):
        self.sump.percentage_changed = Mock(side_effect=UnexpectedWaterLevel(100))
        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker())
        controller.water_change()

        sump_calls = [
            call.return_pump.off(),
            call.empty_pump.on(),
            call.percentage_changed(),
            call.refill_pump.off(),
            call.return_pump.off(),
            call.empty_pump.off()
        ]

        self.sump.assert_has_calls(sump_calls, any_order=False)
