class Task:

    def __init__(self, id, duration, ready):
        self.id = id
        self.duration = duration
        self.ready = ready
        self.started = False

    def task_started(self):
        self.started = True
