from network import WLAN
import pycom
import socket
import time

pycom.rgbled(0xff0000)
wlan = WLAN()
wlan.init(mode=WLAN.AP, ssid='abc123')
print("hotspot started")
print(wlan.ifconfig(id=1))
pycom.rgbled(0x00ff00)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("192.168.4.1", 80))
serversocket.listen(5)
print("listening")
(clientsocket, address) = serversocket.accept()
print("connected from %s" % str(address))
pycom.rgbled(0x0000ff)

while True:
    clientsocket.send("CO2")
    print("waiting for response")
    response = clientsocket.recv(1024)
    print("request received", response.decode())
    time.sleep(3)
