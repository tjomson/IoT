from network import LoRa
from machine import I2C
import time
from scd30 import SCD30
import ubinascii
import socket

# My mac is: 70b3d5499f3b3b80
i2c = I2C(2)
scd30 = SCD30(i2c, 0x61)


lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('1257279ab3b44855ad3260a6c3123f74')
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    time.sleep(1)
    print('Not yet joined...')

print("Joined")

# setup socket for connection
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
s.setblocking(False)

s.send("HEJ MOR")
s.send("HEJ MOR") # send twice to make sure it gets through, before antenna turns off

while True:
    s.setblocking(True)
    received = s.recv(10000)
    s.setblocking(False)

    if (len(received) > 0):
        # Wait for sensor data to be ready to read (by default every 2 seconds)
        while scd30.get_status_ready() != 1:
            time.sleep_ms(500)
        ans = scd30.read_measurement()
        
        # convert the answers to byte
        if(received == b'humidity'):
            s.send(str.encode(str(ans[2])))
        elif(received == b'temperature'):   
            s.send(str.encode(str(ans[1])))
        elif(received == b'co2'):
            s.send(str.encode(str(ans[0])))