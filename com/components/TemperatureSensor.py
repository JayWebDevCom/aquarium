from loguru import logger


class TemperatureSensor:
    name: str
    db_device_id_location: str

    def __init__(self, name, db_device_filepath: str, num_sensor_readings: int = 5):
        self.name = name
        self.db_device_filepath = db_device_filepath
        self.num_sensor_readings = num_sensor_readings

    def get_temp(self) -> float:
        attempt = 1
        while attempt <= self.num_sensor_readings:
            try:
                with open(self.db_device_filepath) as file:
                    text = file.read()

                second_line = text.split("\n")[1]
                temperature_data = second_line.split(" ")[9]
                temperature = float(temperature_data[2:])
                celsius = temperature / 1000
                return celsius

            except IndexError as _:
                logger.error(f"Unable to get temp from {self._id(self.db_device_filepath)} at attempt {attempt}")
                attempt += 1
                pass

        raise IndexError(f"Couldn't get reading from {self._id(self.db_device_filepath)}")

    @staticmethod
    def _id(value: str) -> str:
        return value.split("/")[-2]
