import sys
import time

class Task:
    #task id
    task_id = 0
    # duration
    p = 0
    # readyTime
    r = 0
    # deadline
    d = 0
    # wage
    w = 0
    #is_late task
    is_late = 0

    def __init__(self,t_id, p, r, d, w):
        self.task_id = int(t_id)
        self.p = int(p)
        self.r = int(r)
        self.d = int(d)
        self.w = int(w)
        self.is_late = 0

    def __repr__(self):
        return repr((self.task_id, self.p, self.r,self.d,self.w))

    def __str__(self):
        return '{0}| {1} {2} {3} {4}'.format(self.task_id,self.p, self.r, self.d, self.w)

tasks =[]

def load_task(file_line):
    params = file_line.split()
    return params[0],params[1],params[2],params[3]

def find_longest_task(tasks):
    maxtime = (0, 0)
    for i in range(len(tasks)):
        id,time = maxtime
        if tasks[i].p > time:
            maxtime = (i, tasks[i].p)
    return maxtime


def count_solution(task_list):
    foundSolution = 0
    clock = 0
    for task in task_list:
        # first task setup clock
        if task == task_list[0]:
            clock = task.r + task.p
        else:
            # increment our clock by task time duration
            if clock < task.r:
                # if taks is not ready, we must wait, assign to clock ready value plus duration time
                clock = task.r + task.p
            else:
                # else increment our clock by task time duration
                clock += task.p

        # if our clock is greater than deadline, task is late
        if clock > task.d:
            foundSolution += task.w

    return foundSolution

def find_solution(file):
    size = int(file.readline())
    global tasks
    for i in range(size):
        p,r,d,w = load_task(file.readline())
        tasks.append(Task(i+1,p,r,d,w))
    sort_tasks()
    timer = 0
    solution = 0
    # print(len(available_tasks))
    #for every task in list check if he can manage before deadline
    for task in tasks:
        #check if task is ready if not set timer to it.
        if timer < task.r:
            timer = task.r +task.p
        else:
            timer = timer + task.p
        #if he can, add him to chosen list, increment timer
        if timer > task.d:
            solution = solution + task.w


    # print(chosen_tasks)
    #print(len(chosen_tasks))
    #print(f'solution found by counting late tasks {solution}')
    task_order = ''
    for t in tasks:
        task_order += f'{t.task_id} '
    #print(f'finished {len(chosen_tasks)} with solution {solution}')
    if len(sys.argv) >= 3:
        solution_file = open(sys.argv[2],'w')
        solution_file.write(f'{solution}\n')
        solution_file.write(task_order)
    else:
        print(solution)
        [print(t.task_id, end=' ') for t in tasks]


def sort_tasks():
    global tasks
    #print('Sorting tasks')
    tasks.sort(key=lambda task: (task.p + task.r)/(task.w + task.d))

def main():
    timest = time.time()
    if(len(sys.argv) >= 2):
        find_solution(file=open(sys.argv[1]))
        # print(f'\n{(time.time() - timest)*1000}')
    else:
        find_solution(sys.stdin)
        # print(f'\n{(time.time() - timest)*1000}')


if __name__ == "__main__":
    main()