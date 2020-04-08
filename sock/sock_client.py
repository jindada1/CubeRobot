'''
a socket client class that can ->
    connect to host
    receive msg from host
    send msg to host
    disconnect from host
'''
import socket
from time import sleep
from pywifi import PyWiFi
from threading import Thread

class SClient(object):
    '''
        socket client

        callback: 
            - on_recv: will be called when msg received

        methods:
            - detect: scan nearby wifi signals
            - connect: connect to server
            - send: send msg to server
        
        properties:
            - host: server ip
            - port: server port
            - client: socket instance
            - running: listening thread
    '''
    def __init__(self, host='127.0.0.1', port=4396):
        self.host = host
        self.port = port

        # whis func will be called when msg received
        self.on_recv = None

        self.client = None
        self.running = True

    def detect(self):
        wifi = PyWiFi()
        iface = wifi.interfaces()[0]

        iface.scan()
        sleep(5)
        scaners = iface.scan_results()

        for scaner in scaners:
            print("{:<15} {} {} {}".format(scaner.ssid, scaner.bssid, scaner.signal, scaner.freq))

        return scaners

    def connect(self):

        # socket client, socket.AF_INET means IPv4
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        Thread(target=self.__recv).start()

    def send(self, msg):

        if not type(msg) is str:
            msg = str(msg)

        if type(msg) is str:
            msg = msg.encode()

        return self.client.sendall(msg)

    def __recv(self):

        while self.running:

            msg = self.client.recv(1024)
            msg = msg.decode()

            if self.on_recv:
                self.on_recv(msg)

            print(msg)

    def close(self):
        # stop receive loop
        self.running = False

    def __del__(self):

        if self.client:
            self.client.close()

        print('close')

if __name__ == "__main__":
    
    client = SClient()
    client.detect()