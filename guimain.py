
import setting
from tkinter import *
from components import Window, Camera, CameraCanvas
import cube_vision as vision
from collections import Counter

class Controller(Window):
    
    def __init__(self, title=None):
        
        Window.__init__(self, title)

        self.initui()

        self.update_func = self.update

        # candidate color of every grid
        self.grids = [Counter() for i in range(9)]

        self.id = 50
    
    def initui(self):

        self.camera = Camera()
        self.camera.open()

        self.canvas = CameraCanvas(self.window, w=300, h=300)
        self.canvas.pack()
    
    def update(self):

        frame = self.camera.frame()
        face, image = vision.sample(frame)
        self.canvas.setframe(image)

        if self.id > 0:
            self.id -= 1
            for i, grid in enumerate(face):
                self.grids[i] += Counter(grid)
        
        elif self.id == 0:
            self.id = -1
            print(self.grids)

if __name__ == "__main__":

    setting.init()

    Controller("Rubik's Cube Robot").run()