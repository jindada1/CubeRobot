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
from threading import Thread
from time import sleep

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

        # image
        self.frame = None

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

        # delete last frame to save memory
        self.delete(self.frame)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # must have 'self', otherwise photo will not be shown
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.frame = self.create_image(0, 0, image=self.photo, anchor=NW)


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

    def __init__(self, parent, w=640, h=480):

        Canvas.__init__(self, master=parent, width=w, height=h, bg='white', bd=0, highlightthickness=0)

        self.backim = None
        
        self.width  = w
        self.height = h
        
        self.mask_padding = (10, 10)

        self.maskup()
        self.start_animation()

    # mask on top layer
    def maskup(self, color='green'):

        x1, y1 = self.mask_padding
        x2 = self.width - x1
        y2 = self.height - y1
        w = self.width // 3
        h = self.height // 3

        self.line = ImageTk.PhotoImage(self.gradient_line(x1, y1))
        self.scanline = self.create_image(x1, y1, image=self.line, anchor='nw')

        self.create_line(x1, y1, x1 + w, y1, width=3, fill=color)
        self.create_line(x1, y1, x1, y1 + h, width=3, fill=color)

        self.create_line(x2, y1, x2 - w, y1, width=3, fill=color)
        self.create_line(x2, y1, x2, y1 + h, width=3, fill=color)

        self.create_line(x1, y2, x1 + w, y2, width=3, fill=color)
        self.create_line(x1, y2, x1, y2 - h, width=3, fill=color)

        self.create_line(x2, y2, x2 - w, y2, width=3, fill=color)
        self.create_line(x2, y2, x2, y2 - h, width=3, fill=color)

    def gradient_line(self, x1, y1):
        
        max_alpha = 120
        h = self.height - y1 * 2
        w  = 5

        alpha_gradient = Image.new('L', (1, h), color=0xFF)
        
        for y in range(h):
            a = max_alpha - int(max_alpha * ((y - h/2) / (h/2)) ** 2)
            if a > 0:
                alpha_gradient.putpixel((0, y), a)
            else:
                alpha_gradient.putpixel((0, y), 0)

        alpha = alpha_gradient.resize((w, h))

        line = Image.new('RGBA', (w, h), color="green")
        line.putalpha(alpha)

        return line
    
    def start_animation(self):

        self.th = Thread(target=self.aniloop)
        # protect thread
        self.th.setDaemon(True)
        self.th.start()

    def aniloop(self):
        
        start, y = self.mask_padding
        end = self.width - start
        step = 1
        x = start

        while True:
            x += step

            if x > end or x < start:
                step = -step

            self.coords(self.scanline, x, y)

            sleep(0.006)

    # frame in bottom layer
    def setframe(self, frame):
        if frame is None:
            return

        # delete last image to save memory
        self.delete(self.backim)

        # resize frame to fit screen
        frame = cv2.resize(frame, (self.width, self.height), interpolation = cv2.INTER_AREA)

        # correct color space
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # must have 'self', otherwise photo will not be shown
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.backim = self.create_image(0, 0, image=self.photo, anchor=NW)

        # set to bottom layer
        self.tag_lower(self.backim)
    

