from network import Bluetooth
import time
import machine
import uhashlib


identifier = 1

print("starting")
bt_out = Bluetooth()

print("scanning")
bt_out.start_scan(-1)
while True:
    adv = bt_out.get_adv()
    if adv:
        print(bt_out.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
        # Use name of server to determine which to connect to. Use names like node1, node2... for the chain
        if bt_out.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == f"tjoms_{identifier+1}":
            conn = bt_out.connect(adv.mac)
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
            print('char {} value = {}'.format(char.uuid(), char.read()))
            nextChr = char
            # svc = service

print("setting adv")
bt_in = Bluetooth()
SERVICE_UUID = uhashlib.sha256(
    "gsghrsyksvb45676ryj5768").digest()[:16]
bt_in.set_advertisement(name=f"tjoms_{identifier}", service_uuid=SERVICE_UUID)

svc = bt_in.service(uuid=SERVICE_UUID, isprimary=True)
myChr = svc.characteristic(uuid=10904, value='default2',
                           properties=Bluetooth.PROP_WRITE)


def on_bt_rx(gattChar, message):
    mes = message[1].decode()
    nextChr.write(mes.encode())
    print('transfer received: ', mes)


myChr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=on_bt_rx)
bt_in.advertise(True)
print("advertising")
while True:
    time.sleep(2)
