'''
    author: kris
    main application of this project
'''

import vision
import setting
from tkinter import *
from components import *
from sock import EspWifiClient
from collections import Counter


class App(Window):
    '''
    main gui application of this project
    '''

    def __init__(self, title=None, controller=False):
        Window.__init__(self, title)

        self.initui()

        # update_func will be executed in loop
        self.update_func = self.update

        # candidate color of every grid
        self.grids = [Counter() for i in range(9)]

        # number of a sample action
        self.batch = 30
        self.sample_id = 0

        # bluetooth window singleton
        self.esp_client = EspWifiClient()
        self.esp_client.wifi_connected = self.device_connected

        # self.finished will be called when task finished
        self.finished = None

    def initui(self):

        self.camera = Camera()
        self.camera.open()

        Top = Frame(self.window)
        Top.pack(fill=BOTH, expand=True)
        Left = Frame(Top)
        Left.pack(side=LEFT, fill=BOTH, expand=True)
        self.canvas = CameraCanvas(Left, w=300, h=300)
        self.canvas.pack(expand=True)

        Control = Frame(Left)
        Control.pack(side=BOTTOM, fill=X)
        HoverButton(Control, text='识别此面', command=self.get_face).pack(fill=X)
        HoverButton(Control, text='连接设备', command=self.connect_device).pack(fill=X)

        Right = Frame(Top)
        Right.pack(side=RIGHT, fill=Y)
        self.floor = CubeFloorPlan(Right)
        self.floor.pack()

        self.console = Console(Right)
        self.console.pack(side=BOTTOM, fill=BOTH, expand=True)

    def connect_device(self):

        ssid, pw = setting.wifi
        self.esp_client.connect(ssid, pw)

    def device_connected(self):

        ip = self.esp_client.host
        self.console.log('设备已连接, ip为' + ip, 'success')

        if self.finished:
            self.finished(ip)

    def update(self):

        frame = self.camera.frame()
        face, image = vision.sample(frame)

        self.canvas.setframe(image)
        self.analyse(face)

    def analyse(self, face):

        if not self.sample_id:
            return

        if self.sample_id > 1:
            self.sample_id -= 1
            for i, grid in enumerate(face):
                self.grids[i] += Counter(grid)

        else:
            self.sample_id = 0
            face = list(map(lambda C: C.most_common()[0][0], self.grids))
            self.floor.show_face(face)
            s = self.floor.definition_string()

            self.console.log(list(map(lambda C: C[0], face)))

            if self.finished:
                self.finished(s)

    def get_face(self):

        if self.sample_id:
            return

        for i in range(9):
            self.grids[i] = Counter()

        self.sample_id = self.batch
        self.console.log("正在识别此面色块...")


if __name__ == "__main__":

    App("Rubik's Cube Robot").run()
