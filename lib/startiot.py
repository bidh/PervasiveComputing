from network import LoRa
import socket
import time
import binascii
import pycom
import machine

class Startiot:

    def __init__(self):
        self.dev_eui = binascii.unhexlify("70B3D5499FFD7D50")
        self.app_eui = binascii.unhexlify("70B3D57ED000B952")
        self.app_key = binascii.unhexlify("5C1C7B199BB7438D27C254D59F6EBA00")

        self.lora = LoRa(mode=LoRa.LORAWAN)
    def connect(self, blocking):
        self.lora.join(activation=LoRa.OTAA, auth=(self.app_eui, self.app_key), timeout=0)

        while not self.lora.has_joined():
            print('not joined yet')

        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        # make the socket non-blocking
        self.s.setblocking(blocking)

    def send(self, data):
        self.s.send(data)

    def recv(self, length):
        return self.s.recv(length)
