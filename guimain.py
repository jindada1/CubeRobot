
from tkinter import Tk, Label

class Window(Tk):
    
    def __init__(self, title='window', control=False, update=None):

        Tk.__init__(self, title)

        self.update_delay = 300
        # update_func will be called in update
        self.update_func = update

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


class Controller(Window):
    
    def __init__(self, title=None):
        
        Window.__init__(self, title=title)

        Label(self, text='1111').pack()

        self.update_func = haha


def haha():

    print('123')

if __name__ == "__main__":

    Controller("Rubik's Cube Robot").run()