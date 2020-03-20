from tkinter import ttk, Frame, Scale, Label
from tkinter import LEFT, BOTH, HORIZONTAL, X, Y, IntVar, StringVar


try:
    from .button import HoverButton

except:
    from button import HoverButton


padding_y = 2

class HSVAdjuster(Frame):

    '''
        adjust hsv range of a color, and store in json file 

    '''

    def __init__(self, parent, adjusting=None, toggle=None, save=None):

        Frame.__init__(self, master=parent, pady=padding_y)

        self.hsv_space = {
            "h": (0, 180),
            "s": (0, 255),
            "v": (0, 255)
        }

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
            v_l = StringVar(self)
            v_l.set(str(low))
            v_r = StringVar(self)
            v_r.set(str(up))
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

        for i, (prop, (l, r)) in enumerate(self.hsv_space.items()):
            Label(col1, text=prop).pack(fill=Y, expand=True)

            Scale(col2, from_=l, to=r, variable=self.lower_vars[i], tickinterval=r, command=self.sliding, \
                orient=HORIZONTAL).pack(fill=Y, expand=True)

            Scale(col3, from_=l, to=r, variable=self.upper_vars[i], tickinterval=r, command=self.sliding, \
                orient=HORIZONTAL).pack(fill=Y, expand=True)

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


if __name__ == "__main__":

    from tkinter import Tk

    window = Tk()
    HSVAdjuster(window).pack()
    window.mainloop()
