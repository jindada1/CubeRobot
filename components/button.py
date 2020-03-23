
from tkinter import Button

class HoverButton(Button):

    def __init__(self, parent, hover="gainsboro", bg="white", params=None, click=None, **kw):

        if click:
            # pass params to command
            def do():
                click(params)

            Button.__init__(self, master=parent, bg=bg, activebackground="whitesmoke", command=do, **kw)

        else:
            Button.__init__(self, master=parent, bg=bg, activebackground="whitesmoke", **kw)

        self.hover = hover
        self.background = bg
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.config(border='0')

    def on_enter(self, e):
        self['background'] = self.hover
        self['cursor'] = 'hand2'

    def on_leave(self, e):
        self['background'] = self.background

