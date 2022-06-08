## aquarium
![](https://github.com/JayWebDevCom/aquarium/workflows/Python%20CI/badge.svg)

### A water-change management application for aquariums to be run on a raspberry pi
- a python3 learning project
- this application will perform scheduled water-changes on an aquarium with a sump
- water is removed from and replaced into the sump during a water-change
- sump water will not be mixed back into the tank until sump and aquarium tank water are within a configurable temperature band of each other


- scheduling library used is [schedule][scheduling-library] by dbader
- the testing library is [unittest] and makes use of [side-effects]


- 1 [_vl53l0x_][laser-distance-sensor] laser is used to monitor sump  water volume as water level/height
- 2 [_DS18B20_][digital-temp-sensor] digital thermometers are used to monitor sump and water temperature


- setup a virtual environment
```bash
$ python3 -m virtualenv env --python=python3.10
$ activate
```

- install library dependencies
```bash
$ python3 -m pip install -r requirements.txt
```

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

- initialize thermometers, restart pi after
```bash
$ sudo modprobe w1-gpio
$ sudo modprobe w1-therm
```

### configuration
- place your _vl53l0x_ device suspended roughly 15cm above your sump water surface
- configure by updating [com/config.yaml](com/config.yaml) with
- `sump_temp_device_id` and `tank_temp_device_id` variables with your corresponding _DS18B20_  device ids
- `pump_out_channel` `pump_in_channel` and `sump_pump_channel` variables with your corresponding relay pins for your drain pump, clean water input pump and sump return to aquarium pump respectively
- `full_level`: laser reading when your sump is operationally full
- `water_change_span`: laser reading difference between `full_level`, and minimum sump water height when your sump is operationally empty i.e. empty but your pumps won't burn
- `times_to_check_level`: an average reading is taken for sump level (water height) this is the number of laser readings to take tp calculate this average
- `overfill_allowance`: an error will be raised when readings are greater than `full_level`, or less than `full_level` minus `water_change_span` minus `overfill_allowance`
- `accuracy_allowance`: laser readings are sanitized, this is a % that describes the upper and lower bounds of the sump levels for which readings should be discarded 
- `level_check_interval`: interval in seconds between sump water height readings during a water-change
- `temp_check_interval`:  interval in seconds between temperature equalization readings as the final step in a water-change
- `temperature_difference_band`: max temperature difference between the tank and sump below which water recirculation can recommence after a water-change
- `water_change_level`: % of sump water to extract when your sump max water height is `full_level`, and empty level is `full_level` minus `water_change_span`


- using the current configuration 
  - logged updates of sump height, sump temp and tank temp will occur every 15 mins
  - water changes will occur 5 times a day at; '09:01', '12:01', '15:01', '18:01', and '21:01'
  
### run the application
```bash
$ python3 com/main.py
```

#### run as a service with [systemctl]
 - example configuration file when this project is located at `/home/pi/Documents/Projects/aquarium`

```text
[Unit]
Description=aquarium

[Service]
Type=simple
ExecStart=/home/pi/Documents/Projects/aquarium/env/bin/python3 /home/pi/Documents/Projects/aquarium/com/main.py
StandardOutput=append:/home/pi/Documents/Projects/aquarium/logs/log.log
StandardError=append:/home/pi/Documents/Projects/aquarium/logs/log.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### top-up or empty sump water by time
```bash
$ env/bin/python3 com/inPumpScript.py --time <num-seconds>
$ env/bin/python3 com/outPumpScript.py --time <num-seconds>
```
a progress bar will be displayed
![add water log](images/add_water_log.png?raw=true "Add Water Log")

#### example log output
 - create text file `logs/log.log`
 - `tail -f /home/pi/Documents/Projects/aquarium/logs/log.log`

![tail log output](images/log_output.png?raw=true "Tail Log Output")


[scheduling-library]: https://github.com/dbader/schedule
[unittest]: (https://docs.python.org/3/library/unittest.html)
[side-effects]: https://docs.python.org/3/library/unittest.mock.html#quick-guide
[systemctl]: https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/
[laser-distance-sensor]: https://www.hobbytronics.co.uk/vl53l0x
[digital-temp-sensor]: https://shop.pimoroni.com/products/ds18b20-programmable-resolution-1-wire-digital-thermometer
