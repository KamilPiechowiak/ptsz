from math import floor
from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Schedule, Solution, Task

class ScheduleTask:
    def __init__(self, duration: int, due_date: int, weight: int = 0, no: int = 0, start: float = 0, end: float = 0):
        self.duration = duration
        self.due_date = due_date
        self.weight = weight
        self.no = no
        self.start = start
        self.end = end
    
    def __repr__(self):
        return f'ScheduleTask(duration={self.duration}, due_date={self.due_date}, weight={self.weight}, no={self.no})'

class Algorithm136834(Algorithm):
    def dummy_schedule(self, instance: Instance):
        n = instance.no_tasks
        return Schedule(instance.no_tasks, list(range(1, n + 1)))

    def sort_global(self, instance: Instance, key):
        n = instance.no_tasks
        tasks = sorted(instance.tasks, key=key)
        return Schedule(n, [task.no for task in tasks])
    
    def due_date_global(self, instance: Instance):
        return self.sort_global(instance, key=lambda task: task.due_date)

    def duration_global(self, instance: Instance):
        return self.sort_global(instance, key=lambda task: max(task.duration))


    def mwt(self, instance: Instance, schedule: Schedule):
        m = instance.no_machines
        times = [0 for i in range(0, m)]
        late_work_sum = 0
        for task_i in schedule:
            task = instance.tasks[task_i - 1]
            times[0] = times[0] + task.duration[0]
            for i in range(1, m):
                times[i] = max(times[i], times[i - 1]) + task.duration[i]
            late_work_sum += task.weight * max(times[-1] - task.due_date, 0)
        weight_sum = sum([task.weight for task in instance.tasks])
        return late_work_sum / weight_sum


    def run(self, instance: Instance):
        algorithm = self.duration_global

        for i, task in enumerate(instance.tasks):
            instance.tasks[i] = ScheduleTask(task.duration, task.due_date, task.weight, no=i + 1)
        schedule = algorithm(instance)
        score = self.mwt(instance, schedule)
        # evaluator = Evaluator136834()
        # score = evaluator.mwt(instance, schedule)
        return Solution(score, schedule)
