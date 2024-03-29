import socket
from network import LoRa
import ubinascii
import time
import machine

print("starting")
mac = ""
dev_eui = ubinascii.unhexlify(mac)

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('1257279ab3b44855ad3260a6c3123f74')
# mac address of my Pycom, such that the one on IoT lab can also access LoRa
# dev_eui = ubinascii.unhexlify("70b3d5499f3b3b80")
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
while not lora.has_joined():
    time.sleep(1)
    print('Not yet joined...')
print("Joined")

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

sum = 0
readCount = 0
readIntervalSec = 1
reportRate = 10

while True:
    temperature = ((machine.temperature() - 32) / 1.8)
    sum += temperature
    readCount += 1
    if readCount == reportRate:
        message = "avg temp: {} C".format(sum / readCount)
        print(message)
        s.send(str.encode(message))
        sum = 0
        readCount = 0

    time.sleep(readIntervalSec)  # should be 60 seconds
