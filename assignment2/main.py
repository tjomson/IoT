import pycom
import time
from machine import I2C
from scd30 import SCD30
from network import LoRa
import ubinascii
import socket
import machine

while True:
    try: 
        i2cbus = I2C(2)  # bus 0 does not work for some reason
        scd30 = SCD30(i2cbus, 0x61)

        pycom.heartbeat(False)

        mac = "804abcdef0abcdef"
        dev_eui = ubinascii.unhexlify(mac)

        lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
        app_eui = ubinascii.unhexlify('0000000000000000')
        # 1257279ab3b44855ad3260a6c3123f74
        # 9C32D2E1F603B786812CBCA37E1C76A0
        app_key = ubinascii.unhexlify('9C32D2E1F603B786812CBCA37E1C76A0')
        lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
        while not lora.has_joined():
            time.sleep(1)
            print('Not yet joined...')
        print("Joined")

        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        while scd30.get_status_ready() != 1:
            time.sleep_ms(200)
        res = scd30.read_measurement()
        mes = "CO2: %s, temp: %s, humidity: %s" % res
        print(mes)
        s.send(str.encode(mes))
        machine.deepsleep(5000)
    except:
        print("failed")
        time.sleep(0.5)
        continue
