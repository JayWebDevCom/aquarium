import time
from components.dependencies import VL53L0X 

tof = VL53L0X.VL53L0X()
tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

while True:
    d = tof.get_distance()
    print(d)
    time.sleep(1)
