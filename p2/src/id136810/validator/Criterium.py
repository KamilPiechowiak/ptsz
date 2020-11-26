from p2.src.data_api import Instance, Solution

class Criterium:
    def __init__(self, instance: Instance, output: Solution):
        self.size = instance.no_tasks
        self.tasks = instance.tasks
        self.speeds = instance.machine_speeds
        self.schedule = output.schedule

    def getCriterium(self):
        criterium = 0
        for i in range(0, len(self.speeds)):
            currMoment = 0
            for task_no in self.schedule[i]:
                readyTime = self.tasks[task_no - 1].ready
                if currMoment < readyTime:
                    currMoment = readyTime
                duration = self.tasks[task_no - 1].duration * self.speeds[i]
                currMoment += duration
                criterium += currMoment - readyTime
        return criterium / self.size
