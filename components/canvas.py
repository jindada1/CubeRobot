'''
references:
    1. how to display opencv-video-capture-window in tkinter gui
    -> https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window

    2. draw cube floor plan
    -> https://github.com/hkociemba/RubiksCube-TwophaseSolver/blob/master/client_gui.py

'''
try:
    from . import Camera
except:
    from video import Camera

import cv2
from tkinter import Canvas, NW
from PIL import Image, ImageTk

class ViewCanvas(Canvas):

    def __init__(self, parent):
        self.width = 640
        self.height = 480
        self.white = [255, 255, 255]

        Canvas.__init__(self, master=parent, width=self.width, height=self.height,
                        bg='white', bd=0, highlightthickness=0)

        # Open the camera, default 0 is the first camera device on you computer
        self.camera = Camera(w=self.width, h=self.height)
        self.picture = None

        # 0:nothing, 1:camera, 2:picture
        self.Mode = 0

    def open_camera(self):
        self.camera.open()
        self.Mode = 1

    def close_camera(self):
        self.camera.close()
        self.Mode = 0

    # get frame in screen
    def screen(self):
        if self.Mode == 1:
            return self.camera.frame()

        elif self.Mode == 2:
            return self.picture.copy()

    # display frame on canvas
    def refresh(self, frame=None):
        if frame is None:
            # Get a frame from the video source
            frame = self.screen()

        if frame is None:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # must have 'self', otherwise photo will not be shown
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.create_image(0, 0, image=self.photo, anchor=NW)

    def addpic(self, filepath):
        if not filepath:
            return

        if self.Mode == 1:
            self.close_camera()
            
        self.picture = self.validate(cv2.imread(filepath))
        self.Mode = 2

    def validate(self, image):

        (h, w) = image.shape[:2]

        if w > self.width:
            h = int(self.width * (h / w))
            w = self.width

        if h > self.height:
            w = int(self.height * (w / h))
            h = self.height
        
        # resize the image
        resized = cv2.resize(image, (w, h), interpolation = cv2.INTER_AREA)

        top = (self.height - h) // 2
        bottom = self.height - h - top

        left = (self.width - w) // 2
        right = self.width - w - left

        # padding image
        image = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=self.white)
        
        return image


class CameraCanvas(Canvas):

    def __init__(self, parent, w=200, h=200):

        Canvas.__init__(self, master=parent, width=w, height=h, bg='white', bd=0, highlightthickness=0)

    # 设置 frame 在底层
    def setframe(self, frame):
        if frame is None:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # must have 'self', otherwise photo will not be shown
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.create_image(0, 0, image=self.photo, anchor=NW)


class CubeFloorPlan(Canvas):
    '''
        draw floor plan of a rubik's cube
    '''

    def __init__(self, parent):

        self.square_width = sw = 20
        self.padding = pd = 20
        width = 12 * sw + pd
        height = 9 * sw + pd
        Canvas.__init__(self, master=parent, width=width, height=height,
                        bg='white', bd=0, highlightthickness=0)

        self.facelet_id = [[[0 for col in range(3)]
                            for row in range(3)] for face in range(6)]

        self.squares, anchors = self.initSquares()
        self.drawSquares(anchors)

    # init square_id container and left-top coordinate of every face
    def initSquares(self):
        ''' initialize six faces '''
        squares = {}
        anchors = {}
        colors = ("yellow", "green", "red", "white", "blue", "orange")
        offsets = ((1, 0), (2, 1), (1, 1), (1, 2), (0, 1), (3, 1))
        flags = ("U", "R", "F", "D", "L", "B")

        for i in range(6):
            squares[colors[i]] = [[0 for col in range(3)]for row in range(3)]
            x = 3 * offsets[i][0] * self.square_width + self.padding // 2
            y = 3 * offsets[i][1] * self.square_width + self.padding // 2
            anchors[colors[i]] = (x, y, flags[i])

        return squares, anchors

    # draw 3 x 3 small squares on 6 faces
    def drawSquares(self, anchors):
        # print(anchors)
        w = self.square_width
        for face in anchors:
            x, y, flag = anchors[face]
            for row in range(3):
                for col in range(3):
                    self.squares[face][row][col] = self.drawSquare(x + col * w, y + row * w)

            # set center color of every face
            self.itemconfig(self.squares[face][1][1], fill=face)
            self.create_text(x + w * 1.5, y + w * 1.5, font=("", 14), text=flag)

    # draw square_width x square_width square on (x, y)
    def drawSquare(self, x, y):
        w = self.square_width
        return self.create_rectangle(x, y, x + w, y + w, fill="whitesmoke", outline="gray")

    # display a face
    def showResult(self, result):

        face = result[1][1]
        try:
            for i in range(3):
                for j in range(3):
                    self.itemconfig(self.squares[face][i][j], fill=result[i][j])
        except:
            pass


if __name__ == "__main__":

    from tkinter import Tk

    window = Tk()
    CubeFloorPlan(window).pack()
    # camera = CameraCanvas(window)
    # camera.pack()
    # camera.openCamera(2)
    window.mainloop()
