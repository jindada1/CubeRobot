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

    def get_solution(self):
        # self.instructions = solve(self.gui.cube_str)
        cube = "F2 R3 U2 B2 R3 D2 F2 R1 U2 F1 D3 R3 D2 R1 B3 D3 F2 U3 R3 U2"
        self.instructions = solve(cube)
        self.task_end()

    def adapt_instruction(self, raw_ins: str) -> str:
        '''
        raw_ins: for example "F2 R3 U2 B2 R3 D2 F2 R1 U2 F1 D3 R3 D2 R1 B3 D3 F2 U3 R3 U2"
        replace actions contains U, D with instructions contains L, F, R, B
        for example:
            U1 = F3,B1 L1 F1,B3
            U2 = F3,B1 L2 F1,B3
            D1 = F3,B1 R1 F1,B3
        '''
        actions = raw_ins.split(' ')
        for i in range(len(actions)):
            action = actions[i]
            face = action[0]

            if face == 'U':
                deg = action[1]
                actions[i] = 'F3,B1 L%s F1,B3' % deg
            
            elif face == 'D':
                deg = action[1]
                actions[i] = 'F3,B1 R%s F1,B3' % deg

        return ' '.join(actions)
            
    def send_instructions(self):
        '''
        instructions(str): a serial of actions, use whitespace to separate actions
        for example:
            F1 B3 F1,B3 U1 L2.
        '''
        adapted_ins = self.adapt_instruction(self.instructions)
        res = self.gui.esp_client.send('/restore', {
            'ins': adapted_ins
        })
        self.task_end()

    def send_action(self, action: str):
        '''
        action(str): rotate one or many faces. [face][deg], use ',' to combine multiple faces
        for example:
            F1: rotate face 'F' 90 degrees clockwise
            B3: rotate face 'B' 90 degrees counterclockwise
            F1,B3: flip the entire cube to the right, which means L -> U, U -> R, R -> B, B -> L.
        '''
        # print('send action', action)
        res = self.gui.esp_client.send('/action', {
            'action': action
        })
        self.task_end()

    def go(self):
        self.start()
        self.gui.run()

    def task_start(self, task: str):
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
    'send:F1,B3',
    # face: recognize colors on face 2
    'face',
    # horizontal rotation →
    'send:F1,B3',
    # face: recognize colors on face 3
    'face',
    # horizontal rotation →
    'send:F1,B3',
    # face: recognize colors on face 4
    'face',
    # horizontal rotation →
    'send:F1,B3',
    # vertical rotation ↑
    'send:L3,R1',
    # face: recognize colors on face 5
    'face',
    # vertical rotation ↓ x 2
    'send:L2,R3',
    # face: recognize colors on face 6
    'face',
    # vertical rotation ↑
    'send:L3,R1',
    # get cube solution
    'solu',
    # solve the cube
    'cube'
]

if __name__ == "__main__":

    gui = App("Rubik's Cube Robot")
    con = Controller(gui, cube_robot_tasks)
    
    try:
        con.go()
    except:
        con.close()
