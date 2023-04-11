from network import Bluetooth
import time
import uhashlib


print("starting")
identifier = 1

bt = Bluetooth()

print("setting adv")
SERVICE_UUID = uhashlib.sha256(
    "gsghrsyksvb45676ryj5768").digest()[:16]
bt.set_advertisement(name="tjoms_{}".format(
    identifier), service_uuid=SERVICE_UUID)

svc = bt.service(uuid=SERVICE_UUID, isprimary=True)
myChr = svc.characteristic(uuid=10904, value='default2',
                           properties=Bluetooth.PROP_WRITE)


def on_bt_rx(gattChar, message):
    mes = message[1].decode()
    print('transfer received: ', mes)
    bt.advertise(False)
    bt.start_scan(-1)
    conn_set = False
    while not conn_set:
        print("looping")
        adv_list = bt.get_advertisements()
        for adv in adv_list:
            if bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == "tjoms_{}".format(identifier+1):
                while True:
                    try:
                        print("trying", adv.mac)
                        conn = bt.connect(adv.mac)
                        print("isConnected: ", conn.isconnected())
                        conn_set = True
                        break
                    except:
                        continue
                break
        time.sleep(0.1)

    bt.stop_scan()
    time.sleep(1)
    for service in conn.services():
        time.sleep(0.050)
        print("service loop")
        if type(service.uuid()) == bytes:
            print('Reading chars from service = {}'.format(service.uuid()))
        else:
            print("reading chars ", service.uuid())
        chars = service.characteristics()
        for char in chars:
            if (char.properties() & Bluetooth.PROP_WRITE):
                print('char {} value = {}'.format(char.uuid(), char.read()))
                chr = char
    print("transfer {0} sending {1}".format(identifier, mes))
    chr.write("{0} {1}".format(mes, identifier).encode())
    conn.disconnect()
    bt.advertise(True)


myChr.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=on_bt_rx)
bt.advertise(True)
print("advertising")
print("isScanning:", bt.isscanning())
while True:
    time.sleep(1)
