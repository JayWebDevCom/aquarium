## aquarium
![](https://github.com/JayWebDevCom/aquarium/workflows/Python%20CI/badge.svg)

### A water change management application for aquariums to be run on a raspberry pi
- a python3 learning project
- scheduling library used is [schedule by dbader](https://github.com/dbader/schedule)
- the testing library is UnitTest and makes use of side-effects

<br/>

- this aplication will perform scheduled water changes on an aquarium with a sump
- water is removed from and replaced into the sump during a water change
- sump water will not be mixed back into the tank until sump and aquarium tank water are within 1°C of each other

<br/>

- a `vl53l0x` laser is used to monitor water volume as water level/height
- two `DS18B20` digital thermometers are used to monitor sum and water temperature

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

- place your `vl53l0x` device suspended roughly 15cm above your sump water surface
- configure by updating `com/main.py` with
  - `sump_temp_device_id` and `tank_temp_device_id` variables with your corresponding `DS18B20` device ids
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
