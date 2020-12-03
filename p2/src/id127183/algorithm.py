from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule

from p2.src.id127183.classes.machine import Machine
from p2.src.id127183.classes.task import Task


class Algorithm127183(Algorithm):
    clock, flow_time = 0.0, 0.0
    machines, tasks = [], []

    @staticmethod
    def get_instance_data(machines_list, tasks_list):
        Algorithm127183.machines = [Machine(counter+1, speed) for counter, speed in enumerate(machines_list)]
        Algorithm127183.tasks = [Task(counter+1, task.duration, task.ready) for counter, task in enumerate(tasks_list)]

    @staticmethod
    def sort_lists():
        Algorithm127183.tasks.sort(key=lambda x: (x.ready, x.duration))  # sort by readiness ASC if equal then by duration ASC

    @staticmethod
    def pick_machine():
        free_machines = []
        for machine in Algorithm127183.machines:
            if machine.check_status(Algorithm127183.clock):
                free_machines.append(machine)
        if free_machines == []:
            return None
        else:
            return min(free_machines, key=lambda x: x.speed)

    @staticmethod
    def assign_task():
        for task in Algorithm127183.tasks:
            if task.started == False:
                Algorithm127183.clock = max(Algorithm127183.clock, task.ready)
                task.task_started()
                return task
        return None

    def run(self, in_data: Instance) -> Solution:
        self.get_instance_data(in_data.machine_speeds, in_data.tasks)
        self.sort_lists()
        self.clock, self.flow_time = 0.0, 0.0
        task = self.assign_task()
        while task:
            machine = self.pick_machine()
            if machine != None:
                self.flow_time += machine.add_task(task)
            else:
                ready_machine = min(self.machines, key=lambda x: x.clock)
                self.clock = ready_machine.clock
                self.flow_time += ready_machine.add_task(task)
            task = self.assign_task()
        sequence = [machine.list_of_tasks for machine in self.machines]
        final_sequence = Schedule(len(self.tasks), len(self.machines), sequence)
        mean_flow_time = round(self.flow_time / in_data.no_tasks, 6)
        return Solution(mean_flow_time, final_sequence)
