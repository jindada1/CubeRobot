
from tkinter import Tk, ttk, Toplevel, StringVar

class Window():
    '''
    tkinter window

    properties:
        window: Tk() instance, root window

    interfaces:
        update_func: this method will be called when update
        onclose: this method will be called when click right-top close button
    
    methods:
        run: start tk mainloop
    '''
    def __init__(self, title=None):
        
        self.window = Tk(title)

        self.update_delay = 33
        # update_func will be called in update
        self.update_func = None
        # onclose will be called when __close
        self.onclose = None

        self.window.protocol("WM_DELETE_WINDOW", self.__close)

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

    def __close(self):

        if self.onclose:
            self.onclose()

        self.window.destroy()

class SubWindow():
    '''
    tkinter wubwindow
    
    methods:
        open: focus subwindow if exits, otherwise create a new one
    '''
    def __init__(self, parent):

        self.parent = parent
        self.win = None
        self.selected = StringVar()

    def open(self):

        if self.win and Toplevel.winfo_exists(self.win):
            self.win.focus()
            return
        
        else:
            self.__create()
    
    def __create(self):

        self.win = Toplevel(self.parent)
        self.display()

    def display(self):

        for i in range(9):
            text = 'text_%d' % i
            value = 'value_%d' % i
            ttk.Radiobutton(self.win, text=text, variable=self.selected, value=value).pack()

if __name__ == "__main__":
    
    win = Window('test window')
    SubWindow(win.window).open()
    win.run()