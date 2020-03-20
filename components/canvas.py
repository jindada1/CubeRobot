'''
references:
    1. how to display opencv-video-capture-window in tkinter gui
    -> https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window

    2. draw cube floor plan
    -> https://github.com/hkociemba/RubiksCube-TwophaseSolver/blob/master/client_gui.py

'''


import cv2
from tkinter import Canvas, NW
from PIL import Image, ImageTk


class CameraCanvas(Canvas):

    '''
        CameraCanvas can get frames from camera and display on self.

        valid frame size (width x height):
            640 x 480
            352 x 288
            320 x 240
            176 x 144
            160 x 120
    '''

    def __init__(self, parent):

        self.width = 640
        self.height = 480

        Canvas.__init__(self, master=parent, width=self.width, height=self.height,
                        bg='white', bd=0, highlightthickness=0, relief='ridge')

        self.video = None
        self.picture = None

        # 0:nothing, 1:camera, 2:picture
        self.Mode = 0

    # Release the video source when the object is destroyed
    def __del__(self):
        self.closeCamera()

    def openCamera(self, camera_id=0):

        # Open the camera, default 0 is the first camera device on you computer
        self.video = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", camera_id)

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self.Mode = 1

    def closeCamera(self):

        if self.video and self.video.isOpened():
            self.video.release()
            self.Mode = 0

    # get frame of camera
    def frame(self):
        if self.Mode == 1:
            ret, frame = self.video.read()
            return frame if ret else None

        elif self.Mode == 2:
            return self.picture.copy()

    # display camera on canvas
    def refresh(self, frame=None):

        if frame is None:
            # Get a frame from the video source
            frame = self.frame()

        if frame is None:
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # must have 'self', otherwise photo will not be shown
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        
        if self.Mode == 1:
            self.create_image(0, 0, image=self.photo, anchor=NW)
        
        elif self.Mode == 2:
            self.create_image(self.x, self.y, image=self.photo, anchor=NW)

    def add_pic(self, filepath):

        if not filepath:
            return

        self.Mode = 2

        self.picture = self.validate(cv2.imread(filepath))
        self.x = (self.width - self.picture.shape[1]) // 2
        self.y = (self.height - self.picture.shape[0]) // 2

    def validate(self, image, inter = cv2.INTER_AREA):
        
        (h, w) = image.shape[:2]

        # if both the width and height are valid, then return the original image
        if w < self.width and h < self.height:
            return image

        if w > self.width:
            
            h = self.width * (h / w)
            w = self.width

        if h > self.height:
            w = self.height * (w / h)
            h = self.height
        
        # resize the image
        resized = cv2.resize(image, (int(w), int(h)), interpolation = inter)

        # return the resized image
        return resized

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
                        bg='white', bd=0, highlightthickness=0, relief='ridge')

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
                    self.squares[face][row][col] = self.drawSquare(x + row * w, y + col * w)

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

        for i in range(3):
            for j in range(3):
                self.itemconfig(self.squares[face][i][j], fill=result[i][j])


if __name__ == "__main__":

    from tkinter import Tk

    window = Tk()
    CubeFloorPlan(window).pack()
    CameraCanvas(window).pack()
    window.mainloop()
