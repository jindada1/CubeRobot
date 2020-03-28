from tkinter import ttk, Frame, Scale, Label, Entry, Canvas, Scrollbar, Text
from tkinter import LEFT, RIGHT, BOTH, X, Y, IntVar, StringVar

try:
    from . import HoverButton

except:
    from button import HoverButton


padding_y = 4

class HSVAdjuster(Frame):

    '''
        adjust hsv range of a color, and store in json file 

    '''

    def __init__(self, parent, adjusting=None, toggle=None, save=None):

        Frame.__init__(self, master=parent, pady=padding_y)

        self.hsv_space = [
            ("h", 0, 180),
            ("s", 0, 255),
            ("v", 0, 255)
        ]

        # bind event, callback when slidding any Scale
        self.adjusting = adjusting
        # bind event, callback when toggle mode
        self.toggle = toggle
        # bind event, callback when toggle mode
        self.save = save

        # store hsv ranges val
        self.hsv_range_vars = {}
        # store Scales' val
        self.lower_vars = [IntVar() for i in range(3)]
        self.upper_vars = [IntVar() for i in range(3)]

        self.adjustPanel = self.init_adjust_panel()

    def set_hsv_range(self, hsv_range):
        for color, (low, up) in hsv_range.items():
            v_l = StringVar(self, value=str(low))
            v_r = StringVar(self, value=str(up))
            self.hsv_range_vars[color] = (v_l, v_r)
        
        self.visualPanel = self.init_visual_panel()
        return self

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

        for color, (v_l, v_r) in self.hsv_range_vars.items():
            HoverButton(col1, bg=color, text=color, cursor="hand2", params=color, click=self.adjust)\
                .pack(fill=BOTH, expand=True, pady=padding_y)
            Label(col2, textvariable=v_l).pack(fill=Y, expand=True)
            Label(col3, textvariable=v_r).pack(fill=Y, expand=True)

        visualPanel.pack(fill=BOTH, expand=True)
        return visualPanel

    def init_adjust_panel(self):

        adjustPanel = Frame(self)

        title = Frame(adjustPanel)
        title.pack(fill=X)
        Label(title, text="正在调整颜色: ").pack(side=LEFT)
        self.adj_color = StringVar(title)
        ttk.OptionMenu(title, self.adj_color, "-_-", *self.hsv_range_vars.keys()).pack(side=LEFT, fill=X, expand=True)
        HoverButton(title, text="保存", command=self.save_color).pack(side=LEFT)
        Label(title).pack(side=LEFT)
        HoverButton(title, text="返回", command=self.visualize).pack(side=LEFT)

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

        for i, (prop, l, r) in enumerate(self.hsv_space):
            Label(col1, text=prop).pack(fill=Y, expand=True)

            Scale(col2, from_=l, to=r, variable=self.lower_vars[i], tickinterval=r, command=self.sliding, \
                orient='horizontal').pack(fill=Y, expand=True)

            Scale(col3, from_=l, to=r, variable=self.upper_vars[i], tickinterval=r, command=self.sliding, \
                orient='horizontal').pack(fill=Y, expand=True)

        return adjustPanel

    def adjust(self, color):
        self.adj_color.set(color)

        lower, upper = self.hsv_range_vars[color]
        for i in range(3):
            self.lower_vars[i].set(int(lower.get()[1:-1].split(', ')[i]))
            self.upper_vars[i].set(int(upper.get()[1:-1].split(', ')[i]))

        self.visualPanel.pack_forget()
        self.adjustPanel.pack(fill=BOTH, expand=True)

        if self.toggle:
            self.toggle((
                list(map(lambda var: var.get(), self.lower_vars)),
                list(map(lambda var: var.get(), self.upper_vars))
            ))

    def visualize(self):
    
        self.adjustPanel.pack_forget()
        self.visualPanel.pack(fill=BOTH, expand=True)
        if self.toggle:
            self.toggle(None)

    def sliding(self, e):

        if self.adjusting:
            self.adjusting((
                list(map(lambda var: var.get(), self.lower_vars)),
                list(map(lambda var: var.get(), self.upper_vars))
            ))
        else:
            print('test', 'sliding', e)

    def save_color(self):

        if self.save:
            lower = list(map(lambda var: var.get(), self.lower_vars))
            upper = list(map(lambda var: var.get(), self.upper_vars))
            color = self.adj_color.get()

            self.hsv_range_vars[color][0].set(str(lower))
            self.hsv_range_vars[color][1].set(str(upper))

            self.save((color, (lower, upper)))

        else:
            print('test', 'click save')