class CubeFloorPlan(Canvas):
    '''
        draw floor plan of a rubik's cube
        
        The names of the facelet positions of the cube
                       |--------------|
                       | U1 | U2 | U3 |
                       |--------------|
                       | U4 | U5 | U6 |
                       |--------------|
                       | U7 | U8 | U9 |
                       |--------------|
        |--------------|--------------|--------------|--------------|
        | L1 | L2 | L3 | F1 | F2 | F3 | R1 | R2 | R3 | B1 | B2 | B3 |
        |--------------|--------------|--------------|--------------|
        | L4 | L5 | L6 | F4 | F5 | F6 | R4 | R5 | R6 | B4 | B5 | B6 |
        |--------------|--------------|--------------|--------------|
        | L7 | L8 | L9 | F7 | F8 | F9 | R7 | R8 | R9 | B7 | B8 | B9 |
        |--------------|--------------|--------------|--------------|
                       |--------------|
                       | D1 | D2 | D3 |
                       |--------------|
                       | D4 | D5 | D6 |
                       |--------------|
                       | D7 | D8 | D9 |
                       |--------------|
        
        reference: https://pypi.org/project/kociemba/
    '''

    def __init__(self, parent):

        self.grid_width = sw = 20
        self.padding = pd = 20
        width = 12 * sw + pd
        height = 9 * sw + pd
        Canvas.__init__(self, master=parent, width=width, height=height,
                        bg='white', bd=0, highlightthickness=0)

        self.facelet_id = [[[0 for col in range(3)]
                            for row in range(3)] for face in range(6)]
        
        self.colors = {
            'yellow': 'U',
            'green' : 'R',
            'red'   : 'F',
            'white' : 'D',
            'blue'  : 'L',
            'orange': 'B'
        }
        self.faces = {}
        faces_pos = self.face_position()
        self.draw_faces(faces_pos)

    # init square_id container and left-top coordinate of every face
    def face_position(self):

        ''' 
            initialize six faces
        '''

        anchors = {}
        offsets = ((1, 0), (2, 1), (1, 1), (1, 2), (0, 1), (3, 1))

        for i, (color, flag) in enumerate(self.colors.items()):
            self.faces[color] = [0 for g in range(9)]
            x = 3 * offsets[i][0] * self.grid_width + self.padding // 2
            y = 3 * offsets[i][1] * self.grid_width + self.padding // 2
            anchors[color] = (x, y, flag)
        
        return anchors

    # draw 3 x 3 small squares on 6 faces
    def draw_faces(self, faces_pos):
        
        w = self.grid_width
        for face in faces_pos:
            x, y, flag = faces_pos[face]
            for grid in range(9):
                row = grid // 3
                col = grid % 3
                self.faces[face][grid] = self.drawSquare(x + col * w, y + row * w)

            # set center color of every face
            self.itemconfig(self.faces[face][4], fill=face)
            self.create_text(x + w * 1.5, y + w * 1.5, font=("", 14), text=flag)

    # draw grid_width x grid_width square on (x, y)
    def drawSquare(self, x, y):
        w = self.grid_width
        return self.create_rectangle(x, y, x + w, y + w, fill="whitesmoke", outline="gray")

    # display a face
    def show_face(self, result):

        face = result[4]
        
        for i in range(9):
            self.itemconfig(self.faces[face][i], fill=result[i])


    def definition_string(self):

        '''
            get definition string
            
            A cube definition string "UBL..." means for example: 
                In position U1 we have the U-color, in position U2 we have the B-color, 
                in position U3 we have the L color etc. according to the order
                U1, U2, U3, U4, U5, U6, U7, U8, U9, R1, R2, R3, R4, R5, R6, R7, R8, R9, 
                F1, F2, F3, F4, F5, F6, F7, F8, F9, D1, D2, D3, D4, D5, D6, D7, D8, D9, 
                L1, L2, L3, L4, L5, L6, L7, L8, L9, B1, B2, B3, B4, B5, B6, B7, B8, B9
            
            eg: LUFRUDDBDLFULRUDBRFLFFFDDRLRUBFDDRDBBBRLLRULBLFUBBUURF

            reference: https://pypi.org/project/kociemba/
        '''

        s = ''
        for color, grids in self.faces.items():
            for grid in grids:
                c = self.itemcget(grid, "fill")
                s += self.colors.get(c, '-')
        
        return s

def test():

    from tkinter import Tk

    window = Tk()
    # CubeFloorPlan(window).pack()
    # camera = ViewCanvas(window)
    # camera.pack()
    # camera.openCamera(2)

    canvas = CameraCanvas(window, w=300, h=300)
    canvas.pack()

    window.mainloop()


if __name__ == "__main__":

    test()