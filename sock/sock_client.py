'''
an esp8266 wifi client class that can ->
    connect to esp8266 access point
    receive msg from esp8266 working on AP mode
    send msg to esp8266
'''
from time import sleep
from pywifi import PyWiFi
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class SClient(object):
    '''
        esp8266 wifi client

        callback: 
            - on_recv: will be called when msg received

        methods:
            - detect: scan nearby wifi signals
            - connect: connect to wifi
            - send: send msg to ap server

        properties:
            - host: ip address of access point
            - port: port
    '''

    def __init__(self, host='127.0.0.1', port=80):
        self.host = host
        self.port = port

        # whis func will be called when msg received
        self.on_recv = None

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

        pass

    def local_ip(self):

        pass

    def get_url_body(self, params: dict) -> str:

        if not params:
            return ''

        body = '?'
        for key, value in params.items():
            body += str(key) + '=' + str(value) + '&'

        return body[:-1]

    def send(self, route: str, params: dict = {}):

        url = route + self.get_url_body(params)

        client = socket(AF_INET, SOCK_STREAM)
        client.connect((self.host, self.port))

        request = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" % (url, self.host)
        print(request)

        client.sendall(request.encode())
        Thread(target=self.__recv, args=(client,)).start()

    def __recv(self, client):

        msg = client.recv(1024).decode('utf-8')
        code = self.http_code(msg)

        if self.on_recv:
            self.on_recv(code)

        print(code)

    def http_code(self, response: str):

        return response.split("\n")[0].split(' ')[1]


if __name__ == "__main__":

    client = SClient(host='192.168.4.1')

    for i in range(3):
        client.send('/wait', {
            'time': 1000
        })
        sleep(3)
