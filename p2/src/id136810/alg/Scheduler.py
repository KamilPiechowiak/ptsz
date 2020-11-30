from p2.src.id136810.alg.Job import Job
from p2.src.id136810.alg.Machine import Machine
from p2.src.id136810.alg.Utils import getFirstJobCost, getSecondJobCost, isOverlapping, getClosestBeginMoment
from p2.src.data_api import Instance


class Scheduler:
    def __init__(self, in_data: Instance):
        self.machines_states = [Machine(speed, index) for index, speed in enumerate(in_data.machine_speeds)]
        self.tasks = [Job(task.ready, task.duration, index + 1) for index, task in enumerate(in_data.tasks)]

    def sortTasksByReadyMoment(self):
        self.tasks = sorted(self.tasks, key=lambda task: task.ready_moment)

    def getOverlappingJobs(self, current_job: Job, machine: Machine):
        job_index = self.tasks.index(current_job) + 1
        overlapping = []
        while job_index < len(self.tasks) and isOverlapping(current_job, self.tasks[job_index], machine.speed):
            overlapping.append(self.tasks[job_index])
            job_index += 1
        return overlapping

    def getMachineScheduleRanking(self, current_job: Job):
        schedule_costs = map(lambda machine: (getFirstJobCost(current_job, machine), machine), self.machines_states)
        schedule_costs = sorted(schedule_costs, key=lambda cost_machine: cost_machine[0])
        return [cost_machine[1] for cost_machine in schedule_costs]

    def getBestMachine(self, current_job: Job, current_machine: Machine):
        overlapping = self.getOverlappingJobs(current_job, current_machine)
        picked_machine = current_machine
        for overlapping_job in overlapping:
            loss = getFirstJobCost(current_job, picked_machine) + getSecondJobCost(current_job, overlapping_job, picked_machine)
            overlapping_machine_ranking = self.getMachineScheduleRanking(overlapping_job)
            if overlapping_machine_ranking[0] == picked_machine:
                basic_loss = getFirstJobCost(overlapping_job, picked_machine)
                for machine_alternative in overlapping_machine_ranking[1::]:
                    loss_alternative = basic_loss + getFirstJobCost(current_job, machine_alternative)
                    if loss_alternative < loss:
                        picked_machine = machine_alternative
                        loss = loss_alternative
        return picked_machine

    def schedule(self, job: Job, machine: Machine):
        task_index = self.tasks.index(job)
        self.tasks[task_index].begin = getClosestBeginMoment(job, machine)
        self.tasks[task_index].end = self.tasks[task_index].begin + job.duration * machine.speed
        machine.schedule(self.tasks[task_index])

    def scheduleJob(self, current_job: Job):
        machines_ranking = self.getMachineScheduleRanking(current_job)
        curr_machine = machines_ranking[0]
        picked_machine = self.getBestMachine(current_job, curr_machine)
        self.schedule(current_job, picked_machine)

    def getFinalSchedule(self):
        finalSchedule = []
        for machine in self.machines_states:
            finalSchedule.append(machine.getSchedule())
        return finalSchedule
