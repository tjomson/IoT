from network import Bluetooth
import time
import uhashlib

# Define the Bluetooth service and characteristic UUIDs
SERVICE_UUID = uhashlib.sha256("bruhbruhyaQWEassdf89687tyggyki6tTYGY4").digest()[:16]
CHARACTERISTIC_UUID = uhashlib.sha256("/(IUogiug)8976HJHuweasdjh/T769VYILkpp").digest()[:16]

# Define the callback function to handle incoming Bluetooth connections and data


def on_bt_rx(payload):
    print('Received:', payload.decode())

print("starting")
# Initialize the Bluetooth interface and set the device name
bt = Bluetooth()
print("setting adv")
bt.set_advertisement(name='sink', service_uuid=SERVICE_UUID)
print("adv set")

# Define the Bluetooth service and characteristic
svc = bt.service(uuid=SERVICE_UUID, isprimary=True)
chr = svc.characteristic(uuid=CHARACTERISTIC_UUID, value='', properties=Bluetooth.PROP_WRITE)
print("char set")

# Register the callback function to handle incoming data
chr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=on_bt_rx)

# Start advertising the Bluetooth service
print("starting adv")
bt.advertise(True)
print("adv started")

# Wait for incoming Bluetooth connections and data
while True:
    print("sleeping")
    time.sleep(1)

# from network import Bluetooth
# import time
# import uhashlib

# # Define the Bluetooth service and characteristic UUIDs
# SERVICE_UUID = uhashlib.sha256("/(IUogiug)8976HJHuweasdjh/T769VYILkpp").digest()[:16]
# # CHARACTERISTIC_UUID = b'1234567890123457'

# # Initialize the Bluetooth interface and set the device name
# bt = Bluetooth()
# bt.start_scan(-1)
# print("Scanning...")
# while True:
#     adv = bt.get_adv()
#     if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'MyDevice':
#         conn = bt.connect(adv.mac)
#         print("Connected")
#         break
#     time.sleep(0.5)

# # Get the service and characteristic from the server
# srv = conn.services()[0]
# chr = srv.characteristics()[0]

# # Send data to the characteristic
# while True:
#     data = "stuff"
#     chr.write(data)
#     time.sleep(1)