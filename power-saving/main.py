from network import LoRa
from machine import I2C, sleep
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

prevSent = 0
command = "undefined"
nextMeasurement = 0

s.send("HEJ MOR")
s.send("HEJ MOR")
s.send("HEJ MOR") # send twice to make sure it gets through, before antenna turns off

# sometimes it does not get the first message even though we block???????
s.setblocking(True)
received = s.recv(10000)
s.setblocking(False)
if (len(received) > 0):
    receivedString = received.decode()
    print("received: " + receivedString)
    command, interval, nextMeasurement = receivedString.split()
    interval = int(interval)
    nextMeasurement = int(nextMeasurement)
    received = b''
print("got it! " + received.decode())

while True:
    print("loop")
        # Wait for sensor data to be ready to read (by default every 2 seconds)
    while scd30.get_status_ready() != 1:
        time.sleep_ms(500)
    ans = scd30.read_measurement()
    print("current reading:", end=" ")
    print(ans)
    print("command: " + command)

    def isWithinInterval(index):
        val = abs(prevSent - float(ans[index])) > interval
        print("isWithinInterval: " + str(val))
        return val
        
        # convert the answers to byte
    toSend = ""
    if(command == 'humidity'):
        if (isWithinInterval(2)):
            toSend = str.encode(str(ans[2]))
            prevSent = ans[2]
    elif(command == 'temperature'):   
        if (isWithinInterval(1)):
            toSend = str.encode(str(ans[1]))
            prevSent = ans[1]
    elif(command == 'co2'):
        if (isWithinInterval(0)):
            toSend = str.encode(str(ans[0]))
            prevSent = ans[0]

    if (toSend != ""):
        print("sending: " + toSend.decode())
        s.setblocking(True)
        s.send(toSend)
        toSend = ""
        s.setblocking(False)
        received = s.recv(10000)
        if (len(received) > 0):
            receivedString = received.decode()
            print("received: " + receivedString)
            command, interval, nextMeasurement = receivedString.split()
            interval = int(interval)
            nextMeasurement = int(nextMeasurement)
            received = b''

    sleep(nextMeasurement * 1000)
