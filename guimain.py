
import setting
from tkinter import *
from components import Window, Camera, CameraCanvas
import cube_vision as vision


class Controller(Window):
    
    def __init__(self, title=None):
        
        Window.__init__(self, title=title)

        self.initui()

        self.update_func = self.update
    
    def initui(self):

        self.camera = Camera()
        self.camera.open()

        self.canvas = CameraCanvas(self, w=300, h=300)
        self.canvas.pack()
    
    def update(self):

        frame = self.camera.frame()
        vision.sample(frame)
        self.canvas.setframe(a)


if __name__ == "__main__":

    setting.init()

    Controller("Rubik's Cube Robot").run()