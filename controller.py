from time import sleep
from guimain import App
from twophase import solve
from threading import Thread


class Controller(Thread):
    '''
    Controller thread that control main gui application
    '''
    def __init__(self, client):

        Thread.__init__(self)
        self.daemon = True
        self.loop = True

        self.client = client
        client.onclose = self.close
        client.finished = self.task_finished

        self.init_tasks()
        self.lock = False

    def init_tasks(self):

        self.tasks = [i for i in range(20)]

    def go(self):
        self.start()
        self.client.run()

    def handle(self):
        
        if self.lock or not self.tasks:
            return

        arg = self.tasks.pop()
        if arg % 2:
            self.client.get_face()
            self.lock = True
        
        print(self.tasks)
        print(arg)

    def task_finished(self, arg):
        
        print(arg)
        self.lock = False

    def run(self):
        
        while self.loop:
            delay = .5
            sleep(delay)
            self.handle()

    def close(self):
        self.loop = False
        
        while self.isAlive():
            sleep(.2)

        print('exit thread')

if __name__ == "__main__":

    client = App("Rubik's Cube Robot")

    Controller(client).go()