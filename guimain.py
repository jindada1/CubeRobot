
from components import *
from tkinter import Label


class Controller(Window):
    
    def __init__(self, title=None):
        
        Window.__init__(self, title=title)

        Label(self, text='1111').pack()

        self.update_func = haha



if __name__ == "__main__":

    Controller("Rubik's Cube Robot").run()