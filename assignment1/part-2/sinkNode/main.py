from network import Bluetooth
import time

# Define the Bluetooth service and characteristic UUIDs
SERVICE_UUID = b'1234567890123456'
CHARACTERISTIC_UUID = b'1234567890123456'

# Define the callback function to handle incoming Bluetooth connections and data


def on_bt_rx(payload):
    print('Received:', payload.decode())


# Initialize the Bluetooth interface and set the device name
bt = Bluetooth()
bt.set_advertisement(name='Peripherals', service_uuid=SERVICE_UUID)

# Define the Bluetooth service and characteristic
svc = bt.service(uuid=SERVICE_UUID, isprimary=True)
chr = svc.characteristic(uuid=CHARACTERISTIC_UUID, value='')

# Register the callback function to handle incoming data
chr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=on_bt_rx)

# Start advertising the Bluetooth service
bt.advertise(True)

# Wait for incoming Bluetooth connections and data
while True:
    time.sleep(1)
