import random
import math
import numpy
import statistics
from operator import attrgetter


class Task:
    p = 0
    r = 0

    def __init__(self, p, r):
        self.p = p
        self.r = r

    def __str__(self):
        return str(self.r) + " " + str(self.p)


def generate_task_param(tasks, indices, min_r, max_r, count, val_type=0):
    if val_type == 0:
        for i in range(count):
            r_time = random.randint(min_r, max_r)
            chosen_id = random.randint(0, len(indices) - 1)
            tasks[indices[chosen_id]].r = r_time
            indices.pop(chosen_id)
    else:
        for i in range(count):
            r_time = random.randint(min_r, max_r)
            chosen_id = random.randint(0, len(indices) - 1)
            tasks[indices[chosen_id]].p = r_time
            indices.pop(chosen_id)


def generate(n):
    early_tasks = int(n / 2)
    lazy_tasks = int(math.ceil(n / 4))
    late_tasks = int(math.floor(n / 4))
    short_tasks = int(n / 2)
    medium_tasks = int(math.ceil(n / 4))
    long_tasks = int(math.floor(n / 4))
    print(f'generating file with {n} jobs')
    # pick random index to assing 1 value
    basic = [random.uniform(1, 5) for i in range(5)]
    if statistics.mean(basic) > 3.5:
        max_pos = basic.index(max(basic))
        basic[max_pos] -= 1.0
        # if still too large repeat
        if statistics.mean(basic) > 3.5:
            max_pos = basic.index(max(basic))
            basic[max_pos] -= 1.0
    for i in range(len(basic)):
        basic[i] = round(basic[i], 1)
    if not basic.__contains__(1.0):
        basic[random.randint(0, 4)] = 1.0
    # assign task table
    tasks = [Task(0, 0) for i in range(n)]

    if n > 250:
        # early tasks from time 0 to n/5
        # lazy tasks from n/5 to n
        # late tasks from n to n*1.5
        print('Big instance')
        indices = [i for i in range(n)]
        generate_task_param(tasks, indices, 0, n / 5, early_tasks)
        generate_task_param(tasks, indices, n / 5, n, lazy_tasks)
        generate_task_param(tasks, indices, n, n * 1.5, late_tasks)

        # short_tasks 5 -> 30
        # medium_tasks 30 -> 45
        # long_tasks 45 -> 50
        indices = [i for i in range(n)]
        generate_task_param(tasks, indices, 5, 30, short_tasks, 1)
        generate_task_param(tasks, indices, 30, 45, medium_tasks, 1)
        generate_task_param(tasks, indices, 45, 50, long_tasks, 1)

    else:
        # early tasks from time 0 to 60
        # lazy tasks from 50 to 100
        # late tasks from 90 to 150
        print('Small instance')
        indices = [i for i in range(n)]
        generate_task_param(tasks, indices, 0, 60, early_tasks)
        generate_task_param(tasks, indices, 50, 100, lazy_tasks)
        generate_task_param(tasks, indices, 90, 150, late_tasks)

        # short_tasks 1 -> 20
        # medium_tasks 20 -> 30
        # long_tasks 30 -> 40
        indices = [i for i in range(n)]
        generate_task_param(tasks, indices, 1, 20, short_tasks, 1)
        generate_task_param(tasks, indices, 20, 30, medium_tasks, 1)
        generate_task_param(tasks, indices, 30, 40, long_tasks, 1)

    min_task = min(tasks, key=attrgetter("r"))
    min_task.r = 0
    file = open(f"../../instances/126828_{n}.in", 'w')
    file.write(n.__str__() + "\n")

    s = ' '.join([str(i) for i in basic])
    file.write(s + '\n')
    tasks_string = '\n'.join(task.__str__() for task in tasks)
    file.write(tasks_string)
    file.close()


def main():
    for i in range(50, 501, 50):
        generate(i)


if __name__ == "__main__":
    main()
