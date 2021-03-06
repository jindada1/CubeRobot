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

        self.ssid = None
        self.pw   = None

        # pywifi's interface
        self.iface = PyWiFi().interfaces()[0]
        # all access points nearby
        self._aps = {}

        # this func will be called when wifi connected
        self.wifi_connected = None

    @property
    def nearby(self):
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
            try:
                ssid = scaner.ssid.encode(encoding='raw_unicode_escape', errors='strict').decode()
                
                self._aps[ssid] = {
                    'bssid': scaner.bssid,
                    'signal': scaner.signal,
                    'freq': scaner.freq
                }
            except:
                pass

        return self._aps

    def current_wifi(self):
        b_info = check_output("netsh wlan show interfaces")
        ssid_ = b_info[b_info.find(b'SSID'):]
        b_ssid = ssid_[:ssid_.find(b'\r')]
        ssid = b_ssid.decode('utf8').split()
        return ssid[-1]

    def connect(self, ssid, pw):

        if ssid == self.current_wifi():
            self.__connecting()
            return

        if not ssid in self.nearby.keys():
            if self.wifi_connected:
                self.wifi_connected(False)
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

        self.ssid = ssid
        self.pw   = pw

        Thread(target=self.__connecting, daemon=True).start()

    def __connecting(self):

        while True:
            status = self.iface.status()
            if status == const.IFACE_CONNECTED:
                break
            sleep(.5)

        self.host = self.gateway_ip()

        if self.wifi_connected:
            self.wifi_connected(True)

    def gateway_ip(self, lang='zh'):

        command = 'ipconfig | findstr ' + ('Default Gateway', '默认网关')[lang == 'zh']
        pipe = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)

        line = pipe.stdout.readline()

        if not line:
            return self.gateway_ip('en') if lang == 'zh' else None

        try:
            res = line.decode('gbk').split(":")[-1].split()[0]
        except:
            res = line.decode('gbk')
        
        return res

    def get_url_body(self, params: dict) -> str:

        if not params:
            return ''

        body = '?'
        for key, value in params.items():
            body += str(key) + '=' + str(value) + '&'

        return body[:-1]

    def send(self, route: str, params: dict = {}, retry = False):

        if not self.host:
            print("[x] %s:%s" % (route, str(params)))
            return False
        
        try:
            url = route + self.get_url_body(params)

            client = socket(AF_INET, SOCK_STREAM)
            client.connect((self.host, self.port))

            request = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" % (url, self.host)

            client.sendall(request.encode())

            msg = client.recv(1024).decode('utf-8')
            code = self.http_code(msg)

            return code == '200'

        except:
            
            if retry:
                return False

            if self.ssid and self.pw:
                self.connect(self.ssid, self.pw)

            return False


    def http_code(self, response: str):

        return response.split("\n")[0].split(' ')[1]


if __name__ == "__main__":

    client = EspWifiClient()
    # client.scan_wifi()
    # client.connect('Rubik-Cube', '1213141516')
    # client.send('/wait', {
    #     'time': 3000 
    # })
    # c_wifi = client.current_wifi()
    # client.scan_wifi()
    print(client.nearby.keys())