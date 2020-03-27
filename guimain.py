
import setting
from tkinter import *
from components import *
import cube_vision as vision
from collections import Counter

class Controller(Window):
    
    def __init__(self, title=None):
        Window.__init__(self, title)

        self.initui()

        self.update_func = self.update

        # candidate color of every grid
        self.grids = [Counter() for i in range(9)]

        self.SAMPLE_FRAMES = 50
        self.id = 0
    
    def initui(self):

        self.camera = Camera()
        self.camera.open()

        self.canvas = CameraCanvas(self.window, w=300, h=300)
        self.canvas.pack()

        HoverButton(self.window, text='识别此面', command=self.getcolor).pack(fill=X)

        self.floor = CubeFloorPlan(self.window)
        self.floor.pack()
    
    def update(self):

        frame = self.camera.frame()
        face, image = vision.sample(frame)

        self.canvas.setframe(image)
        self.analyse(face)

    def analyse(self, face):
        
        if not self.id:
            return

        if self.id > 1:
            self.id -= 1
            for i, grid in enumerate(face):
                self.grids[i] += Counter(grid)
        
        else:
            self.id = 0
            face = list(map(lambda C: C.most_common()[0][0], self.grids))
            self.floor.show_face(face)
            s = self.floor.definition_string()
            print(s)
    
    def getcolor(self):
        
        if self.id:
            return

        for i in range(9):
            self.grids[i] = Counter()

        self.id = self.SAMPLE_FRAMES

if __name__ == "__main__":

    setting.init()

    Controller("Rubik's Cube Robot").run()