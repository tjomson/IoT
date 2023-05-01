while True:
    print("trying")
    try: 
        import pycom
        import time
        from machine import I2C
        from scd30 import SCD30
        from network import LoRa
        import ubinascii
        import socket
        import machine

        i2cbus = I2C(2)  # bus 0 does not work for some reason
        scd30 = SCD30(i2cbus, 0x61)

        pycom.heartbeat(False)

        mac = "809ABCDEF0ABCDEF"
        dev_eui = ubinascii.unhexlify(mac)

        lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
        app_eui = ubinascii.unhexlify('0000000000000000')
        # 1257279ab3b44855ad3260a6c3123f74
        # 9C32D2E1F603B786812CBCA37E1C76A0 for 804
        # C7FB9C5899356C770662E3C9E0742D13 for 809
        app_key = ubinascii.unhexlify('C7FB9C5899356C770662E3C9E0742D13')
        lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
        while not lora.has_joined():
            time.sleep(1)
            print('Not yet joined...')
        print("Joined")

        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        while scd30.get_status_ready() != 1:
            print("not ready")
            time.sleep_ms(200)
        res = scd30.read_measurement()
        mes = "%s, %s, %s" % res # CO2, temp, humi
        print(mes)
        s.send(str.encode(mes))
        machine.deepsleep(945000) # 14 min, 45 sec
        # machine.deepsleep(25000) # 14 min, 45 sec
    except:
        print("failed")
        time.sleep(0.5)
        continue
