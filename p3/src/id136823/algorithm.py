from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule


class Task:
    def __init__(self, task_id, task_duration, task_due_date, task_weight):
        self.id = task_id
        self.duration = task_duration
        self.due_date = task_due_date
        self.weight = task_weight


class Algorithm136823(Algorithm):

    @staticmethod
    def chose_next_element(tasks, machine_times, average_weight):
        task_values = {}
        for task in tasks:
            task_total_duration = 0
            system_downtime = 0
            for task_duration in task.duration:
                task_total_duration += task_duration
            for i in range(len(machine_times) - 1):
                system_downtime += max(0, machine_times[i] + task.duration[i] - machine_times[i + 1])
            task_values[task.id] = task_total_duration * average_weight - system_downtime * average_weight
        return max(task_values, key=task_values.get)

    @staticmethod
    def get_average_weight(tasks):
        weights_sum = 0
        for task in tasks:
            weights_sum += task.weight
        return weights_sum / len(tasks)

    @staticmethod
    def update_machine_times(machine_times, selected_task):
        task_time = 0
        for i in range(len(machine_times)):
            task_time = max(task_time, machine_times[i]) + selected_task.duration[i]
            machine_times[i] = task_time
        new_machine_times = machine_times
        return new_machine_times

    @staticmethod
    def remove_selected_task(tasks, selected_task):
        for task in tasks:
            if task.id == selected_task:
                tasks.remove(task)
                break

    def run(self, in_data: Instance) -> Solution:
        tasks = [Task(i, in_data.tasks[i].duration, in_data.tasks[i].due_date, in_data.tasks[i].weight) for i in range(len(in_data.tasks))]
        machine_times = [0 for _ in range(in_data.no_machines)]
        average_weight = self.get_average_weight(tasks)
        schedule = []
        total_latency = 0
        weights_sum = 0
        for task in tasks:
            weights_sum += task.weight

        for i in range(in_data.no_tasks):
            selected_task = self.chose_next_element(tasks, machine_times, average_weight)
            self.remove_selected_task(tasks, selected_task)
            schedule.append(selected_task + 1)
            machine_times = self.update_machine_times(machine_times, in_data.tasks[selected_task])
            total_latency += max(0, machine_times[in_data.no_machines - 1] - in_data.tasks[selected_task].due_date) * in_data.tasks[selected_task].weight
        return Solution(total_latency / weights_sum, schedule=Schedule(in_data.no_tasks, schedule))