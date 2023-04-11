from network import Bluetooth
import time
import machine
import uhashlib

print("starting")
identifier = 0
bt = Bluetooth()

while True:
    print("scanning")
    bt.start_scan(-1)
    while True:
        adv = bt.get_adv()
        if adv:
            print(bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL))
            # Use name of server to determine which to connect to. Use names like node1, node2... for the chain
            if bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == "tjoms_{}".format(identifier+1):
                while True:
                    try:
                        print("trying", adv.mac)
                        conn = bt.connect(adv.mac)
                        print("isConnected: ", conn.isconnected())
                        break
                    except:
                        continue
                break
        time.sleep(0.05)
    bt.stop_scan()
    time.sleep(1)
    print("scan stopped", bt.isscanning())
    print("checking services")
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
                svc = service
    print("done with services")
    # while True:
    temperature = ((machine.temperature() - 32) / 1.8)
    message = "avg temp: {0} C {1}".format(temperature, identifier)
    print('sending: ', message)
    chr.write(message.encode())
    print("disconnecting")
    conn.disconnect()
    print("isConnected: ", conn.isconnected())
    time.sleep(20)
