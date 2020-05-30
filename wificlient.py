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

        self.step_var = IntVar(value=512)
        self.deg_var = IntVar(value=2)
        self.clockwise_var = IntVar(value=-1)

        self.initui()

        # update_func will be executed in loop
        self.update_func = self.update

        # wifi client instance
        self.esp_client = EspWifiClient()
        self.esp_client.wifi_connected = self.device_connected


    def initui(self):
        Top = Frame(self.window)
        Top.pack(side=TOP, fill=BOTH, expand=True)

        Left = Frame(Top)
        Left.pack(side=LEFT, fill=BOTH, expand=True)

        HoverButton(Left, text='旋转左面',   click=self.rotate, params='L').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='旋转右面',   click=self.rotate, params='R').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='旋转前面',   click=self.rotate, params='F').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='旋转后面',   click=self.rotate, params='B').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='拉伸',   click=self.rotate, params='D').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='前后翻转',   click=self.rotate, params='H').pack(fill=BOTH, expand=True)
        HoverButton(Left, text='左右翻转',   click=self.rotate, params='V').pack(fill=BOTH, expand=True)
        mySpinBox(Left, range_=(1, 2), var=self.deg_var, editable=True).pack(fill=BOTH, expand=True)


        self.console = Console(Top, width=60, height=20)
        self.console.pack(side=LEFT, fill=BOTH, expand=True)
        
        Right = Frame(Top)
        Right.pack(side=LEFT, fill=BOTH, expand=True)

        HoverButton(Right, text='L电机', click=self.config, params='L').pack(fill=BOTH, expand=True)
        HoverButton(Right, text='R电机', click=self.config, params='R').pack(fill=BOTH, expand=True)
        HoverButton(Right, text='F电机', click=self.config, params='F').pack(fill=BOTH, expand=True)
        HoverButton(Right, text='B电机', click=self.config, params='B').pack(fill=BOTH, expand=True)
        HoverButton(Right, text='D电机', click=self.config, params='D').pack(fill=BOTH, expand=True)
        mySpinBox(Right, range_=(0, 512), var=self.step_var, editable=True).pack(fill=BOTH, expand=True)

        Bottom = Frame(self.window)
        Bottom.pack(side=TOP, fill=BOTH)

        HoverButton(Bottom, text='连接 esp8266', command=self.connect_device).pack(side=LEFT, fill=BOTH, expand=True)
        Radiobutton(Bottom, text='逆时针', variable=self.clockwise_var, value=-1).pack(side=RIGHT)
        Radiobutton(Bottom, text='顺时针', variable=self.clockwise_var, value=1).pack(side=RIGHT)

    def connect_device(self):

        ssid, pw = ['Rubik-Cube', '1213141516']
        self.console.log('尝试连接 %s, 密码为 %s' % (ssid, pw))
        self.esp_client.connect(ssid, pw)

    def device_connected(self, success):

        if success:
            ip = self.esp_client.host
            self.console.log('设备已连接, ip为' + ip, 'success')
        
        else:
            self.console.log('连接失败')

    def rotate(self, face, deg = 1):
        self.esp_client.send('/action', {
            'face': face,
            'deg': self.deg_var.get(),
            'clockwise': self.clockwise_var.get()
        })
        self.console.log('【动作】面 %s，角 %d，方向 %d' % (face, deg, self.clockwise_var.get()))

    def config(self, face):
        self.esp_client.send('/config', {
            'face': face,
            'steps': self.step_var.get(),
            'clockwise': self.clockwise_var.get()
        })
        self.console.log('【调试】电机 %s，步数 %d，方向 %d' % (face, self.step_var.get(), self.clockwise_var.get()))

    def update(self):
        pass

if __name__ == "__main__":
    
    App("Wifi client").run()