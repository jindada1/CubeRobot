from time import sleep
from guimain import App
# from twophase import solve
from threading import Thread


class Controller(Thread):
    '''
    Controller thread that control main gui application
    '''

    def __init__(self, gui, tasks):

        Thread.__init__(self)
        self.daemon = True
        self.loop = True
        self.loop_delay = 0.5

        self.gui = gui
        gui.onclose = self.close
        gui.finished = self.task_end

        self.tasks = tasks
        self.waiting = False
        self.next_task_id = 0

        self.operations = {
            'conn': self.gui.connect_device,
            'face': self.gui.get_face,
            'send': self.send_action,
            'solu': self.get_solution,
            'cube': self.send_instructions
        }

    @property
    def round_completed(self):
        return self.next_task_id == len(self.tasks)

    @property
    def current_task(self):
        return self.tasks[self.next_task_id - 1]

    def get_solution(self):
        cube_definition = self.gui.cube_str
        print('cube definition is', cube_definition)
        self.task_end()

    def send_instructions(self):
        res = self.gui.esp_client.send('/wait', {
            'time': 2000
        })
        self.task_end()

    def send_action(self, action):
        print('send action', action)
        res = self.gui.esp_client.send('/wait', {
            'time': 2000
        })
        self.task_end()

    def go(self):
        self.start()
        self.gui.run()

    def task_start(self, task):
        self.waiting = True
        op = task.split(':')
        func = self.operations[op[0]]
        if len(op) == 1:
            func()
        else:
            func(op[1])

    def task_end(self, arg='finished'):
        print(self.current_task, arg)
        self.waiting = False

    def next_task(self):

        if self.round_completed:
            return

        now = self.tasks[self.next_task_id]
        self.next_task_id += 1
        return now

    def run(self):

        while self.loop:
            sleep(self.loop_delay)

            if self.waiting or self.round_completed:
                continue

            task = self.next_task()
            self.task_start(task)

    def close(self):
        self.loop = False

        while self.isAlive():
            sleep(.2)

        print('exit thread')


cube_robot_tasks = [
    # connect esp8266 access point
    'conn',
    # face: recognize colors on face 1
    'face',
    # horizontal rotation →
    'send:h',
    # face: recognize colors on face 2
    'face',
    # horizontal rotation →
    'send:h',
    # face: recognize colors on face 3
    'face',
    # horizontal rotation →
    'send:h',
    # face: recognize colors on face 4
    'face',
    # horizontal rotation →
    'send:h',
    # vertical rotation ↑
    'send:v',
    # face: recognize colors on face 5
    'face',
    # vertical rotation ↓ x 2
    'send:-2v',
    # face: recognize colors on face 6
    'face',
    # vertical rotation ↑
    'send:v',
    # get cube solution
    'solu',
    # just solve cube
    'cube'
]

if __name__ == "__main__":

    gui = App("Rubik's Cube Robot")
    con = Controller(gui, cube_robot_tasks)

    try:
        con.go()
    except:
        con.close()
