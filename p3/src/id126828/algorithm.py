import sys

from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule
from p3.src.id126828.evaluator import Evaluator126828


def find_best_task_by_due_date_duration(tasks, clock):
    best_solution = sys.maxsize
    best_task = None
    sol = 0
    id_list = 0
    for id_in_list, (task_id, task) in enumerate(tasks):
        # count acc clock for task
        task_finish_time = clock + sum(task.duration)
        # check task Dj
        task_sol = task.weight * max(0, task_finish_time - task.due_date)
        if task_sol == 0:
            id_list = id_in_list
            sol = task_sol
            best_task = task_id
            break
        # check value of solution for task if its less than
        if task_sol < best_solution:
            id_list = id_in_list
            sol = task_sol
            best_task = task_id

    return id_list, sol, best_task


def add_rest_tasks_to_schedule(tasks, schedule, solution, clock):
    for tasks_id, task in tasks:
        schedule.append(tasks_id)
        clock += sum(task.duration)
        solution += task.weight * max(0, clock - task.due_date)


class Algorithm126828(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        """ 
        0. Reduce searched tasks by tasks with weight less than some parameters ( weight, due date)
        1. Sort available tasks by due date and then weight
        2. for every task find one with best score
        3. add this to solution
        4. 
        """
        tasks_with_id = list(enumerate(in_data.tasks, 1))
        # print(' ======================= ')
        # print([t[0] for t in tasks_with_id], end='\n')

        tasks_with_id.sort(key=lambda t: (t[1].due_date, -t[1].weight))
        # print(' ======================= \n'
        #       'sorted tasks with id\'s')
        # print([t[0] for t in tasks_with_id], end='\n')
        # sort out tasks with high due_date and low weight or with no weight
        less_important_tasks = list(filter(lambda task: task[1].weight < 20, tasks_with_id))
        # print(' ======================= \n'
        #       'less important tasks ')
        # print([t[0] for t in less_important_tasks], end='\n')
        # take all tasks with weight != 0 which have higher weight and due date isn't high
        tasks_to_proceed = list(filter(lambda task: task[1].weight >= 20, tasks_with_id))
        # print(' ======================= \n'
        #       'tasks to proceed')
        # print([t[0] for t in tasks_to_proceed], end='\n')
        schedule_by_id = []
        solution = 0
        clock = 0
        while len(tasks_to_proceed) > 0:
            # find best fitting
            id_in_list, partial_solution, best_task_id = find_best_task_by_due_date_duration(tasks_to_proceed,
                                                                                             clock)
            # add to solution  new values
            solution += partial_solution
            schedule_by_id.append(best_task_id)
            # increase clock and remove chosen task from available
            clock += sum(tasks_to_proceed[id_in_list][1].duration)
            tasks_to_proceed.pop(id_in_list)

        add_rest_tasks_to_schedule(less_important_tasks, schedule_by_id, solution, clock)

        schedule = Schedule(in_data.no_tasks, schedule_by_id)
        #solution = solution / sum([t[1].weight for t in tasks_with_id])
        solution = Evaluator126828().evaluate(in_data,Solution(0.0, schedule)).value
        return Solution(solution, schedule=schedule)
