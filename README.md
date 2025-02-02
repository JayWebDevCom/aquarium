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
$ virtualenv --python=/usr/bin/python3 env
$ source env/bin/activate
```

- install library dependencies
```bash
$ python3 -m pip install -r requirements.txt rpi-gpio --pre
```

- run the test suite
```bash
$ python3 -m unittest discover
```

- install dependencies
```bash
env/bin/pip3 install picamera==1.13
env/bin/pip3 install adafruit-extended-bus==1.0.2
env/bin/pip3 install install adafruit-circuitpython-vl53l0x==3.6.11
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
- `times_to_check_temp`: an average reading is taken for tank/sump temperatures; this is the number of thermometer readings to take to calculate this average
- `overfill_allowance`: an error will be raised when readings are greater than `full_level`, or less than `full_level` minus `water_change_span` minus `overfill_allowance`
- `accuracy_allowance`: laser readings are sanitized, this is a % that describes the upper and lower bounds of the sump levels for which readings should be discarded 
- `level_check_interval`: interval in seconds between sump water height readings during a water-change
- `temp_check_interval`:  interval in seconds between temperature equalization readings as the final step in a water-change
- `temperature_difference_band`: max temperature difference between the tank and sump below which water recirculation can recommence after a water-change
- `water_change_level`: % of sump water to extract when your sump max water height is `full_level`, and empty level is `full_level` minus `water_change_span`


- using the current configuration 
  - logged updates of sump height, sump temp and tank temp will occur every 15 mins
  - water changes will occur 5 times a day at; '09:01', '12:01', '15:01', '18:01', and '21:01'
  
### run the application manually
```bash
$ python3 com/main.py
```

#### run as a service with [systemctl]
 - example configuration file when this project is located at `/home/pi/Documents/Projects/aquarium`
 - add configuration to `/etc/systemd/system/aquarium.service`
```text
[Unit]
Description=aquarium

[Service]
Type=simple
ExecStart=/home/pi/Documents/Projects/aquarium/env/bin/python3 /home/pi/Documents/Projects/aquarium/com/main.py
StandardOutput=append:/home/pi/Documents/Projects/aquarium/logs/log.log
StandardError=append:/home/pi/Documents/Projects/aquarium/logs/log-error.log
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### top-up sump, empty the sump or drain tank by time
```bash
$ env/bin/python3 com/switchScript.py -h
$ env/bin/python3 com/switchScript.py --time <num-seconds> --switch <pump-name>
```
a progress bar will be displayed
![add water log](images/add_water_log.png?raw=true "Add Water Log")

#### example log output
 - `tail -f /home/pi/Documents/Projects/aquarium/logs/log.log`

![tail log output](images/log_output.png?raw=true "Tail Log Output")

### configure log rotation with logrotate
- add the following to `/etc/logrotate.conf`
```bash
/home/pi/Documents/Projects/aquarium/logs/log.log {
    rotate 5
    copytruncate
    notifempty
    compress
    maxsize 100M
    weekly
}
```
### satisfy basic auth
- add a user `username` value and `generate_password_hash(password)` value to the users list in in `config.yaml`
```shell
http -a username:password 192.168.1.14:5000/config | jq '.water_change_times'
http 192.168.1.14:5000/config "Authorization: Basic <base84-encoded-credentials>" | jq '.water_change_times'
```
### update aquarium configuration over the webserver
- set entire aquarium configuration using [httpie][httpie]
```shell
http -a username:password PUT <pi_ip_address>:5000/config Content-Type:application/json @config.json # full configuration json file
```

- get water change times
```shell
http <pi_ip_address>:5000/times
```

- set water change times
```shell
http -a username:password PATCH <pi_ip_address>:5000/times Content-Type:application/json @times.json # :water_change_times": [] json file
http -a username:password PATCH <pi_ip_address>:5000/times Content-Type:application/json water_change_times:=@times_list.json # read from json water_change_times value only file
http -a username:password PATCH <pi_ip_address>:5000/times Content-Type:application/json water_change_times:='["09:01","12:01","15:01"]' # inline json
echo '{"water_change_times": ["09:01", "18:31"]}' | http -a username:password PATCH <pi_ip_address>:5000/times
http 192.168.1.14:5000/config "Authorization: Basic $(echo -ne 'username:password' | base64)" | jq '.water_change_times'

curl -s \
 --header "Authorization: Basic $(echo -ne 'user:pass' | base64)" \
 --header "Content-Type: application/json" \
 --request PATCH \
 --data '{"water_change_times": ["09:01", "12:01"]}' \
  http://pi4.pihole:5000/times
```

[scheduling-library]: https://github.com/dbader/schedule
[unittest]: (https://docs.python.org/3/library/unittest.html)
[side-effects]: https://docs.python.org/3/library/unittest.mock.html#quick-guide
[systemctl]: https://www.liquidweb.com/kb/what-is-systemctl-an-in-depth-overview/
[laser-distance-sensor]: https://www.hobbytronics.co.uk/vl53l0x
[digital-temp-sensor]: https://shop.pimoroni.com/products/ds18b20-programmable-resolution-1-wire-digital-thermometer
[httpie]: https://httpie.io/
