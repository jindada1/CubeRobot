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

    def close(self):
        self.loop = False
        
        while self.isAlive():
            sleep(.2)

        print('exit thread')


    def run(self):
        looptime = 0
        while self.loop:
            looptime += 1
            print(looptime)

            delay = .5
            sleep(delay)

    def go(self):
        self.start()
        self.client.run()


def get_tasks() -> list:

    tasks = []

    for i in range(6):
        tasks.insert(0, {
            'name': 0,
            'description': '正在扫描第 %s 个面' % (i + 1)
        })

    tasks.insert(0, {
        'name': 1,
        'description': '正在求解'
    })

    tasks.insert(0, {
        'name': 2,
        'description': '旋转机械臂'
    })

    return tasks

if __name__ == "__main__":

    client = Client("Rubik's Cube Robot")

    Controller(client).go()