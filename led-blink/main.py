import pycom
import time
import machine
from machine import Pin
pycom.heartbeat(False)

# wake_pin = Pin('P11', mode=Pin.IN, pull=Pin.PULL_UP)
# machine.pin_sleep_wakeup([wake_pin], machine.WAKEUP_ALL_LOW, enable_pull=True)

# while True:
pycom.rgbled(0x880000)  # Red
time.sleep(1)
pycom.rgbled(0x008800)  # Green
time.sleep(1)
pycom.rgbled(0x000088)  # Blue
time.sleep(1)

machine.deepsleep(5000)
