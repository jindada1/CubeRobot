'''
references:
    1. how to display opencv-video-capture-window in tkinter gui
    -> https://solarianprogrammer.com/2018/04/21/python-opencv-show-video-tkinter-window

    2. draw cube floor plan
    -> https://github.com/hkociemba/RubiksCube-TwophaseSolver/blob/master/client_gui.py

'''
import cv2
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from vision import grab_colors

L_PADDING = 10
S_PADDING = 5


class HoverButton(Button):

    def __init__(self, parent, hover="gainsboro", bg="white", params=None, click=None, **kw):

        if click:
            # pass params to command
            def do():
                click(params)

            Button.__init__(self, master=parent, bg=bg, activebackground="gray", command=do, **kw)

        else:
            Button.__init__(self, master=parent, bg=bg, activebackground="gray", **kw)

        self.hover = hover
        self.background = bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.config(border='0')

    def on_enter(self, e):
        self['background'] = self.hover

    def on_leave(self, e):
        self['background'] = self.background


class CubeFloorPlan(Canvas):

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
            self.create_text(x + w * 1.5, y + w * 1.5, font=("", 14), text=flag, state=DISABLED)

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

        self.canopen = True

        if self.canopen:
            self.openCamera(0)

    # Release the video source when the object is destroyed
    def __del__(self):

        if self.video.isOpened():
            self.video.release()

    def openCamera(self, camera_id=0):

        # Open the camera, default 0 is the first camera device on you computer
        self.video = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", camera_id)

        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

    # get frame of camera
    def frame(self):
        if self.video.isOpened():
            ret, frame = self.video.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)

    # display imae on canvas
    def refresh(self):
        # Get a frame from the video source
        ret, frame = self.frame()

        if ret:
            # must have 'self', otherwise photo will not be shown
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
            self.create_image(0, 0, image=self.photo, anchor=NW)

    def setPic(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(rgb))
        self.create_image(0, 0, image=self.photo, anchor=NW)


class HSVAdjuster(Frame):

    '''
        adjust hsv range of a color, and store in json file 

    '''

    def __init__(self, parent, adjusting=None, toggle=None):

        Frame.__init__(self, master=parent, pady=S_PADDING)

        # current hsv ranges for color segmentation
        self.hsv_range = {
            'Red'   : ([156,  43,  46], [180, 255, 255]), # Red
            'blue'  : ([ 69, 120, 100], [179, 255, 255]), # Blue
            'yellow': ([ 21, 110, 117], [ 45, 255, 255]), # Yellow
            'orange': ([  0, 110, 125], [ 17, 255, 255]), # Orange
            'white' : ([  0,   0, 221], [180,  30, 255]), # White
            'green' : ([ 35,  43,  46], [ 77, 255, 255]), # Green
        }

        self.hsv_space = {
            "h": (0, 180),
            "s": (0, 255),
            "v": (0, 255)
        }

        # bind event, callback when slidding any Scale
        self.adjusting = adjusting

        # bind event, callback when toggle mode
        self.toggle = toggle

        # store Scales' val
        self.lower_vars = [IntVar() for i in range(3)]
        self.upper_vars = [IntVar() for i in range(3)]

        self.initui()

    def initui(self):
        self.visualPanel = self.init_visual_panel()

        self.adjustPanel = self.init_adjust_panel()

        self.visualize()

    def init_visual_panel(self):

        visualPanel = Frame(self)
        
        col1 = Frame(visualPanel)
        col1.pack(side=LEFT, fill=Y, expand=True)
        col2 = Frame(visualPanel)
        col2.pack(side=LEFT, fill=BOTH, expand=True)
        col3 = Frame(visualPanel)
        col3.pack(side=LEFT, fill=BOTH, expand=True)

        Label(col1, text="color").pack()
        Label(col2, text="hsv-lower").pack()
        Label(col3, text="hsv-upper").pack()

        for color, (l, r) in self.hsv_range.items():
            HoverButton(col1, bg=color, text=color, cursor="hand2", params=color, click=self.adjust)\
                .pack(fill=BOTH, expand=True, pady=S_PADDING)
            Label(col2, text=str(l)).pack(fill=Y, expand=True)
            Label(col3, text=str(l)).pack(fill=Y, expand=True)

        return visualPanel

    def init_adjust_panel(self):

        adjustPanel = Frame(self)

        title = Frame(adjustPanel)
        title.pack(fill=X)
        Label(title, text="正在调整颜色: ").pack(side=LEFT)
        self.adj_color = StringVar(title)
        ttk.OptionMenu(title, self.adj_color, "-_-", *self.hsv_range.keys()).pack(side=LEFT, fill=X, expand=True)
        HoverButton(title, text="保存", command=self.save_color).pack(side=LEFT)
        HoverButton(title, text="退出调整", command=self.visualize).pack(side=LEFT)

        content = Frame(adjustPanel)
        content.pack(fill=BOTH, expand=True)
        col1 = Frame(content)
        col1.pack(side=LEFT, fill=Y, expand=True)
        col2 = Frame(content)
        col2.pack(side=LEFT, fill=BOTH, expand=True)
        col3 = Frame(content)
        col3.pack(side=LEFT, fill=BOTH, expand=True)

        Label(col1, text="HSV").pack()
        Label(col2, text="lower").pack()
        Label(col3, text="upper").pack()

        for i, (prop, (l, r)) in enumerate(self.hsv_space.items()):
            Label(col1, text=prop).pack(fill=Y, expand=True)

            Scale(col2, from_=l, to=r, variable=self.lower_vars[i], tickinterval=r, command=self.sliding, \
                orient=HORIZONTAL).pack(fill=Y, expand=True)

            Scale(col3, from_=l, to=r, variable=self.upper_vars[i], tickinterval=r, command=self.sliding, \
                orient=HORIZONTAL).pack(fill=Y, expand=True)

        return adjustPanel

    def adjust(self, color):
        self.adj_color.set(color)

        lower, upper = self.hsv_range[color]
        for i in range(3):
            self.lower_vars[i].set(lower[i])
            self.upper_vars[i].set(upper[i])

        self.visualPanel.pack_forget()
        self.adjustPanel.pack(fill=BOTH, expand=True)

    def visualize(self):
    
        self.adjustPanel.pack_forget()
        self.visualPanel.pack(fill=BOTH, expand=True)

    def sliding(self, e):
        if self.adjusting:
            self.adjusting((
            list(map(lambda var: var.get(), self.lower_vars)),
            list(map(lambda var: var.get(), self.upper_vars))
        ))

    def save_color(self):

        self.hsv_range[self.adj_color.get()] = (
            list(map(lambda var: var.get(), self.lower_vars)),
            list(map(lambda var: var.get(), self.upper_vars))
        )


