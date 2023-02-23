# import time
# import pycom
# from machine import I2C
# from scd30 import SCD30

# i2cbus = I2C(0)
# scd30 = SCD30(i2cbus, 0x61)

# print("starting")

# while True:
#     pycom.rgbled(0x00FF00)  # Green
#     print("loop")
#     # Wait for sensor data to be ready to read (by default every 2 seconds)
#     while scd30.get_status_ready() != 1:
#         print("waiting for data")
#         time.sleep_ms(200)
#     res = scd30.read_measurement()
#     print("stuff")
#     pycom.rgbled(0x0000FF)  # Blue
import pycom
import time
from machine import I2C
from scd30 import SCD30

i2cbus = I2C(2)
scd30 = SCD30(i2cbus, 0x61)

pycom.heartbeat(False)

while True:
    print("loop")
    # pycom.rgbled(0xFF0000)  # Red
    # time.sleep(1)
    # print("hejjjae")
    pycom.rgbled(0x00FF00)  # Green
    time.sleep(1)
    # pycom.rgbled(0x0000FF)  # Blue
    # time.sleep(1)
    while scd30.get_status_ready() != 1:
        print("waiting")
        time.sleep_ms(200)
    res = scd30.read_measurement()
    print("%s %s %s" % res)
