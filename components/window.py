
from tkinter import Tk, ttk, Toplevel, StringVar

class Window():
    
    def __init__(self, title=None):
        
        self.window = Tk(title)

        self.update_delay = 33
        # update_func will be called in update
        self.update_func = None

    def run(self):

        # update will be automatically called every {update_delay} milliseconds
        self.__update()

        self.window.mainloop()

    def __update(self):

        if self.update_func:
            self.update_func()

        else:
            print('update')

        self.window.after(self.update_delay, self.__update)


class BlueTooth():

    def __init__(self, parent):

        self.parent = parent
        self.win = None
        self.mac = StringVar()

    def open(self):

        if self.win and Toplevel.winfo_exists(self.win):
            self.win.focus()
            return
        
        else:
            self.create()
    
    def create(self):

        self.win = Toplevel(self.parent)
        self.display()

    def display(self):

        for i in range(9):
            text = 'text_%d' % i
            value = 'value_%d' % i
            ttk.Radiobutton(self.win, text=text, variable=self.mac, value=value).pack()

if __name__ == "__main__":
    
    win = Window('test window')
    BlueTooth(win.window).open()
    win.run()