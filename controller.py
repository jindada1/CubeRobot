from threading import Thread
from time import sleep
from guimain import Client


class Controller(Thread):

    def __init__(self, client):

        Thread.__init__(self)
        self.daemon = True
        self.loop = True

        self.client = client
        client.onclose = self.close
        client.finished = self.finished

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

    def finished(self, arg):
        
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

    client = Client("Rubik's Cube Robot")

    Controller(client).go()