import machine
import socket
from network import WLAN
wlan = WLAN(mode=WLAN.STA)

from deepsleep import DeepSleep

ds = DeepSleep()

nets = wlan.scan()
for net in nets:
    if net.ssid == 'sensors':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'n0n53n53'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break


def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
http_get('http://api.openweathermap.org/data/2.5/weather?q=London&appid=1a23339876abc4e92594a29371d0ad2d')
ds.go_to_sleep(10)

#exercise 1
#pycom.heartbeat(False)

#for cycles in range(10): # stop after 10 cycles
#    pycom.rgbled(0x007f00) # green
#    print ('now I am green')
#    time.sleep(5)
#
#    pycom.rgbled(0x7f7f00) # yellow
#    print ('now I am yellow')
#    time.sleep(1.5)

#    pycom.rgbled(0x7f0000)# red
#    print ('now I am red')
#    time.sleep(4)
