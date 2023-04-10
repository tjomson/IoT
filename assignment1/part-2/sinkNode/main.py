from network import Bluetooth
from network import LoRa
import time
import uhashlib
import socket
import ubinascii
identifier = 2

mac = "804abcdef0abcdef"
dev_eui = ubinascii.unhexlify(mac)

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
app_eui = ubinascii.unhexlify('0000000000000000')
app_key = ubinascii.unhexlify('1257279ab3b44855ad3260a6c3123f74')
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
while not lora.has_joined():
    time.sleep(1)
    print('Not yet joined...')
print("Joined")

s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# Define the Bluetooth service and characteristic UUIDs
SERVICE_UUID = uhashlib.sha256(
    "bruhbruhyaQWEassdf89687tyggyki6tTYGY4").digest()[:16]
CHARACTERISTIC_UUID = uhashlib.sha256(
    "/(IUogiug)8976HJHuweasdjh/T769VYILkpp").digest()[:16]


def on_bt_rx(gattChar, message):
    mes = message[1].decode()
    s.send(str.encode(mes))
    print('Sink received: ', mes)


print("starting")
# Initialize the Bluetooth interface and set the device name
bt = Bluetooth()
print("setting adv")
bt.set_advertisement(name=f"tjoms_{identifier}", service_uuid=SERVICE_UUID)
print("adv set")

# Define the Bluetooth service and characteristic
svc = bt.service(uuid=SERVICE_UUID, isprimary=True)
chr = svc.characteristic(uuid=10903, value='default',
                         properties=Bluetooth.PROP_WRITE)
print("char set")

# Register the callback function to handle incoming data
chr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=on_bt_rx)

# Start advertising the Bluetooth service
print("starting adv")
bt.advertise(True)
print("adv started")

# Wait for incoming Bluetooth connections and data
while True:
    time.sleep(1)
