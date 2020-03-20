
from tkinter import ttk
from tkinter import *

from components import *
from vision import grab_colors
import setting as st

class App:
    '''
    main gui window of this project
    '''

    def __init__(self, title):

        self.window = Tk()
        self.window.title(title)

        # create weigets
        self.init_ui(self.window)

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
        Top.pack(side=TOP, pady=st.L_PADDING)

        Left = Frame(Top)
        Left.pack(side=LEFT, fill=Y, padx=st.L_PADDING)
        self.camera_vision = CameraCanvas(Left)
        self.camera_vision.pack(side=TOP)

        Right = Frame(Top)
        Right.pack(side=RIGHT, fill=Y, padx=st.L_PADDING)

        RightTop = Frame(Right)
        RightTop.pack(side=TOP)
        self.floorplan = CubeFloorPlan(RightTop)
        self.floorplan.pack()

        RightDown = Frame(Right)
        RightDown.pack(side=BOTTOM, fill=BOTH, expand=True)
        HSVAdjuster(RightDown, toggle=self.hsv_toggle, adjusting=self.hsv_update, save=self.hsv_save) \
            .set_hsv_range(st.hsv_range) \
            .pack(fill=BOTH, expand=True)

        HoverButton(RightDown, text="Start", command=self.toggle_vision).pack(fill=X)

        Bottom = Frame(window, bg='white')
        Bottom.pack(side=BOTTOM, fill=X)
        self.Statuslabel = Label(Bottom, text='(づ￣ 3￣)づ', bg='white')
        self.Statuslabel.pack(side=LEFT, padx=st.L_PADDING)

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

    def hsv_save(self, item):
        st.hsv_range[item[0]] = item[1]
        st.store()

    def hsv_update(self, args):
        print(args)
        
    def hsv_toggle(self):
        print('toggle')

    def status(self, string):

        self.Statuslabel.configure(text=string)

    def update(self):

        if self.update_func:
            self.update_func()

        else:
            self.camera_vision.refresh()

        self.window.after(self.update_delay, self.update)


if __name__ == "__main__":

    st.init()

    App('test')