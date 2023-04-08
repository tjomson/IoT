from network import Bluetooth
import time
import machine
import uhashlib

SERVICE_UUID = uhashlib.sha256("jahksdkasjdbasldiasd").digest()[:16]
CHARACTERISTIC_UUID = uhashlib.sha256(
    "/(IUogiug)8976HJHuweasdjh/T769VYILkpp").digest()[:16]
print('char uuid = {}'.format(CHARACTERISTIC_UUID))

print("starting")
bt = Bluetooth()
# bt.set_advertisement(name='Central', service_uuid=SERVICE_UUID)

print("scanning")
bt.start_scan(-1)
while True:
    adv = bt.get_adv()
    if adv:
        print(bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
        if bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'sink':
            conn = bt.connect(adv.mac)
            print("isConnected: ", conn.isconnected())
            break
    time.sleep(0.5)

for service in conn.services():
    time.sleep(0.050)
    if type(service.uuid()) == bytes:
        print('Reading chars from service = {}'.format(service.uuid()))
    else:
        print("reading chars ", service.uuid())
    chars = service.characteristics()
    for char in chars:
        if (char.properties() & Bluetooth.PROP_WRITE):
            # if (char.read() == b'sink'):
            #     chr = char
            #     svc = service
            print('char {} value = {}'.format(char.uuid(), char.read()))
            chr = char
            svc = service

print("done scanning")
# Get the Bluetooth service and characteristic from the peripheral device
# svc = conn.services()[0]
print(svc.uuid())
# chr = svc.characteristics()[0]
# print(chr.read())
print("isConnected2: ", conn.isconnected())
# Send some data to the peripheral device
while True:
    temperature = ((machine.temperature() - 32) / 1.8)
    message = "avg temp: {} C".format(temperature)
    print('sending: ', message)
    chr.write(message.encode())
    time.sleep(5)

# from network import Bluetooth
# import time
# import uhashlib

# # Define the Bluetooth service and characteristic UUIDs
# SERVICE_UUID = uhashlib.sha256("jahksdkasjdbasldiasd").digest()[:16]
# CHARACTERISTIC_UUID = uhashlib.sha256("fgjrrytj").digest()[:16]

# # Initialize the Bluetooth interface and set the device name
# bt = Bluetooth()
# bt.set_advertisement(name='MyDevice', service_uuid=SERVICE_UUID)

# # Create a GATT server
# srv = bt.service(uuid=SERVICE_UUID, isprimary=True)

# # Add a characteristic to the GATT server with the write property enabled
# chr = srv.characteristic(uuid=CHARACTERISTIC_UUID,
#                          value=None, properties=Bluetooth.PROP_WRITE)

# # Start advertising the Bluetooth service
# bt.advertise(True)

# # Wait for a connection
# while not bt.connected():
#     time.sleep(1)

# # Wait for data to be written to the characteristic
# while True:
#     if bt.connected():
#         value = chr.value()
#         if value:
#             print("Received: ", value)
#             chr.value(None)  # Clear the value to receive more data
#     time.sleep(1)
