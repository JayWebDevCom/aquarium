

class TemperatureSensor:
    name: str
    db_device_id_location: str

    def __init__(self, name, db_device_id: str):
        self.name = name
        self.db_device_id_location = f"/sys/bus/w1/devices/{db_device_id}/w1_slave"

    def get_temp(self) -> float:
        with open(self.db_device_id_location) as file:
            text = file.read()

        second_line = text.split("\n")[1]
        temperature_data = second_line.split(" ")[9]
        temperature = float(temperature_data[2:])
        celsius = temperature / 1000
        return celsius
