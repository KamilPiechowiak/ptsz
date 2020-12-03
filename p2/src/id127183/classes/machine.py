from p2.src.id127183.classes.task import Task


class Machine:

    def __init__(self, id, speed):
        self.id = id
        self.speed = speed
        self.list_of_tasks = []
        self.clock = 0.0

    def check_status(self, time):
        return self.clock <= time

    def update_clock(self, task):
        self.clock = max(self.clock, task.ready) + task.duration * self.speed
        return self.clock - task.ready

    def add_task(self, task):
        self.list_of_tasks.append(task.id)
        return self.update_clock(task)
