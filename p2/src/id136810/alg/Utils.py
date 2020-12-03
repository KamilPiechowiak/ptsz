from typing import List, Any

from p2.src.data_api import Schedule, Instance, Solution
from p2.src.id136810.alg.Job import Job
from p2.src.id136810.alg.Machine import Machine
from p2.src.id136810.validator.Criterium import Criterium


def flatten(input_list: List[List[Any]]):
    return [element for sublist in input_list for element in sublist]


def isMomentBetween(start: float, moment: float, end: float):
    return start <= moment < end


def getClosestBeginMoment(current_job: Job, machine: Machine):
    return max(machine.end_moment, current_job.ready_moment)


def getSecondJobCost(current_job: Job, other_job: Job, machine: Machine):
    start = getClosestBeginMoment(current_job, machine)
    end = start + current_job.duration * machine.speed
    loss = end + other_job.duration * machine.speed - other_job.ready_moment
    return loss


def getFirstJobCost(job: Job, machine: Machine):
    closest_begin = getClosestBeginMoment(job, machine)
    return closest_begin + job.duration * machine.speed - job.ready_moment


def isOverlapping(current_job: Job, other_job: Job, machine_speed: float):
    actual_ready = current_job.ready_moment
    possible_end = actual_ready + current_job.duration * machine_speed
    checkedMoment = other_job.ready_moment + (other_job.duration * machine_speed) / 4
    #checkedMoment = other_job.ready_moment
    return isMomentBetween(actual_ready, checkedMoment, possible_end)


def getSolution(in_data: Instance, schedule: List[List[int]]):
    schedule = Schedule(in_data.no_tasks, in_data.no_machines, schedule)
    tmpSolution = Solution(0, schedule)
    criterium = Criterium(in_data, tmpSolution)
    return Solution(criterium.getCriterium(), schedule)