class mySpinBox(Frame):
    
    def __init__(self, parent, title=None, var=None, change=None, range_=(0, 180)):

        Frame.__init__(self, master=parent, pady=padding_y)

        self.var = var or IntVar()
        self.range = range_
        self.change = change
        self.title = title

        self.init_widgets()

    def init_widgets(self):

        if self.title:
             Label(self,text=self.title, width=6).pack(side=LEFT)

        c = Frame(self)
        c.pack(side=RIGHT, fill=X, expand=True)
        HoverButton(c, text='-', params=-1, click=self.action) \
            .pack(side=LEFT, fill=X, expand=True)
        Entry(c, textvariable=self.var, width=4, bd=0, state='disabled', justify='center') \
            .pack(side=LEFT, fill=BOTH, expand=True)
        HoverButton(c, text='+', params=1, click=self.action) \
            .pack(side=LEFT, fill=X, expand=True)

    def action(self, op):
        val = int(self.var.get())
        val += op

        if self.range and (val < self.range[0] or val > self.range[1]):
                val -= op
                return

        self.var.set(str(val))

        if self.change:
            self.change(self.title, val)


class SampleAdjuster(Frame):

    '''
        adjust hsv range of a color, and store in json file 

    '''

    def __init__(self, parent, adjusting=None, toggle=None, save=None):

        Frame.__init__(self, master=parent, pady=padding_y)

        # bind event, callback when slidding any Scale
        self.adjusting = adjusting
        # bind event, callback when toggle mode
        self.save = save

        self.vars = [IntVar() for i in range(3)]
        
        self.projection_rate = 1    # float: projection rate, big/small
        self.sample_area = None     # int: rectangle created by canvas, represents sampling area
        self.smallscreen = None     # tuple: (w, h, y): info of smallscreen
        self.bigscreen = None       # tuple: (w, h): size of bigsreen, passed by caller, 
        self.sample = None          # list: [x, y, w]: sample in smallscreen

        self.scale_step = StringVar(value='10')

        self.toggle_val = True
        self.init_canvas_panel().pack(fill=BOTH, expand=True)

    def init_canvas_panel(self):

        self.canvas_panel = cp = Frame(self)

        control = Frame(cp)
        control.pack(fill=X)

        Label(control, text='缩放步长').pack(side=LEFT)
        vcmd = (control.register(lambda c: c.isdigit()), '%P')
        Entry(control, textvariable=self.scale_step, validate='key', vcmd=vcmd, width=4)\
            .pack(side=LEFT, fill=Y)
        HoverButton(control, text="缩小", params=-1, click=self.change_scale) \
            .pack(side=LEFT, fill=X, expand=True, padx=6)
        HoverButton(control, text="放大", params=1, click=self.change_scale) \
            .pack(side=LEFT, fill=X, expand=True)
        HoverButton(control, text="保存", command=self.save_setting).pack(side=LEFT, fill=X, expand=True, padx=6)
        HoverButton(control, text="⚙", command=self.toggle).pack(side=LEFT, fill=X, expand=True)

        panel = Frame(cp)
        panel.pack(fill=BOTH, expand=True)
        
        self.canvas = Canvas(panel, bg='white', width=40, height=30, bd=0, highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True, pady=4)
        self.canvas.bind("<Enter>", self.init_projection)

        return cp

    def init_data_panel(self):

        self.data_panel = dp = Frame(self)
        control = Frame(dp)
        control.pack(fill=X)

        HoverButton(control, text="保存", command=self.save_setting).pack(side=LEFT, fill=X, expand=True)
        Label(control).pack(side=LEFT)
        HoverButton(control, text="返回", command=self.toggle).pack(side=LEFT, fill=X, expand=True)

        col1 = Frame(dp)
        col1.pack(side=LEFT, fill=BOTH, expand=True)
        for color, var in self.hues:
            mySpinBox(col1, title=color, var=var, change=self.color_hsv_changed).pack(fill=X)

        col2 = Frame(dp)
        col2.pack(side=LEFT, fill=BOTH, expand=True)
        mySpinBox(col2, title='sline', var=self.saturation, range_=(0, 255), change=self.color_hsv_changed).pack(fill=X)
        for color, var in self.values:
            mySpinBox(col2, title=color, var=var, range_=(0, 255), change=self.color_hsv_changed).pack(fill=X)

        return dp

    def init_projection(self, e=None):

        if not self.bigscreen:
            return

        if not self.smallscreen:
            # aspect rate of big screen
            h_aspect_w = self.bigscreen[1]/self.bigscreen[0]

            # get safe area
            w = self.canvas.winfo_width()
            h = int(w * h_aspect_w)
            y = (self.canvas.winfo_height() - h) // 2
            self.smallscreen = (w, h, y)

            # count projection rate: small to big
            self.projection_rate = r = self.bigscreen[0] / w

            # project sample from bigscreen to small screen
            self.sample = list(map(lambda v: int(v/r), self.sample))
            self.draw_sample_area()

        w, h, y = self.smallscreen
        
        self.canvas.create_line(0,   y-3, w,   y-3, fill="palegreen", width=3)
        self.canvas.create_line(0, h+y+3, w, h+y+3, fill="palegreen", width=3)

    def draw_sample_area(self):
        x, y, w = self.sample
        y += self.smallscreen[2]
        w = 3*w

        self.sample_area = self.canvas.create_rectangle(x, y, x+w, y+w, \
            fill='whitesmoke', outline="skyblue", activewidth=3)

        self.canvas.tag_bind(self.sample_area, '<Button-1>', self.dragstart)
        self.canvas.tag_bind(self.sample_area, '<B1-Motion>', self.draging)

    def dragstart(self, event):
        self.x = event.x
        self.y = event.y
        self.s_x = self.sample[0]
        self.s_y = self.sample[1]

    def draging(self,event):
        
        self.sample[0] = event.x - self.x + self.s_x
        self.sample[1] = event.y - self.y + self.s_y

        self.refresh()

    def refresh(self):

        self.verify_sample()

        x, y, w = self.sample
        y += self.smallscreen[2]
        w = 3*w

        self.canvas.coords(self.sample_area, x, y, x+w, y+w)

        if self.adjusting:
            self.adjusting(
                'sample',
                list(map(lambda v: int(self.projection_rate*v), self.sample))
            )

        else:
            print('test', 'sliding', e)

    def verify_sample(self):

        W, H, _ = self.smallscreen
        w = self.sample[2]*3

        self.sample[0] = max(self.sample[0], 0)
        self.sample[1] = max(self.sample[1], 0)

        if self.sample[0] + w > W:
            self.sample[0] = W - w

        if self.sample[1] + w > H:
            self.sample[1] = H - w

    def set_data(self, sample, bigscreen, color_hsv):

        self.sample = sample.copy()

        self.bigscreen = bigscreen

        hues, saturation, values = color_hsv
        self.hues = list(map(lambda t: (t[0], IntVar(value=t[1])), hues))
        self.saturation = IntVar(value=saturation)
        self.values = list(map(lambda t: (t[0], IntVar(value=t[1])), values))

        self.init_data_panel()

    def change_scale(self, arg):

        self.sample[2] += int(self.scale_step.get()) * arg

        self.refresh()

    def color_hsv_changed(self, color, val):
        hues = list(map(lambda t: [t[0], t[1].get()], self.hues))
        saturation = self.saturation.get()
        values = list(map(lambda t: [t[0], t[1].get()], self.values))
        if self.adjusting:
            self.adjusting(
                'hsv',
                (hues, saturation, values)
            )

    def save_setting(self):

        if self.save:
            self.save()

        else:
            print('test', 'click save')
    
    def toggle(self):
        self.toggle_val = not self.toggle_val

        if self.toggle_val:
            self.data_panel.pack_forget()
            self.canvas_panel.pack(fill=BOTH, expand=True)
        
        else:
            self.canvas_panel.pack_forget()
            self.data_panel.pack(fill=BOTH, expand=True)


