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

    def __init__(self, title=None, controlled=False):
        Window.__init__(self, title)

        # whether controlled by thread
        self.controlled = controlled

        # update_func will be executed in loop
        self.update_func = self.update

        # candidate color of every grid
        self.grids = [Counter() for i in range(9)]

        # number of a sample action
        self.batch = 30
        self.sample_id = 0

        # wifi client instance
        self.esp_client = EspWifiClient()
        self.esp_client.wifi_connected = self.device_connected

        # self.message is the chanel to send message to controller thread
        self.message = None
        
        self.initui()

    @property
    def cube_str(self):
        return self.floor.definition_string()

    def initui(self):

        self.camera = Camera()
        self.camera.open()

        Top = Frame(self.window)
        Top.pack(fill=BOTH, expand=True)
        Left = Frame(Top, bg='white')
        Left.pack(side=LEFT, fill=Y)
        self.canvas = CameraCanvas(Left, w=300, h=300)
        self.canvas.pack(expand=True)
        self.floor = CubeFloorPlan(Left)
        self.floor.pack()

        Mid = Frame(Top)
        Mid.pack(side=LEFT, fill=BOTH, padx=5, expand=True)
        self.console = Console(Mid, width=40)
        self.console.pack(fill=BOTH, expand=True)

        Control = Frame(Mid)
        Control.pack(side=BOTTOM, fill=X)
        HoverButton(Control, text='识别此面', command=self.get_face).pack(fill=X)
        HoverButton(Control, text='连接esp8266', command=self.connect_device).pack(fill=X)
        if self.controlled:
            HoverButton(Control, text='暂停任务', click=self.to_controller, params='pause').pack(fill=X)

        Right = Frame(Top)
        Right.pack(side=RIGHT, fill=Y)
        ControlPanel(Right, esp_client=self.esp_client, sending=self.sending_msg).pack(fill=BOTH, expand=True)

    def sending_msg(self, s):
        self.console.log(s)

    def connect_device(self):

        ssid, pw = setting.wifi
        self.esp_client.connect(ssid, pw)

    def device_connected(self, success):

        if success:
            ip = self.esp_client.host
            self.console.log('设备已连接, ip为' + ip, 'success')
        
        else:
            self.console.log('连接失败')

        if self.controlled:
            self.message('finish', success)

    def to_controller(self, action):
        
        if self.message:
            self.message(action)

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
            self.console.log(list(map(lambda C: C[0], face)))

            if self.controlled:
                self.message('finish')

    def get_face(self):

        if self.sample_id:
            return

        for i in range(9):
            self.grids[i] = Counter()

        self.sample_id = self.batch
        self.console.log("正在识别此面色块...")


if __name__ == "__main__":

    App("Rubik's Cube Robot").run()
