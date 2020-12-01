from typing import List, Any

from p2.src.data_api import Schedule, Instance, Solution
from p2.src.id136810.alg.Job import Job
from p2.src.id136810.alg.Machine import Machine
from p2.src.id136810.validator.Criterium import Criterium


def flatten(list: List[List[Any]]):
    return [element for sublist in list for element in sublist]


def isMomentBetween(start: float, moment: float, end: float):
    return start <= moment < end


def isMomentBefore(moment: float, start: float, end: float):
    return moment <= start and moment < end


def fitsBeforeScheduled(job_duration: float, closest_begin: float, next_begin: float):
    return closest_begin + job_duration <= next_begin


def getClosestBeginMoment(current_job: Job, machine: Machine):
    closest_begin = current_job.ready_moment
    for job in machine.scheduled_jobs:
        if isMomentBefore(current_job.ready_moment, job.begin, job.end):
            if fitsBeforeScheduled(current_job.duration * machine.speed, closest_begin, job.begin):
                return closest_begin
        closest_begin = max(closest_begin, job.end)
    return closest_begin


def getCostAndBegin(job: Job, machine: Machine):
    closest_begin = getClosestBeginMoment(job, machine)
    return closest_begin + job.duration * machine.speed - job.ready_moment, closest_begin


def isOverlapping(current_job: Job, other_job: Job, machine_speed: float, ready: int = -1):
    actual_ready = max(current_job.ready_moment, ready)
    possible_end = actual_ready + current_job.duration * machine_speed
    checkedMoment = other_job.ready_moment + (other_job.duration * machine_speed) / 2
    return isMomentBetween(actual_ready, checkedMoment, possible_end)


def getSolution(in_data: Instance, schedule: List[List[int]]):
    schedule = Schedule(in_data.no_tasks, in_data.no_machines, schedule)
    tmpSolution = Solution(0, schedule)
    criterium = Criterium(in_data, tmpSolution)
    return Solution(criterium.getCriterium(), schedule)