class Console(Frame):

    def __init__(self, parent, debug=False):
        
        Frame.__init__(self, master=parent)

        self.line = 1
        self.debug = debug

        self.initwidgets()

    def initwidgets(self):
        
        Left = Frame(self, height=10)
        Left.pack(side=LEFT, fill=BOTH, expand=True)

        self.content = C = Text(Left, width=20, height=3)
        C.tag_config('index',foreground='green', background="whitesmoke" )
        C.tag_config('warning',foreground='black', background="lemonchiffon" )
        C.bind("<Key>", lambda e: self.__ctrl(e))
        C.pack(fill=BOTH, expand=True)

        HoverButton(Left, text='清空控制台', command=self.clear).pack(side=LEFT, fill=X, expand=True)

        if self.debug:
            HoverButton(Left, text='插入', command=self.__addline).pack(side=LEFT, fill=X, expand=True)

        S = Scrollbar(self)
        S.pack(side=RIGHT, fill=Y)

        S.config(command=C.yview)
        C.config(yscrollcommand=S.set)


    def __ctrl(self, event):
        if(12==event.state and event.keysym=='c' ):
            return
        else:
            self.log('read only', 'warning')
            return "break"
            
    def log(self, text, tag=None):
        
        self.content.insert('end', "%3d " % self.line, 'index')
        self.content.insert('end', "%s\n" % text, tag)
        self.line += 1
        self.content.see('end')
    
    def clear(self):

        self.line = 1
        self.content.delete('1.0','end')
    
    def __addline(self):

        self.log('debug')


if __name__ == "__main__":

    from tkinter import Tk

    window = Tk()
    hr = {
        'Red'   : ([156,  43,  46], [180, 255, 255]), # Red
        'red'   : ([  0,  43,  46], [ 13, 255, 255]), # Red
        'blue'  : ([ 69, 120, 100], [179, 255, 255]), # Blue
        'yellow': ([ 21, 110, 117], [ 45, 255, 255]), # Yellow
        'orange': ([  0, 110, 125], [ 17, 255, 255]), # Orange
        'white' : ([  0,   0, 221], [180,  30, 255]), # White
        'green' : ([ 35,  43,  46], [ 77, 255, 255]), # Green
    }
    # HSVAdjuster(window).set_hsv_range(hr).pack()
    # SampleAdjuster(window).pack(fill=BOTH, expand=True)
    Console(window, debug=True).pack(fill=BOTH, expand=True)
    window.mainloop()
