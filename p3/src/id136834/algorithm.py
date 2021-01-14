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
        return f'ScheduleTask(duration={self.duration}, due_date={self.due_date}, weight={self.weight}, no={self.no}, start={self.start}, end={self.end})'

class Algorithm136834(Algorithm):
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


    def dummy_schedule(self, instance: Instance):
        n = instance.no_tasks
        return Schedule(instance.no_tasks, list(range(1, n + 1)))

    def sort_global(self, instance: Instance, key):
        n = instance.no_tasks
        tasks = sorted(instance.tasks, key=key)
        return Schedule(n, [task.no for task in tasks])
    
    def due_date_global(self, instance: Instance):
        return self.sort_global(instance, key=lambda task: task.due_date)

    def weight_global(self, instance: Instance):
        return self.sort_global(instance, key=lambda task: -task.weight)

    def duration_global(self, instance: Instance):
        return self.sort_global(instance, key=lambda task: max(task.duration))

    def duration_by_weight_global(self, instance: Instance):
        return self.sort_global(instance, key=lambda task: sum(task.duration) / task.weight)


    def update_times(self, times, task):
        times[0] = times[0] + task.duration[0]
        times[1] = max(times[1], times[0]) + task.duration[1]
        times[2] = max(times[2], times[1]) + task.duration[2]
        return times
    
    def get_end_time(self, times, task):
        end_time = times[0] + task.duration[0]
        end_time = max(times[1], end_time) + task.duration[1]
        end_time = max(times[2], end_time) + task.duration[2]
        return end_time

    def get_late_tasks(self, times, tasks, k):
        tasks.sort(key=lambda task: task.due_date - task.end)

        # new_tasks = []
        # new_k = k
        # for task in tasks:
        #     if task.due_date < task.end:
        #         new_tasks.append(task)
        #     elif new_k > 0:
        #         new_tasks.append(task)
        #         new_k -= 1

        # return new_tasks

        i = 0
        while i < len(tasks) and tasks[i].due_date < tasks[i].end:
            i += 1

        return tasks[:i + k]

    def look_ahead(self, instance: Instance, key, k=10):
        n = instance.no_tasks
        m = instance.no_machines
        tasks = instance.tasks.copy()
        schedule = []
        times = [0] * m

        while len(tasks) > 0:
            for task in tasks:
                task.start = times[0]
                task.end = self.get_end_time(times, task)

            late_tasks = self.get_late_tasks(times, tasks, k)
            task = min(late_tasks, key=key)
            schedule.append(task.no)
            tasks.remove(task)
            self.update_times(times, task)

        return Schedule(n, schedule)

    def duration_by_weight_look_ahead(self, instance: Instance):
        return self.look_ahead(instance, key=lambda task: sum(task.duration) / task.weight, k=1)


    def run(self, instance: Instance):
        algorithm = self.duration_by_weight_look_ahead

        for i, task in enumerate(instance.tasks):
            instance.tasks[i] = ScheduleTask(task.duration, task.due_date, task.weight, no=i + 1)
        schedule = algorithm(instance)
        score = self.mwt(instance, schedule)
        # evaluator = Evaluator136834()
        # score = evaluator.mwt(instance, schedule)
        return Solution(score, schedule)
