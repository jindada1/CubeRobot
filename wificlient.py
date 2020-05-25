'''
    author: kris
    main application of this project
'''

from tkinter import *
from components import *
from sock import EspWifiClient


class App(Window):
    '''
    main gui application of this project
    '''

    def __init__(self, title=None):
        Window.__init__(self, title)

        self.initui()

        # update_func will be executed in loop
        self.update_func = self.update

        # wifi client instance
        self.esp_client = EspWifiClient()
        self.esp_client.wifi_connected = self.device_connected


    def initui(self):

        Left = Frame(self.window)
        Left.pack(side=LEFT, fill=BOTH, expand=True)

        HoverButton(Left, text='连接 esp8266', command=self.connect_device).pack(fill=BOTH, expand=True)
        HoverButton(Left, text='旋转左面',   click=self.rotate, params='L').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='旋转右面',   click=self.rotate, params='R').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='旋转前面',   click=self.rotate, params='F').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='旋转后面',   click=self.rotate, params='B').pack(fill=BOTH, expand=True)

        self.console = Console(self.window, width=40, height=5)
        self.console.pack(side=LEFT, fill=BOTH, expand=True)

    def connect_device(self):

        ssid, pw = ['Rubik-Cube', '1213141516']
        self.console.log('尝试连接 %s, 密码为 %s' % (ssid, pw))
        self.esp_client.connect(ssid, pw)

    def device_connected(self):

        ip = self.esp_client.host
        self.console.log('设备已连接, ip为' + ip, 'success')

    def rotate(self, face):
        self.esp_client.send('/action', {
            'action': '%s1' % face
        })
        self.console.log('旋转 %s 面' % face)

    def update(self):
        pass

if __name__ == "__main__":
    
    App("Wifi client").run()