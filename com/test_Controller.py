"""
from unittest import TestCase
from unittest.mock import call, MagicMock, Mock

from Controller import Controller
from components.LevelDetector import UnexpectedWaterLevel


# This test will pass if
#  - Controller lines 58, 60, 62 are commented out
#  - Switch lines 1, 15, 19 are commented out


class TestController(TestCase):
    water_detector = MagicMock()
    temperature_detector = MagicMock()

    pump_out = MagicMock()
    pump_in = MagicMock()
    sump_pump = MagicMock()

    controller = Controller("some name", water_detector, temperature_detector, pump_out, pump_in, sump_pump)

    def test_catches_exception_and_stops_pumps(self):
        self.water_detector.percentage_changed = Mock(side_effect=UnexpectedWaterLevel(100))

        self.controller.water_change(50)

        sump_calls = [call.off()]
        pump_out_calls = [call.on(), call.off()]
        pump_in_calls = [call.off()]

        self.sump_pump.assert_has_calls(sump_calls)
        self.pump_out.assert_has_calls(pump_out_calls, any_order=False)
        self.pump_in.assert_has_calls(pump_in_calls, any_order=False)
"""



