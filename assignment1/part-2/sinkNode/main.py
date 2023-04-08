from network import Bluetooth
import time
import uhashlib

# Define the Bluetooth service and characteristic UUIDs
SERVICE_UUID = uhashlib.sha256(
    "bruhbruhyaQWEassdf89687tyggyki6tTYGY4").digest()[:16]
CHARACTERISTIC_UUID = uhashlib.sha256(
    "/(IUogiug)8976HJHuweasdjh/T769VYILkpp").digest()[:16]

# Define the callback function to
# handle incoming Bluetooth connections and data


def on_bt_rx(gattChar, message):
    print('Received: ', message[1].decode())


print("starting")
# Initialize the Bluetooth interface and set the device name
bt = Bluetooth()
print("setting adv")
bt.set_advertisement(name='sink', service_uuid=SERVICE_UUID)
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
