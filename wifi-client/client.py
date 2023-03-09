from network import WLAN
import time
import socket
import ssl

# External antenna
wlan = WLAN()
wlan.antenna(WLAN.EXT_ANT)
wlan.connect(ssid='', auth=(WLAN.WPA2, ''))
print('connecting..',end='')

wlan.scan()     # scan for available networks
wlan.connect(ssid='abc123', auth=(WLAN.WPA2, ''))
while not wlan.isconnected():
    time.sleep(1)
    pass
print(wlan.ifconfig())

print('connected')
