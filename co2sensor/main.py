import pycom
import time
from machine import I2C
from scd30 import SCD30

i2cbus = I2C(2)  # bus 0 does not work for some reason
scd30 = SCD30(i2cbus, 0x61)

pycom.heartbeat(False)

while True:
    while scd30.get_status_ready() != 1:
        time.sleep_ms(200)
    res = scd30.read_measurement()
    print(" CO2 ppm: %s, temp: %s, humidity: %s" % res)
