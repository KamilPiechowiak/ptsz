from p3.src.data_api import Instance, Task
from p3.src.generator_api import Generator

import math
import numpy as np


class Generator126828(Generator):

    def generate(self, no_tasks: int, no_machines: int) -> Instance:
        """
        Generate instance with:
        number of tasks == no_tasks == [50,500,50]
        number of machines == no_machines == 3
        Tasks where task contains duration time for every machine - p_j.i deadline - dj and wage - wj
        We minimize average delay Dw = sum(j=1..n)wjDj / sum(j=1..n)wj where Dj = max{0,Cj-dj}
        Cj == time where task is finished

        """
        shortTasksFor1stMachine = int(no_tasks / 2)
        shortTasksFor2ndMachine = int(math.ceil(no_tasks / 4))
        shortTasksFor3dMachine = int(math.floor(no_tasks / 4))

        mediumTasksFor1stMachine = int(math.ceil(no_tasks / 4))
        mediumTasksFor2ndMachine = int(math.floor(no_tasks / 4))
        mediumTasksFor3dMachine = int(no_tasks / 2)

        longTasksFor1stMachine = int(math.floor(no_tasks / 4))
        longTasksFor2ndMachine = int(no_tasks / 2)
        longTasksFor3dMachine = int(math.ceil(no_tasks / 4))

        durationMachinesCounters = [[shortTasksFor1stMachine, shortTasksFor2ndMachine, shortTasksFor3dMachine],
                                    [mediumTasksFor1stMachine, mediumTasksFor2ndMachine, mediumTasksFor3dMachine],
                                    [longTasksFor1stMachine, longTasksFor2ndMachine, longTasksFor3dMachine]]
        durationDictionary = {'short': [1, 10], 'medium': [8, 15], 'long': [13, 20]}
        duetimeDictionary = {'early': [int(math.floor(no_tasks / 10)), int(math.ceil(no_tasks / 5))],
                             'lazy': [int(math.ceil(no_tasks / 6)), int(no_tasks/2)],
                             'late': [int(math.ceil(no_tasks / 2)), int(math.ceil(no_tasks * 1.3))]}
        wagesDictionary = {'easy': [1, 15], 'attractive': [10, 22], 'important': [17, 30]}

        def create_task_properties(counter, av_tasks, machine_no, duration_type, dictionary, field):
            if field == 0:
                # duration
                for _ in range(counter):
                    # for random available task for exact machine choose random duration time in range defined in
                    # dictionary
                    taskList[av_tasks[0]].duration[machine_no] = \
                        np.random.randint(dictionary[duration_type][0], dictionary[duration_type][1])
                    # pop from list chosen task index
                    av_tasks.pop(0)
            elif field == 1:
                # due_time
                for _ in range(counter):
                    # for random available task for exact machine choose random duration time in range defined in
                    # dictionary
                    due_time = sum(taskList[av_tasks[0]].duration) + np.random.randint(dictionary[duration_type][0],
                                                                                       dictionary[duration_type][1])
                    index = int(av_tasks[0])
                    task = Task(taskList[index].duration, due_time, 0)
                    taskList[index] = task

                    # pop from list chosen task index
                    av_tasks.pop(0)
            else:
                # wages
                for _ in range(counter):
                    # for random available task for exact machine choose random duration time in range defined in
                    # dictionary
                    weight = \
                        np.random.randint(dictionary[duration_type][0], dictionary[duration_type][1])
                    index = int(av_tasks[0])
                    task = Task(taskList[index].duration, taskList[index].due_date, weight)
                    taskList[index] = task
                    # pop from list chosen task index
                    av_tasks.pop(0)

        # create list of tasks to return
        taskList = [Task([0, 0, 0], 0, 0) for i in range(no_tasks)]
        # print(taskList)
        # for every machine create tasks
        available_tasks = list(range(0, no_tasks))
        for i in range(3):
            task_indexes = available_tasks.copy()
            np.random.shuffle(task_indexes)
            create_task_properties(durationMachinesCounters[0][i], task_indexes, i, 'short', durationDictionary, 0)
            create_task_properties(durationMachinesCounters[1][i], task_indexes, i, 'medium', durationDictionary, 0)
            create_task_properties(durationMachinesCounters[2][i], task_indexes, i, 'long', durationDictionary, 0)

        dueDateCounter = [[int(math.ceil(no_tasks / 4)), 'early'], [int(no_tasks / 2), 'lazy'],
                          [int(math.floor(no_tasks / 4)), 'late']]
        task_indexes = available_tasks.copy()
        np.random.shuffle(task_indexes)
        for i in range(3):
            create_task_properties(dueDateCounter[i][0], task_indexes, i, dueDateCounter[i][1], duetimeDictionary, 1)

        wagesCounter = [[int(math.ceil(no_tasks / 4)), 'easy'], [int(no_tasks / 2), 'attractive'],
                        [int(math.floor(no_tasks / 4)), 'important']]
        task_indexes = available_tasks.copy()
        np.random.shuffle(task_indexes)
        for i in range(3):
            create_task_properties(wagesCounter[i][0], task_indexes, 0, wagesCounter[i][1], wagesDictionary, 2)

        return Instance(no_tasks, no_machines, taskList)
