from src.data_api import Task
from typing import List

from src.id136810.alg.Job import Job


class Scheduler:
    def __init__(self, tasks: List[Task]):
        self.mach_moments = [0, 0, 0]
        self.jobList = [Job(task, index) for index, task in enumerate(tasks)]

    def scheduleSingleTask(self, task, subtask):
        cost1 = self.getCost(task, self.mach_moments)
        cost2 = self.getCost(subtask, self.mach_moments)

        gap12 = self.getSumGaps(task, subtask) * subtask.weight
        gap21 = self.getSumGaps(subtask, task) * task.weight

        diffGaps = gap12 - gap21
        diffCosts = cost1 - cost2

        if diffGaps + diffCosts > 0:
            return 0
        else:
            return 1


    def getCost(self, task, machine_moments):
        end_moment = self.getMomentsAfterSchedule(task, machine_moments)[2]
        return (end_moment - task.due_date) * task.weight

    def getSumGaps(self, task: Task, subtask: Task):
        startingMach1Gap = task.duration[0]
        mach2Gap = startingMach1Gap + task.duration[0] + subtask.duration[0] - task.duration[0] + task.duration[1]

        startingMach2Gap = task.duration[0] + task.duration[1]
        mach3Gap = startingMach2Gap + task.duration[0] + task.duration[1] + mach2Gap + subtask.duration[1] - \
                   task.duration[0] + task.duration[1] + task.duration[2]
        return mach2Gap + mach3Gap

    def getMomentsAfterSchedule(self, job: Job, current_moments):
        updated = current_moments.copy()
        for index, mach_moment in enumerate(current_moments):
            if index == 0:
                updated[index] += job.duration[index]
            else:
                first_machine_moment = updated[index - 1] + job.duration[index]
                curr_machine_moment = updated[index] + job.duration[index]
                updated[index] = max(first_machine_moment, curr_machine_moment)
        return updated

    def schedule2(self):
        noJobs = len(self.jobList)

        tmp_mach_moments = self.mach_moments.copy()
        tmp_job_list = self.jobList.copy()

        currentIndex = 0
        currentJob = tmp_job_list[currentIndex]
        checkedIndex = currentIndex + 1

        while currentIndex < noJobs - 1:
            while checkedIndex < noJobs and self.canSwap(currentJob, tmp_job_list[checkedIndex], tmp_mach_moments):
                tmp_mach_moments = self.getMomentsAfterSchedule(tmp_job_list[checkedIndex], tmp_mach_moments)
                tmp_job_list[checkedIndex], tmp_job_list[checkedIndex - 1] \
                    = tmp_job_list[checkedIndex - 1], tmp_job_list[checkedIndex]
                checkedIndex += 1
            if currentIndex + 1 == checkedIndex:
                tmp_mach_moments = self.getMomentsAfterSchedule(currentJob, tmp_mach_moments)
                self.jobList = tmp_job_list.copy()
                self.mach_moments = tmp_mach_moments.copy()
                currentIndex += 1
            currentJob = tmp_job_list[currentIndex]
            checkedIndex = currentIndex + 1
            tmp_mach_moments = self.mach_moments.copy()
        return self.jobList

    def canSwap(self, currentJob: Job, checkedJob: Job, tmp_mach_moments):
        currCost = self.getCost(currentJob, tmp_mach_moments)
        no_swap_moments = self.getMomentsAfterSchedule(currentJob, tmp_mach_moments)
        no_swap_checked_cost = self.getCost(checkedJob, no_swap_moments)

        checkedCost = self.getCost(checkedJob, tmp_mach_moments)
        swap_moments = self.getMomentsAfterSchedule(checkedJob, tmp_mach_moments)
        swap_curr_cost = self.getCost(currentJob, swap_moments)

        no_swap_cost = currCost + no_swap_checked_cost
        swap_cost = checkedCost + swap_curr_cost
        return swap_cost < no_swap_cost

    def init_sort(self):
        self.jobList.sort(key=lambda x: x.due_date)