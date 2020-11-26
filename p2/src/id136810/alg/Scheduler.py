from typing import List

from p2.src.id136810.alg.Job import Job
from p2.src.id136810.alg.Machine import Machine
from p2.src.id136810.alg.Utils import isMomentBetween, getCostAndBegin, isOverlapping
from p2.src.data_api import Instance


class Scheduler():
    def __init__(self, in_data: Instance):
        self.machines_states = [Machine(speed, index) for index, speed in enumerate(in_data.machine_speeds)]
        self.tasks = [Job(task.ready, task.duration, index + 1) for index, task in enumerate(in_data.tasks)]

    def getJobAtMoment(self, moment: float, machine: Machine):
        if machine.end_moment <= moment:
            return False
        for job in machine.scheduled_jobs:
            if isMomentBetween(job.begin, moment, job.end):
                return job
        return False

    def getOverlappingJobs(self, current_job: Job, machine: (int, Machine)):
        job_index = self.tasks.index(current_job) + 1
        overlapping = []
        while isOverlapping(current_job, self.tasks[job_index], machine[1].speed):
            overlapping.append(self.tasks[job_index])
            job_index += 1
        return overlapping
        #FINISH IMPLEMENTATION

    def sortByReadyMoment(self):
        self.tasks = sorted(self.tasks, key=lambda task: task.ready_moment)

    #checks which machine is the best to schedule job as next
    def getMachineScheduleRanking(self, current_job: Job):
        schedule_costs = []
        for machine in self.machines_states:
            schedule_costs.append(getCostAndBegin(current_job, machine))
        return [(costAndBegin[1], machine) for costAndBegin, machine in sorted(zip(schedule_costs, self.machines_states), key=lambda zipped: zipped[0])]

    def canScheduleJob(self, current_job: Job, overlapping_job: Job, machine: (int, Machine)):
        overlap_cost, overlap_ready = getCostAndBegin(overlapping_job, machine[1])
        current_advantage = overlapping_job.ready_moment - machine[0]
        return overlapping_job.duration - current_job.duration + current_advantage >= 5

    def schedule(self, job: Job, machine: (int, Machine)):
        task_index = self.tasks.index(job)
        self.tasks[task_index].begin = machine[0]
        self.tasks[task_index].end = machine[0] + job.duration * machine[1].speed
        machine[1].schedule(self.tasks[task_index])

    def scheduleJob(self, current_job: Job):
        machines_ranking = self.getMachineScheduleRanking(current_job)
        self.schedule(current_job, machines_ranking[0])

    def getFinalSchedule(self):
        finalSchedule = []
        for machine in self.machines_states:
            finalSchedule.append(machine.getSchedule())
        return finalSchedule
