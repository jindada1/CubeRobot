'''
an esp8266 wifi client class that can ->
    connect to esp8266 access point
    receive msg from esp8266 working on AP mode
    send msg to esp8266
'''
from time import sleep
from threading import Thread
from pywifi import PyWiFi, Profile, const
from socket import socket, AF_INET, SOCK_STREAM
from subprocess import Popen, check_output, PIPE



class EspWifiClient(object):
    '''
        esp8266 wifi client

        callback:
            - wifi_connected: will be called when wifi connected

        methods:
            - scan_wifi: scan_wifi nearby wifi signals
            - connect: connect to wifi
            - send: send msg to ap server

        properties:
            - host: ip address of access point
            - port: port
            - aps: all access points detected nearby
    '''

    def __init__(self, host=None, port=80):
        self.host = host
        self.port = port

        # pywifi's interface
        self.iface = PyWiFi().interfaces()[0]
        # all access points nearby
        self._aps = {}

        # this func will be called when wifi connected
        self.wifi_connected = None

    @property
    def aps(self):
        if not self._aps:
            self.scan_wifi()
        return self._aps

    def scan_wifi(self):
        self.iface.scan()
        sleep(1)
        scaners = self.iface.scan_results()

        for scaner in scaners:
            if not scaner.ssid:
                continue
            self._aps[scaner.ssid] = {
                'bssid': scaner.bssid,
                'signal': scaner.signal,
                'freq': scaner.freq
            }

        self.display_aps()
        return self._aps

    def current_wifi(self):
        wow = check_output("netsh wlan show interfaces")
        print(wow)
        return wow.decode('gbk')

    def display_aps(self):
        for name, data in self._aps.items():
            print("{:<15} {} {} {}".format(name, data['bssid'], data['signal'], data['freq']))

    def connect(self, ssid, pw):
        if ssid in self.current_wifi():
            self.__connecting()
            print('already connected', ssid)
            return

        profile = Profile()
        profile.key = pw
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.akm.append(const.AKM_TYPE_WPA2PSK)

        # self.iface.remove_all_network_profiles()
        tmp_profile = self.iface.add_network_profile(profile)

        self.iface.connect(tmp_profile)
        Thread(target=self.__connecting, daemon=True).start()

    def __connecting(self):

        while True:
            status = self.iface.status()
            if status == const.IFACE_CONNECTED:
                break
            sleep(.5)

        self.host = self.gateway_ip()
        # print('wifi connected, gateway ip is', self.host)

        if self.wifi_connected:
            self.wifi_connected()

    def gateway_ip(self, lang='zh'):
        
        command = 'ipconfig | findstr ' + ('Default Gateway', '默认网关')[lang == 'zh']
        pipe = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)

        line = pipe.stdout.readline()

        if not line:
            return self.gateway_ip('en') if lang == 'zh' else None

        return line.decode('gbk').split(":")[-1].split()[0]

    def get_url_body(self, params: dict) -> str:

        if not params:
            return ''

        body = '?'
        for key, value in params.items():
            body += str(key) + '=' + str(value) + '&'

        return body[:-1]

    def send(self, route: str, params: dict = {}):

        if not self.host:
            raise Exception("no host")

        url = route + self.get_url_body(params)

        client = socket(AF_INET, SOCK_STREAM)
        client.connect((self.host, self.port))

        request = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" % (url, self.host)

        client.sendall(request.encode())

        msg = client.recv(1024).decode('utf-8')
        code = self.http_code(msg)
        
        return code == '200'

    def http_code(self, response: str):

        return response.split("\n")[0].split(' ')[1]


if __name__ == "__main__":

    client = EspWifiClient()
    # client.scan_wifi()
    # client.connect('Rubik-Cube', '1213141516')
    # client.send('/wait', {
    #     'time': 3000
    # })
    client.current_wifi()