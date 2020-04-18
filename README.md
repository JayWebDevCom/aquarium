## aquarium  ![](https://github.com/JayWebDevCom/aquarium/workflows/Python%20CI/badge.svg)

### A water change management application for aquariums to be run on a raspberry pi
- A python3 learning project
- Scheduling library used is [schedule by dbader](https://github.com/dbader/schedule)

- the testing library is UnitTest and makes use of side-effects

<br/>

- run the test suite
```bash
$ python3 -m unittest discover
```

- install dependencies
```bash
$ pip3 install busio
$ pip3 install adafruit-circuitpython-vl53l0x
$ python3 -m pip install --force-reinstall adafruit-blinka
```

- configure by updating `com/main.py` with
  - `sump_temp_device_id` and `tank_temp_device_id` variables with your corresponding `vl53l0x` device id
  - `pump_out_channel` `pump_in_channel` and `sump_pump_channel` variables with your corresponding relay pins for your 
  drain pump, clean water input pump and sump return pump respectively

- adjust the water change percentage settings in `com/main.py` e.g. 50% as
```bash
controller.water_change(50.0)
```

- adjust the schedule settings in `com/main.py` e.g.
```bash
schedule.every().day.at("20:00").do(job).tag("aquarium")
```

- run the application
```bash
$ python3 com/main.py
```
