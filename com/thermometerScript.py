#!/usr/bin/env python3
import time

# device_id = "28-0300a2792070"
device_id = "28-0300a279088e"


class TempSensor:
    name: str
    db_device_id_location: str

    def __init__(self, name: str, db_device_id: str):
        self.name = name
        self.db_device_id_location = '/sys/bus/w1/devices/' + db_device_id + '/w1_slave'

    def get_temp(self) -> float:
        device_file = open(self.db_device_id_location)
        text = device_file.read()
        device_file.close()
        second_line = text.split("\n")[1]
        temperature_data = second_line.split(" ")[9]
        temperature = float(temperature_data[2:])
        celsius = temperature / 1000
        return celsius


temperature_sensor = TempSensor("test sensor", device_id)

for i in range(0, 10):
    time.sleep(1)
    print(temperature_sensor.get_temp())
