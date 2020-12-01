from math import floor
from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Schedule, Solution, Task

class ScheduleTask:
    def __init__(self, duration: int, ready: int, no: int = 0, start: float = 0, end: float = 0):
        self.duration = duration
        self.ready = ready
        self.no = no
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f'ScheduleTask(duration={self.duration}, ready={self.ready}, no={self.no})'

class Algorithm136834(Algorithm):
    def dummy_schedule(self, instance: Instance):
        tasks_per_machine = instance.no_tasks // instance.no_machines

        schedule = []
        task_num = 1
        for i in range(0, instance.no_machines - 1):
            tasks = range(task_num, task_num + tasks_per_machine)
            schedule.append(list(tasks))
            task_num += tasks_per_machine
        tasks = range(task_num, instance.no_tasks + 1)
        schedule.append(list(tasks))
        return Schedule(instance.no_tasks, instance.no_machines, schedule)

    def get_next_machine(self, times, speeds):
        next_machine = 0
        for i in range(0, len(times)):
            if times[i] < times[next_machine]:
                next_machine = i
        return next_machine
    
    def sort_global(self, instance: Instance, key):
        n = instance.no_tasks
        m = instance.no_machines
        times = [0] * m
        schedule = [[] for i in range(0, m)]

        tasks = sorted(instance.tasks, key=key)
        for task in tasks:
            next_machine = self.get_next_machine(times, instance.machine_speeds)
            schedule[next_machine].append(task.no)
            speed = instance.machine_speeds[next_machine]
            times[next_machine] = max(times[next_machine], task.ready) + speed * task.duration
        return Schedule(n, m, schedule)
    
    def ready_global(self, instance: Instance):
        return self.sort_global(instance, key=lambda task: task.ready)

    def mft(self, instance: Instance, schedule: Schedule):
        flow_sum = 0
        for machine_i, machine_tasks in enumerate(schedule):
            time = 0
            for task_i in machine_tasks:
                task = instance.tasks[task_i - 1]
                time = max(time, task.ready)
                duration = task.duration * instance.machine_speeds[machine_i]
                flow_sum += time + duration - task.ready
                time += duration
        return flow_sum / instance.no_tasks

    def run(self, instance: Instance):
        algorithm = self.ready_global

        for i, task in enumerate(instance.tasks):
            instance.tasks[i] = ScheduleTask(task.duration, task.ready, no=i + 1)
        schedule = algorithm(instance)
        score = self.mft(instance, schedule)
        return Solution(score, schedule)
