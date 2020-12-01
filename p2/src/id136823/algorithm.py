from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule


class Machine:
    def __init__(self, machine_id, machine_speed):
        self.machine_id = machine_id
        self.machine_speed = machine_speed
        self.machine_time = 0
        self.schedule = []

    def assign_task(self, task):
        self.schedule.append(task.task_id)
        self.machine_time = min(self.machine_time, task.ready) + task.duration * self.machine_speed
        return self.machine_time - task.ready

    def is_available(self, current_time):
        return self.machine_time <= current_time


class Task:
    def __init__(self, task_id, duration, ready):
        self.task_id = task_id
        self.duration = duration
        self.ready = ready
        self.available = True

    def mark_finished(self):
        self.available = False


class Algorithm136823(Algorithm):
    @staticmethod
    def get_available_machines(machines, current_time):
        available_machines = []
        for machine in machines:
            if machine.is_available(current_time):
                available_machines.append(machine)
        return available_machines

    @staticmethod
    def get_available_tasks(machine, tasks):
        available_tasks = []
        for task in tasks:
            if (task.ready <= machine.machine_time) and task.available:
                available_tasks.append(task)
        return available_tasks

    @staticmethod
    def get_earliest_task(tasks):
        index = 1
        earliest_task = tasks[0]
        while not earliest_task.available:
            earliest_task = tasks[index]
            index += 1

        for i in range(len(tasks)):
            if tasks[i].ready < earliest_task.ready and tasks[i].available:
                earliest_task = tasks[i]
        return earliest_task

    def select_task(self, machine, tasks):
        available_tasks = self.get_available_tasks(machine, tasks)
        if len(available_tasks) == 0:
            return self.get_earliest_task(tasks)

        return self.get_earliest_task(available_tasks)

    @staticmethod
    def init_tasks(tasks):
        tasks_list = []
        task_id = 1
        for task in tasks:
            tasks_list.append(Task(task_id, task.duration, task.ready))
            task_id += 1
        return tasks_list

    @staticmethod
    def init_machines(machines_speed):
        machines = []
        machine_id = 1
        for machine_speed in machines_speed:
            machines.append(Machine(machine_id, machine_speed))
            machine_id += 1
        return machines

    def run(self, in_data: Instance) -> Solution:
        current_time = 0.0
        total_flow = 0.0
        tasks = self.init_tasks(in_data.tasks)
        machines = self.init_machines(in_data.machine_speeds)

        available_tasks_left = len(tasks)

        while available_tasks_left > 0:
            available_machines = self.get_available_machines(machines, current_time)
            for machine in available_machines:
                chosen_task = self.select_task(machine, tasks)
                tasks[chosen_task.task_id - 1].mark_finished()
                total_flow += machine.assign_task(chosen_task)
                available_tasks_left -= 1
                if available_tasks_left == 0:
                    break

            current_time = machines[0].machine_time
            for i in range(1, len(machines)):
                if machines[i].machine_time < current_time:
                    current_time = machines[i].machine_time

        order = []
        for machine in machines:
            order.append(machine.schedule)

        schedule = Schedule(len(tasks), len(machines), order)

        return Solution(total_flow / len(tasks), schedule)