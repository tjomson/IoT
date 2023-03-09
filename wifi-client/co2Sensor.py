import time
from machine import I2C, Pin
from scd30 import SCD30


class scd30_data:
    def __init__(self):
        i2cbus = I2C(0, I2C.MASTER, baudrate=1000)
        self.scd30 = SCD30(i2cbus, 0x61)

    def initialize(self):
        while self.scd30.get_status_ready() != 1:
            time.sleep_ms(200)

    def get_co2(self):
        c02, _, _ = self._measure()
        return c02

    def get_temp(self):
        _, temp, _ = self._measure()
        return temp

    def get_rh(self):
        _, _, rh = self._measure()
        return rh

    def _measure(self):
        while self.scd30.get_status_ready() != 1:
            time.sleep_ms(200)
        co2, temp, rh = self.scd30.read_measurement()
        return co2, temp, rh