class App:
    '''
    main gui application of this project
    '''

    def __init__(self, window, title):

        self.window = window
        self.window.title(title)

        # create weigets
        self.init_ui(window)

        # computer vision toggler
        self.isScaning = False

        self.update_delay = 33
        # update_func will be called in update
        self.update_func = None
        # update will be automatically called every {update_delay} milliseconds
        self.update()

        self.window.mainloop()

    def init_ui(self, window):

        Top = Frame(window)
        Top.pack(side=TOP, pady=L_PADDING)

        Left = Frame(Top)
        Left.pack(side=LEFT, fill=Y, padx=L_PADDING)
        self.camera_vision = CameraCanvas(Left)
        self.camera_vision.pack(side=TOP)

        Right = Frame(Top)
        Right.pack(side=RIGHT, fill=Y, padx=L_PADDING)

        RightTop = Frame(Right)
        RightTop.pack(side=TOP)
        self.floorplan = CubeFloorPlan(RightTop)
        self.floorplan.pack()

        RightDown = Frame(Right)
        RightDown.pack(side=BOTTOM, fill=BOTH, expand=True)
        HSVAdjuster(RightDown, toggle=self.hsv_toggle, adjusting=self.hsv_update).pack(fill=BOTH, expand=True)
        HoverButton(RightDown, text="Start", command=self.toggle_vision).pack(fill=X)

        Bottom = Frame(window, bg='white')
        Bottom.pack(side=BOTTOM, fill=X)
        self.Statuslabel = Label(Bottom, text='(づ￣ 3￣)づ', bg='white')
        self.Statuslabel.pack(side=LEFT, padx=L_PADDING)

    def toggle_vision(self):
        self.isScaning = not self.isScaning

        if self.isScaning:
            self.update_func = self.get_cube_color
            self.status('正在扫描魔方')
        else:
            self.update_func = None
            self.status('使用摄像头中')

    def get_cube_color(self):
        ret, frame = self.camera_vision.frame()
        result, frame = grab_colors(frame)
        self.camera_vision.setPic(frame)
        if result[0]:
            self.floorplan.showResult(result[1])

    def hsv_update(self, args):
        print(args)
        
    def hsv_toggle(self, **args):
        print(args)

    def status(self, string):

        self.Statuslabel.configure(text=string)

    def update(self):

        if self.update_func:
            self.update_func()

        else:
            self.camera_vision.refresh()

        self.window.after(self.update_delay, self.update)


if __name__ == "__main__":

    App(Tk(), "Cube Robot")
