import pycom
import time
import binascii
import socket
from network import LoRa
from machine import UART
from time import sleep
from machine import Pin
from onewire import DS18X20
from onewire import OneWire
from deepsleep import DeepSleep

#ds=DeepSleep()
pycom.heartbeat(False)
class LoRaNetwork:
    def __init__(self):
        global temp
        # Initialize LoRaWAN radio
        self.lora = LoRa(mode=LoRa.LORAWAN)
        # Set network keys
        app_eui = binascii.unhexlify('70B3D57ED000B952')
        app_key = binascii.unhexlify('5C1C7B199BB7438D27C254D59F6EBA00')
        # Join the network
        self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        # Loop until joined
        while not self.lora.has_joined():
            print('Not joined yet...')
        print('Joined')
        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        self.s.setblocking(True)
        self.bytesarraytemp = bytearray(1)

    def convertbytes(self, data):
        self.bytesarraytemp[0] = data
        return self.bytesarraytemp

    def senddata(self):
        waterTemp = temp.read_temp_async()
        temp.start_convertion()
        print(waterTemp)
        if waterTemp:
            self.s.send(self.convertbytes(int(waterTemp)))

if __name__ == '__main__':
    ow = OneWire(Pin('P10'))
    temp = DS18X20(ow)

    lora = LoRaNetwork()
    while(True):
        lora.senddata()
        #time.sleep(60)
        #print('deep sleep started')
        #ds=DeepSleep()
        #ds.go_to_sleep(30)
        #print('deep sleep ended')
