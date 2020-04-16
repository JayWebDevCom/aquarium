## aquarium  ![](https://github.com/JayWebDevCom/aquarium/workflows/Python%20CI/badge.svg)

### A water change management application for aquariums to be run on a raspberry pi
- A python3 learning project
- Scheduling library used is [schedule by dbader](https://github.com/dbader/schedule)
- V53L0X library used is [V53L0X by johnbryanmoore](https://github.com/johnbryanmoore/VL53L0X_rasp_python)

- the testing library is UnitTest and makes use of side-effects

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

- run the application
```bash
$ python3 com/main.py
```

- adjust the schedule settings in `com/main.py`
