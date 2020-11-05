import sys
class Task:
    # duration
    p = 0
    # readyTime
    r = 0
    # deadline
    d = 0
    # wage
    w = 0

    def __init__(self, p, r, d, w):
        self.p = int(p)
        self.r = int(r)
        self.d = int(d)
        self.w = int(w)

    def __str__(self):
        return '{0} {1} {2} {3}'.format(self.p, self.r, self.d, self.w)

size = 50
ind = '136775'
instancePath = f'../instances/{ind}_{size}.in'
solutionPath = f'seqTest.out'
# array of tasks read from file
tasks = []
solution = 0
orderOfTasks = []

def readInstance():
    file = open(instancePath)
    size = file.readline()
    readLines = file.readlines()
    for line in readLines:
        splitLine = line.split(" ")
        splitLine = splitLine[:4]
        p,r,d,w = splitLine
        task = Task(p, r, d, w)
        tasks.append(task)
    print("Read File")
    # [print(t) for t in tasks]
    file.close()

def readSolution():
    file = open(solutionPath)
    global solution
    solution = int(file.readline())
    global orderOfTasks
    orderOfTasks= [t for t in file.readline().split(" ")]
    orderOfTasks.pop()
    # print(solution)
    print("Read Solution File")
    file.close()


def validate():
    print("Start validating")

def sortTasks():
    global orderOfTasks
    print("Sorting tasks")
    tempTasks = []
    for i in orderOfTasks:
        print(f"Add {i}th task")

        tempTasks.append(tasks[int(i)])
    print("New order of tasks: ")
    #[print(t) for t in tempTasks]


def checkRetrasar():
    # actualTime = 0
    # foundSolution = 0
    # complitionTimes = []
    # for task in tasks:
    #     if task == tasks[0]:
    #         newTime = task.r + task.p
    #
    #     # print(f'Checking {task} with time {newTime}')
    #     if newTime > task.d:
    #         #there is retrasar
    #         # print(f'task {task} is late')
    #         foundSolution +=  task.w
    #     if task != tasks[0]:
    #         newTime += task.p
    #     elif newTime < task.r:
    #         newTime = task.r + task.p
    #     complitionTimes.append(newTime)
    #     actualTime = newTime
    #     # print(actualTime)
    # print(f'all tasks checked; solution found: {foundSolution}')
    # print(complitionTimes)
    global tasks
    foundSolution = 0
    clock = 0
    for task in tasks:
        #first task setup clock
        if task == tasks[0]:
            clock = task.r + task.p
        else:
            #increment our clock by task time duration
            if clock < task.r:
                #if taks is not ready, we must wait, assign to clock ready value plus duration time
                clock = task.r + task.p
            else:
                #else increment our clock by task time duration
                clock += task.p

        #if our clock is greater than deadline, task is late
        if clock > task.d:
            foundSolution += task.w



    return foundSolution


if __name__ == '__main__':
    # if len(sys.argv) != 4:
    #     print('bad number of arguments')
    #     exit(-1)
    # instancePath = sys.argv[1]
    # o = sys.argv[2]
    # solutionPath = sys.argv[3]

    #Read file with problem instance
    readInstance()
    #Read solution File
    readSolution()
    #Sort our instances by solution file
    sortTasks()
    solutionFound = checkRetrasar()
    print(f'{solution};{solutionFound}')
    if solutionFound == solution:
        print('Validation successful')
    else:
        print('Validation failed')


