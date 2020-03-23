
from tkinter import ttk, filedialog
from tkinter import *

from components import *
# from vision import grab_colors
from cube_vision import hsv_range_mask, scan_cube, count_sample_points
import setting as st

class App:
    '''
    main gui window of this project
    '''

    def __init__(self, title):

        self.window = Tk()
        self.window.title(title)

        # cube scaning toggler
        self.scaning = False
        self.scan_modes = [('自动定位魔方', 'a'), ('手动定位', 'm')]
        self.last_scan_mode = 'm'
        self.scan_mode = StringVar(value=self.last_scan_mode)

        # hsv color filter range
        self.hsv_mask_range = None

        # status text
        self.status_var = StringVar(self.window)
        # video button text
        self.video_texts = ['开启摄像头', '关闭摄像头']
        self.video_btn_var = StringVar(self.window, value=self.video_texts[0])
        # scan button text
        self.scan_texts = ['扫描魔方', '停止扫描']
        self.scan_btn_var = StringVar(self.window, value=self.scan_texts[0])

        # create weigets
        self.init_ui(self.window)
        # set setting data to widgets
        self.load_setting()
        
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
        self.media_canvas = CameraCanvas(Left)
        self.media_canvas.pack()
        mediaMode = Frame(Left)
        mediaMode.pack(fill=X)
        for text, mode in self.scan_modes:
            Radiobutton(mediaMode, text=text, variable=self.scan_mode, value=mode, command=self.scan_mode_change)\
                .pack(side=LEFT)

        Right = Frame(Top)
        Right.pack(side=RIGHT, fill=Y, padx=st.L_PADDING)

        RightTop = Frame(Right)
        RightTop.pack(side=TOP)
        self.floorplan = CubeFloorPlan(RightTop)
        self.floorplan.pack()

        RightDown = Frame(Right)
        RightDown.pack(side=BOTTOM, fill=BOTH, expand=True)
        Adjuster = Frame(RightDown)
        Adjuster.pack(fill=BOTH, expand=True)
        HoverButton(RightDown, textvariable=self.video_btn_var, command=self.toggle_camera) \
            .pack(side=LEFT, fill=X, expand=True)
        Label(RightDown).pack(side=LEFT)
        HoverButton(RightDown, text="打开图片", command=self.open_photo).pack(side=LEFT, fill=X, expand=True)
        Label(RightDown).pack(side=LEFT)
        HoverButton(RightDown, textvariable=self.scan_btn_var, command=self.toggle_scan) \
            .pack(side=LEFT, fill=X, expand=True)
        
        self.hsv_adjuster = HSVAdjuster(Adjuster, toggle=self.hsv_toggle, adjusting=self.hsv_update, save=self.hsv_save)
        self.sample_adjuster = SampleAdjuster(Adjuster, adjusting=self.resample, save=st.store)
        self.sample_adjuster.pack(fill=BOTH, expand=True)

        Bottom = Frame(window, bg='white')
        Bottom.pack(side=BOTTOM, fill=X)
        Label(Bottom, textvariable=self.status_var, bg='white').pack(side=LEFT, padx=st.L_PADDING)

    def load_setting(self):
        
        self.hsv_adjuster.set_hsv_range(st.hsv_ranges)

        width_height = (self.media_canvas.width, self.media_canvas.height)
        color_hsv = (st.h_ranges, st.s_divide, st.v_ranges)
        self.sample_adjuster.set_data(st.sample, width_height, color_hsv)

    def scan_mode_change(self):

        mode = self.scan_mode.get()
        if self.last_scan_mode == mode:
            return

        self.last_scan_mode = mode

        if mode == 'm':
            self.hsv_adjuster.pack_forget()
            self.sample_adjuster.pack(fill=BOTH, expand=True)

        if mode == 'a':
            self.sample_adjuster.pack_forget()
            self.hsv_adjuster.pack(fill=BOTH, expand=True)

    def resample(self, t, data):
        
        if t == 'sample':
            count_sample_points(data)
        
        elif t == 'hsv':
            st.h_ranges, st.s_divide, st.v_ranges = data


    def toggle_camera(self):

        if self.media_canvas.Mode == 1:
            self.media_canvas.closeCamera()
            self.status_var.set('摄像头已关闭')
            
        else:
            self.media_canvas.openCamera(1)
            self.status_var.set('使用摄像头中')

        self.video_btn_var.set(self.video_texts[self.media_canvas.Mode])

    def toggle_scan(self):

        if self.media_canvas.Mode == 0:
            self.status_var.set('请开启摄像头或打开图片')
            self.scan_btn_var.set(self.scan_texts[0])
            return

        self.scaning = not self.scaning

        if self.scaning:
            self.status_var.set('正在扫描魔方')

            if self.media_canvas.Mode > 0:
                self.update_func = self.get_cube_color

        else:
            self.update_func = None
            if self.media_canvas.Mode == 1:
                self.status_var.set('使用摄像头中')
            
            if self.media_canvas.Mode == 2:
                self.status_var.set('图片')

        self.scan_btn_var.set(self.scan_texts[self.scaning])

    def open_photo(self):
        
        picpath = filedialog.askopenfilename()

        self.media_canvas.add_pic(picpath)
    
    def get_cube_color(self):
        scan_mode = self.scan_mode.get()
        
        frame = self.media_canvas.frame()
        result, frame = scan_cube(frame, scan_mode)
        self.media_canvas.refresh(frame)

        if result:
            self.floorplan.showResult(result)

    def filter_hsv_color(self):

        frame = self.media_canvas.frame()
        mask = hsv_range_mask(frame, self.hsv_mask_range)
        self.media_canvas.refresh(mask)

    def hsv_save(self, item):

        st.hsv_ranges[item[0]] = item[1]
        st.store()

    def hsv_update(self, args):

        self.hsv_mask_range = args
        
    def hsv_toggle(self, hsv_range):

        if hsv_range:
            # filter hsv color
            self.hsv_mask_range = hsv_range

            if self.media_canvas.Mode > 0:
                self.update_func = self.filter_hsv_color

        else:
            self.update_func = None

    def update(self):

        if self.update_func:
            self.update_func()

        else:
            self.media_canvas.refresh()

        self.window.after(self.update_delay, self.update)


if __name__ == "__main__":

    st.init()

    App('test')