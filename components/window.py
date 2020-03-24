
from tkinter import Tk

class Window(Tk):
    
    def __init__(self, title='window', control=False):

        Tk.__init__(self, title)

        self.update_delay = 33
        # update_func will be called in update
        self.update_func = None

    def run(self):
        
        # update will be automatically called every {update_delay} milliseconds
        self.__update()

        self.mainloop()

    def __update(self):

        if self.update_func:
            self.update_func()

        else:
            print('update')

        self.after(self.update_delay, self.__update)

