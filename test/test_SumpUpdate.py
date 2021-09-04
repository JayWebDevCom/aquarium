from unittest import TestCase

from components.SumpUpdate import SumpUpdate


class TestSumpUpdate(TestCase):

    def test_ok(self):
        update_1 = SumpUpdate(
            sump_temps=[],
            tank_temps=[],
            temp_difference=1.1,
            sump_level=12.1
        )

        update_2 = SumpUpdate(
            sump_temps=[],
            tank_temps=[],
            temp_difference=1.1,
            sump_level=12.1
        )

        self.assertEqual(update_1, update_2)
