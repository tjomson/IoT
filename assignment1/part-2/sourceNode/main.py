from network import Bluetooth
import time
import machine

# Define the Bluetooth service and characteristic UUIDs
SERVICE_UUID = 'f0c5ff12-0147-44c8-8a7a-ef0a61e7d7e0'
CHARACTERISTIC_UUID = 'b722bf9b-7a2a-43c7-b3e3-3ab3657a183f'

# Define the callback function to handle incoming Bluetooth connections and data


def on_bt_rx(payload):
    print('Received:', payload.decode())


# Initialize the Bluetooth interface and set the device name
bt = Bluetooth()
bt.set_advertisement(name='Central', service_uuid=SERVICE_UUID)

# Connect to the peripheral device
bt.start_scan(-1)
while True:
    adv = bt.get_adv()
    if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_SERVICE_UUIDS_COMPLETE)[0] == SERVICE_UUID:
        print('Peripheral found!')
        conn = bt.connect(adv.mac)
        break
    time.sleep(0.1)

# Get the Bluetooth service and characteristic from the peripheral device
svc = conn.services()[0]
chr = svc.characteristics()[0]

# Register the callback function to handle incoming data
chr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=on_bt_rx)

# Send some data to the peripheral device

# Wait for incoming Bluetooth data
while True:
    temperature = ((machine.temperature() - 32) / 1.8)
    message = "avg temp: {} C".format(temperature)
    chr.write('Hello, Peripheral!')
    time.sleep(10)
