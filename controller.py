from time import sleep
from guimain import App
from twophase import solve
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
        gui.message = self.receive

        self.tasks = tasks
        self.paused = False
        self.waiting = False
        self.next_task_id = 0

        # instructions that restore the rubik's cube
        self.instructions = None

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
    
    def receive(self, action, params=True):
        
        if action == 'finish':
            self.task_end(params)
        
        if action == 'pause':
            self.gui.console.log('暂停')
            self.paused = True

    def get_solution(self):
        # cube = self.gui.cube_str
        cube = 'LUFRUDDBDLFULRUDBRFLFFFDDRLRUBFDDRDBBBRLLRULBLFUBBUURF'
        self.instructions = solve(cube)
        self.task_end()

    def adapt_instruction(self, sequence: str) -> str:
        '''
        raw_ins: for example "F2 R3 U2 B2 R3 D2 F2 R1 U2 F1 D3 R3 D2 R1 B3 D3 F2 U3 R3 U2"
        replace actions contains U, D with instructions contains L, F, R, B, H, V, D
        '''
        sequence = list(sequence)
        index = 0
        actions = []
        flip = {
            'U': 'F',
            'F': 'D',
            'D': 'B',
            'B': 'F',
            'L': 'L',
            'R': 'R'
        }

        while index < len(sequence):
            face = sequence[index]
            deg = sequence[index + 1]
            if face in 'UD':
                actions.append('D1')
                actions.append('V1')
                actions.append('D3')

                wow = index
                while wow < len(sequence):
                    sequence[wow] = flip[face]
                    wow += 3

            else:
                actions.append(face + deg)
                index += 3

        return actions

    def send_instructions(self):
        '''
        add actions into self.task
        '''
        actions = self.adapt_instruction(self.instructions)
        for action in actions:
            self.tasks.append('send:%s' % action)
        
        self.gui.console.log('add actions:' + str(actions))

        self.task_end()

    def send_action(self, action: str):
        '''
        action(str): rotate one or many faces. [face][deg], use ',' to combine multiple faces
        for example:
            F1: rotate face 'F' 90 degrees clockwise
            B3: rotate face 'B' 90 degrees counterclockwise
            H1: flip the entire cube to the right, which means L -> U, U -> R, R -> B, B -> L.
        '''

        res = self.gui.esp_client.send('/action', {
            'face': action[0],
            'deg': 2 if action[1] == '2' else 1,
            'clockwise': -1 if action[1] == '3' else 1
        })
        self.task_end()

    def go(self):
        self.start()
        self.gui.run()

    def task_start(self, task: str):
        self.waiting = True
        self.gui.console.log(task)
        op = task.split(':')
        func = self.operations[op[0]]
        if len(op) == 1:
            func()
        else:
            func(op[1])

    def task_end(self, arg=True):
        if arg:
            self.waiting = False
        else:
            self.gui.console.log('[task end wrong]', self.current_task)

    def next_task(self):

        if self.round_completed:
            return

        now = self.tasks[self.next_task_id]
        self.next_task_id += 1
        return now

    def run(self):

        while self.loop:
            sleep(self.loop_delay)

            if self.waiting or self.round_completed or self.paused:
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
    # expand FB
    'send:D1',
    # horizontal rotation →
    'send:H1',
    # face: recognize colors on face 2
    'face',
    # horizontal rotation →
    'send:H1',
    # face: recognize colors on face 3
    'face',
    # horizontal rotation →
    'send:H1',
    # face: recognize colors on face 4
    'face',
    # horizontal rotation →
    'send:H1',
    # shrink FB, expand LR
    'send:D2',
    # vertical rotation ↑
    'send:V1',
    # face: recognize colors on face 5
    'face',
    # vertical rotation ↓ x 2
    'send:V2',
    # face: recognize colors on face 6
    'face',
    # vertical rotation ↑
    'send:V1',
    # shrink LR
    'send:D1',
    # get cube solution
    'solu',
    # solve the cube
    'cube'
]

if __name__ == "__main__":

    gui = App("Rubik's Cube Robot", True)
    con = Controller(gui, cube_robot_tasks)

    try:
        con.go()
    except:
        con.close()
        