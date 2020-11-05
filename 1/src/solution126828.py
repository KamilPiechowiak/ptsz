import sys

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
        tasks.append(Task(i,p,r,d,w))
    sort_tasks()
    timer = 0
    chosen_tasks = []
    late_tasks = []
    available_tasks = tasks
    # print(len(available_tasks))
    #find solution
    for task in tasks:
        if timer + task.p <= task.d:
            chosen_tasks.append(task)
            if timer > task.r:
                timer += task.p
            else:
                timer += task.r + task.p
            available_tasks.remove(task)
        else:
            i_id, dur = find_longest_task(chosen_tasks)
            task1 = chosen_tasks[i_id]
            timer -= chosen_tasks[i_id].p
            task1.is_late = 1
            late_tasks.append(task1)
            chosen_tasks.remove(task1)
            chosen_tasks.append(task)
            if timer > task.r:
                timer += task.p
            else:
                timer += task.r + task.p
            available_tasks.insert(0,task1)
            available_tasks.remove(task)
    solution = 0
    # print(chosen_tasks)
    chosen_tasks += available_tasks
    #print(len(chosen_tasks))
    for t in late_tasks:
        solution += t.w

    #print(f'solution found by counting late tasks {solution}')
    clock = 0
    task_order = ''
    for t in chosen_tasks:
        task_order += f'{t.task_id} '
    #print(f'finished {len(chosen_tasks)} with solution {solution}')
    if len(sys.argv) >= 3:
        solution_file = open(sys.argv[2],'w')
        solution_file.write(f'{solution}\n')
        solution_file.write(task_order)
    else:
        print(solution)
        [print(t.task_id, end=' ') for t in chosen_tasks]


def sort_tasks():
    global tasks
    #print('Sorting tasks')
    tasks.sort(key=lambda task: (task.p + task.r)/(task.w + task.d))

def main():
    if(len(sys.argv) >= 2):
        find_solution(file=open(sys.argv[1]))
    else:
        find_solution(sys.stdin)


if __name__ == "__main__":
    main()