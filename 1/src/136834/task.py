import sys

class Task:
    def __init__(self, processing_time=0, ready_time=0, due_time=0, weight=0):
        self.number = 0
        self.processing_time = processing_time
        self.ready_time = ready_time
        self.due_time = due_time
        self.weight = weight
        self.start_time = 0
    
    @property
    def end_time(self):
        return self.start_time + self.processing_time

    def __str__(self):
        '''
        Task in format pi, ri, di, wi
        pi - processing time
        ri - ready time
        di - due time
        wi - weight
        '''
        return '{} {} {} {}'.format(
            self.processing_time,
            self.ready_time,
            self.due_time,
            self.weight
        )


def weighted_number_of_late_tasks(schedule):
    result = 0
    for task_num in schedule.order:
        task = schedule.tasks[task_num]
        end_time = task.start_time + task.processing_time
        if end_time > task.due_time:
            result += task.weight
    return result

class Schedule:
    def __init__(self, jobs=[], order=[]):
        self.tasks = tuple(jobs)
        # Indexes from 0 to len(self.tasks) - 1
        self.order = order
        self.evaluation = 0

    def validate(self):
        indexes = list(range(0, len(self.tasks)))
        if sorted(self.order) != indexes:
            raise ValueError('Jobs indexes are not valid')
        # Compute jobs start times
        time = 0
        for task_num in self.order:
            task = self.tasks[task_num]
            time = max(time, task.ready_time)
            task.start_time = time
            time += task.processing_time
        self.evaluation = weighted_number_of_late_tasks(self)

    def __str__(self):
        result = str(self.evaluation) + '\n'
        result += ' '.join([str(num + 1) for num in self.order])
        return result

def tasks_to_string(tasks):
    '''
    Output format:
    Number of tasks n in first line
    Tasks descriptions in next n lines, ending in newline
    '''
    lines = [str(task) for task in tasks]
    return '{}\n{}\n'.format(str(len(tasks)), '\n'.join(lines))

def read_instance(file):
    n = file.readline()
    tasks = []
    for i, line in enumerate(file):
        line_numbers = [int(num) for num in line.split()]
        task = Task(*line_numbers)
        task.number = i
        tasks.append(task)
    return tasks

def read_schedule(file, tasks):
    '''
    Input format:
    Value of cost function
    Sequence of task numbers
    '''
    schedule = Schedule()
    schedule.tasks = tasks

    cost = file.readline()
    order = file.readline().split(' ')
    schedule.evaluation = int(cost)
    schedule.order = [int(num) - 1 for num in order]

    return schedule

def visualize_instance(tasks):
    READY, DUE = 0, 1
    events = []
    for task in tasks:
        events.append((task.ready_time, READY, task.number))
        events.append((task.due_time, DUE, task.number))
    events.sort()
    for i in range(0, events[-1][0] + 1):
        print(i, end=' ')
        while len(events) > 0 and events[0][0] == i:
            task = tasks[events[0][2]]
            task_string = '{}({})'.format(task.number, task.processing_time)
            if events[0][1] == READY:
                print('R' + task_string, end=' ')
            else:
                print('D' + task_string, end=' ')
            events.pop(0)
        print()

if __name__ == "__main__":
    instance = read_instance(sys.stdin)
    visualize_instance(instance)
