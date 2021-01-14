from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule, Task
from .evaluator import Evaluator136811


class Algorithm136811(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        r1 = self.run1(in_data)
        r2 = self.run2(in_data)
        if r1.score < r2.score:
            r2 = r1
        return r2

    @staticmethod
    def run1(in_data: Instance) -> Solution:  # 99.87, 53.26
        tasks = [(i + 1, t) for i, t in enumerate(in_data.tasks)]
        tasks.sort(key=lambda x: x[1].due_date)

        schedule = Schedule(in_data.no_tasks, [t[0] for t in tasks])
        solution = Solution(score=-1, schedule=schedule)

        evl = Evaluator136811().evaluate(in_data, solution)

        return Solution(score=evl.value, schedule=schedule)

    @staticmethod
    def run2(in_data: Instance) -> Solution:  # 80.5, 61.86
        tasks = [(i + 1, t) for i, t in enumerate(in_data.tasks)]
        tasks.sort(key=lambda x: x[1].due_date / x[1].weight)

        schedule = Schedule(in_data.no_tasks, [t[0] for t in tasks])
        solution = Solution(score=-1, schedule=schedule)

        evl = Evaluator136811().evaluate(in_data, solution)

        return Solution(score=evl.value, schedule=schedule)

    @staticmethod
    def make_simple_task(task: Task) -> Task:
        return Task(weight=task.weight, due_date=task.due_date,
                    duration=[task.duration[0] + task.duration[1], task.duration[2] + task.duration[1]])

    @staticmethod
    def run3(in_data: Instance) -> Solution:  # 55.96, 20.12  |  80.14, 59.81  |
        tasks = [(i + 1, t) for i, t in enumerate(in_data.tasks)]
        simple = [(i, Algorithm136811.make_simple_task(t)) for i, t in tasks]
        group1 = [task for task in simple if task[1].duration[0] <= task[1].duration[1]]
        group2 = [task for task in simple if task[1].duration[0] > task[1].duration[1]]

        group1.sort(key=lambda x: x[1].duration[0])
        group2.sort(key=lambda x: x[1].duration[1], reverse=True)
        group1.sort(key=lambda x: x[1].due_date/x[1].weight)
        group2.sort(key=lambda x: x[1].due_date/x[1].weight)
        i1, i2 = 0, 0
        schedule = []
        while i1 < len(group1) and i2 < len(group2):
            if group1[i1][1].due_date <= group2[i2][1].due_date:
                schedule.append(group1[i1][0])
                i1 += 1
            else:
                schedule.append(group2[i2][0])
                i2 += 1
        while i1 < len(group1):
            schedule.append(group1[i1][0])
            i1 += 1
        while i2 < len(group2):
            schedule.append(group2[i2][0])
            i2 += 1

        # schedule = [t[0] for t in group1]
        # schedule.extend([t[0] for t in group2])
        schedule = Schedule(in_data.no_tasks, schedule)
        solution = Solution(-1, schedule=schedule)

        evl = Evaluator136811().evaluate(in_data, solution)
        return Solution(score=evl.value, schedule=schedule)

    @staticmethod
    def run4(in_data: Instance) -> Solution:
        tasks = [(i + 1, t) for i, t in enumerate(in_data.tasks)]

        tasks.sort(key=lambda x: x[1].weight, reverse=True)
        tasks.sort(key=lambda x: x[1].due_date)

        schedule = Schedule(in_data.no_tasks, [t[0] for t in tasks])
        solution = Solution(score=-1, schedule=schedule)

        evl = Evaluator136811().evaluate(in_data, solution)

        return Solution(score=evl.value, schedule=schedule)

    @staticmethod
    def run5(in_data: Instance) -> Solution:
        tasks = [(i + 1, t) for i, t in enumerate(in_data.tasks)]

