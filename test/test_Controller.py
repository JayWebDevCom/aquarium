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
        'tank_drain_duration': 1,
        'tank_drain_multiplier': 60,
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
    tank_drain_valve = MagicMock()
    scripts = []

    def test_executes_water_change(self):
        self.sump.percentage_changed = Mock(return_value=100)
        self.sump.get_state = Mock(return_value=(True, 100))
        self.sump.temperature_breakdown = Mock(return_value=([2, 3, 4], [3, 4, 5], 1))

        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker(), self.tank_drain_valve)
        controller.water_change()

        sump_calls = [
            call.return_pump.off(),
            call.empty_pump.on(),
            call.percentage_changed(),
            call.empty_pump.off(),
            call.refill_pump.on(),
            call.get_state(),
            call.refill_pump.off(),
            call.temperature_breakdown(),
            call.return_pump.on()
        ]

        self.sump.assert_has_calls(sump_calls, any_order=False)

    def test_catches_exception_and_stops_pumps(self):
        self.sump.percentage_changed = Mock(side_effect=UnexpectedWaterLevel(100))
        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker(), self.tank_drain_valve)
        controller.water_change()

        tank_drain_calls = [
            call.off()
        ]

        self.tank_drain_valve.assert_has_calls(tank_drain_calls, any_order=False)

        sump_calls = [
            call.return_pump.off(),
            call.empty_pump.on(),
            call.percentage_changed(),
            call.refill_pump.off(),
            call.return_pump.off(),
            call.empty_pump.off()
        ]

        self.sump.assert_has_calls(sump_calls, any_order=False)

    def test_executes_tank_drain(self):
        self.sump.percentage_changed = Mock(return_value=100)
        self.sump.get_state = Mock(return_value=(True, 100))
        self.sump.temperature_breakdown = Mock(return_value=([2, 3, 4], [3, 4, 5], 1))

        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker(), self.tank_drain_valve)
        controller.drain_tank()

        tank_drain_calls = [
            call.on(),
            call.off()
        ]

        self.tank_drain_valve.assert_has_calls(tank_drain_calls, any_order=False)

    def test_catches_exception_and_stops_pumps_on_tank_drain(self):
        self.tank_drain_valve.on = Mock(side_effect=Exception('test-exception'))
        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker(), self.tank_drain_valve)
        controller.drain_tank()

        tank_drain_calls = [
            call.on(),
            call.off()
        ]

        self.tank_drain_valve.assert_has_calls(tank_drain_calls, any_order=False)

        sump_calls = [
            call.refill_pump.off(),
            call.return_pump.off(),
            call.empty_pump.off()
        ]

        self.sump.assert_has_calls(sump_calls, any_order=False)

    def test_executes_refill_process(self):
        self.sump.percentage_changed = Mock(return_value=100)
        self.sump.get_state = Mock(return_value=(True, 100))
        self.sump.temperature_breakdown = Mock(return_value=([2, 3, 4], [3, 4, 5], 1))

        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker(), self.tank_drain_valve)
        controller.refill_tank_process()

        sump_calls = [
            call.return_pump.off(),
            call.refill_pump.on(),
            call.get_state(),
            call.refill_pump.off(),
            call.temperature_breakdown(),
            call.return_pump.on()
        ]

        self.sump.assert_has_calls(sump_calls, any_order=False)

    def test_catches_exception_and_stops_pumps_on_refill_tank_process(self):
        sump = MagicMock()
        sump.refill_pump.on = Mock(side_effect=UnexpectedWaterLevel(100))
        controller = Controller(sump, self.scripts, self.configuration, ProgressTracker(), self.tank_drain_valve)
        controller.refill_tank_process()

        sump_calls = [
            call.return_pump.off(),
            call.refill_pump.on(),
            call.refill_pump.off(),
            call.return_pump.off(),
            call.empty_pump.off()
        ]

        sump.assert_has_calls(sump_calls, any_order=False)

    def test_calculate_sump_refill_times(self):
        controller = Controller(self.sump, self.scripts, self.configuration, ProgressTracker(), self.tank_drain_valve)
        refill_times = controller.calculate_sump_refill_times(['01:30', '02:00', '03:13', '23:59'])
        expected_sump_refill_times = ['01:31', '02:01', '03:14', '00:00']
        self.assertEqual(expected_sump_refill_times, refill_times)
