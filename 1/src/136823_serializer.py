import sys


class Task:
    def __init__(self, task_number, p_i, r_i, d_i, w_i):
        self.id = task_number
        self.p_i = p_i
        self.r_i = r_i
        self.d_i = d_i
        self.w_i = w_i


def print_series(total_latency, tasks_order):
    print(str(total_latency))
    print(" ".join([str(tasks_order[i]) for i in range(len(tasks_order))]))


def get_available_tasks(tasks, time_stamp):
    available_tasks = []
    for task in tasks:
        if task.r_i <= time_stamp:
            available_tasks.append(task)
    return available_tasks


def remove_late_tasks(tasks, time_stamp, late_tasks):
    for task in tasks:
        if task.p_i + time_stamp > task.d_i:
            late_tasks.append(task)
            tasks.remove(task)


def compare(task):
    return task.w_i


def select_task(tasks, time_stamp, late_tasks):
    remove_late_tasks(tasks, time_stamp, late_tasks)
    available_tasks = get_available_tasks(tasks, time_stamp)
    if len(available_tasks) == 0:
        return 0, time_stamp + 1
    selected_task_number = 0
    new_timestamp = time_stamp
    available_tasks.sort(key=compare)
    for task in tasks:
        if task.id == available_tasks[0].id:
            selected_task_number = task.id
            new_timestamp += task.p_i
            tasks.remove(task)
    return selected_task_number, new_timestamp


def get_task(line):
    parameters = line.split(" ")
    return parameters[0], parameters[1], parameters[2], parameters[3]


def serialize_tasks(number_of_tasks):
    tasks = []
    for i in range(number_of_tasks):
        p_j, r_j, d_j, w_j = get_task(input())
        tasks.append(Task(i + 1, int(p_j), int(r_j), int(d_j), int(w_j)))

    order = []
    late_tasks = []
    time_stamp = 0
    while len(tasks) != 0:
        selected_task, time_stamp = select_task(tasks, time_stamp, late_tasks)
        if selected_task == 0:
            continue
        order.append(selected_task)

    total_latency = 0
    for task in late_tasks:
        order.append(task.id)
        total_latency += task.w_i

    print_series(total_latency, order)


def main():
    number_of_tasks = int(input())
    serialize_tasks(number_of_tasks)


if __name__ == "__main__":
    main()