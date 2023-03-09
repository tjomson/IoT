#!/usr/bin/env python3
#
import pycom
import time

from network import WLAN
import socket
import ssl
from co2Sensor import scd30_data

ADDRESS = "192.168.4.1"
PORT = 80

pycom.heartbeat(False)

# External antenna
wlan = WLAN(mode= WLAN.STA)
# wlan.ifconfig(id=1, config=('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
wlan.antenna(WLAN.EXT_ANT)

print('connecting..',end='')

wlan.scan()     # scan for available networks
wlan.connect(ssid='abc123', auth=(WLAN.WPA2, ''))
while not wlan.isconnected():
    time.sleep(1)
    pass

print('Connected')
print(wlan.ifconfig())

print("Creating socket connection")
while True:
    try :
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("222...")
        s.connect((ADDRESS, PORT))
        print("333")
        break
    except:
        print("failed")
        time.sleep(2)
        continue
print("444")
scd30_measurer = scd30_data()

while True:
    pycom.rgbled(0x777777) # whie?
    recv = s.recv(1024)
    print(recv)
    print(type(recv))
    recv = recv.upper()
    # CHANGE TO IF :( :( :(

    if recv == b"CO2":
        data = scd30_measurer.get_co2()
    elif recv == b"TEMPERATURE":
        data = scd30_measurer.get_temp()
    elif recv == b"HUMIDITY":
        data = scd30_measurer.get_RH()
    else:
        data = "ERROR: Does not support " + str(recv)
    print("Sending data...")
    print(data)
    s.send(str(data))

    pycom.rgbled(0x7f7f00) # yellow
    print("Data sent")
    time.sleep(3)

print("Closing connection..")

s.close()
wlan.disconnect()

if not wlan.isconnected(): 
    pycom.rgbled(0x7f0000) # red
else:
    pycom.rgbled(0x007f00) # Green

