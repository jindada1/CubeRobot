
from tkinter import Button

class HoverButton(Button):

    def __init__(self, parent, hover="gainsboro", bg="white", params=None, click=None, **kw):

        if click:
            # pass params to command
            def do():
                click(params)

            Button.__init__(self, master=parent, bg=bg, command=do, **kw)

        else:
            Button.__init__(self, master=parent, bg=bg, **kw)

        self.hover = hover
        self.background = bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.config(bd=0)
        self.config(cursor='hand2')
        self.config(activebackground='whitesmoke')

    def on_enter(self, e):
        self['background'] = self.hover

    def on_leave(self, e):
        self['background'] = self.background

