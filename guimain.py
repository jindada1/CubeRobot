'''
    author: kris
    main application of this project
'''

import vision
import setting
from tkinter import *
from components import *
from collections import Counter

class Client(Window):
    
    def __init__(self, title=None, controller=None):
        Window.__init__(self, title)

        self.initui()

        # update_func will be executed in loop
        self.update_func = self.update

        # candidate color of every grid
        self.grids = [Counter() for i in range(9)]

        # number of a sample action
        self.SAMPLE_FRAMES = 10
        self.sample_id = 0

        # bluetooth window singleton
        self.bluetooth_win = None
        
        self.onclose = None
        self.window.protocol("WM_DELETE_WINDOW", self.close)

    
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
        HoverButton(Control, text='蓝牙', command=self.open_bluetooth).pack(fill=X)

        Right = Frame(Top)
        Right.pack(side=RIGHT, fill=Y)
        self.floor = CubeFloorPlan(Right)
        self.floor.pack()

        self.console = Console(Right)
        self.console.pack(side=BOTTOM, fill=BOTH, expand=True)

    def open_bluetooth(self):
        
        if self.bluetooth_win is None:
            self.bluetooth_win = SubWindow(self.window)
        
        self.bluetooth_win.open()

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
    
    def get_face(self):
        
        if self.sample_id:
            return

        for i in range(9):
            self.grids[i] = Counter()

        self.sample_id = self.SAMPLE_FRAMES
    
    def close(self):

        if self.onclose:
            self.onclose()

        self.window.destroy()

if __name__ == "__main__":

    Client("Rubik's Cube Robot").run()