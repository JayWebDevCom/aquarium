import tempfile
from typing import List
from unittest import TestCase

from com.components.TemperatureSensor import TemperatureSensor


class TestTemperatureSensor(TestCase):

    def test_handles_file_exception(self):
        file = tempfile.NamedTemporaryFile()

        with open(file.name, 'w') as f:
            f.write("")

        sensor = TemperatureSensor("error sump", file.name)

        with self.assertRaises(IndexError) as e:
            sensor.get_temp()
        self.assertEqual(f"Couldn't get reading from {file.name.split('/')[-2]}", str(e.exception))

    def test_handles_sensor_exception_fewer_exceptions(self):
        file = tempfile.NamedTemporaryFile()

        with open(file.name, 'w') as f:
            f.write("c1 01 4b 46 7f ff 0c 10 6d : crc=6d YES\n")
            f.write("72 01 4b 46 7f ff 0c 10 c6 t=23125")

        sensor = TemperatureSensor("error sump", file.name)

        self.assertEqual(sensor.get_temp(), 23.125)


class TestTemperatures:
    sump: List[float]
    tank: List[float]

    def __init__(self, sump: List[float], tank: List[float]):
        self.sump = sump
        self.tank = tank
