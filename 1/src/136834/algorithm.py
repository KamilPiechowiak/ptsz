from itertools import permutations
import random
import sys
from task import Schedule, read_instance

def dummy_schedule(jobs):
    schedule = Schedule(jobs)
    schedule.order = list(range(len(schedule.tasks)))
    return schedule

def random_schedule(jobs):
    schedule = dummy_schedule(jobs)
    random.shuffle(schedule.order)
    return schedule

def fcfs(jobs):
    schedule = Schedule(jobs)
    time = 0
    jobs.sort(key=lambda job: job.ready_time)
    schedule.order = [job.number for job in jobs]
    return schedule

def ready_time(jobs):
    schedule = Schedule(jobs)
    time = 0
    jobs.sort(key=lambda job: job.ready_time)

    order = []
    not_used = []
    for job in jobs:
        time = max(time, job.ready_time)
        if time + job.processing_time > job.due_time:
            not_used.append(job.number)
        else:
            order.append(job.number)
            time += job.processing_time
    order.extend(not_used)
    schedule.order = order
    return schedule

def compute_start_times(order, start_time=0):
    time = start_time
    for job in order:
        time = max(job.ready_time, time)
        job.start_time = time
        time += job.processing_time

def weighted_number_of_late_task(order):
    result = 0
    for job in order:
        if job.end_time > job.due_time:
            result += job.weight
    return result



def try_permutations(jobs, start_time):
    best_job = jobs[0]
    best_result = int(1e12)
    for permutation in permutations(jobs):
        compute_start_times(permutation, start_time)
        result = weighted_number_of_late_task(permutation)
        if result < best_result:
            best_result = result
            best_job = permutation[0]
        if result == 0:
            break
    return best_job

def get_available(jobs, time, look_ahead=0):
    return [job for job in jobs 
        if job.ready_time <= time + look_ahead
            and time + job.processing_time <= job.due_time]

def sort_available(jobs, key):
    schedule = Schedule(jobs)

    k = 5
    order = []
    time = 0
    while True:
        available = get_available(jobs, time)
        if len(available) == 0:
            ready_times = [job.ready_time for job in jobs if job.ready_time >= time]
            if len(ready_times) == 0:
                break
            time = min(ready_times)
            available = get_available(jobs, time)
        available.sort(key=key)
        job = try_permutations(available[:k], time)
        order.append(job.number)
        time += job.processing_time
        jobs.remove(job)

    order.extend([job.number for job in jobs])
    schedule.order = order
    return schedule

def weight_first(jobs):
    return sort_available(jobs, key=lambda job: -job.weight)

def shortest_processing_time(jobs):
    return sort_available(jobs, key=lambda job: job.processing_time)

def weight_by_processing_time(jobs):
    return sort_available(jobs, key=lambda job: - float(job.weight) / job.processing_time)

def weight_processing_time_sum(jobs):
    return sort_available(jobs, key=lambda job: job.processing_time - job.weight)

def ready_time_slow(jobs):
    return sort_available(jobs, key=lambda job: job.ready_time)



def compute_move(order):
    move = [0 for job in order]
    move[-1] = order[-1].due_time - order[-1].end_time
    for i in range(len(move) - 2, -1, -1):
        move[i] = min(order[i].due_time - order[i].end_time, 
            order[i + 1].start_time + move[i + 1] - order[i].end_time) 
    return move

def insert(job_to_insert, order):
    if len(order) == 0:
        order.append(job_to_insert)
        job_to_insert.start_time = job_to_insert.ready_time
        return True

    move = compute_move(order)
    time = job_to_insert.ready_time
    for i, job in enumerate(order):
        if job.end_time <= job_to_insert.ready_time:
            continue
        if time + job_to_insert.processing_time > job_to_insert.due_time:
            break
        if time + job_to_insert.processing_time <= job.start_time + move[i]:
            order.insert(i, job_to_insert)
            compute_start_times(order)
            return True
        time = max(time, job.end_time)

    # Insert at the end
    if time + job_to_insert.processing_time <= job_to_insert.due_time:
        order.append(job_to_insert)
        job_to_insert.start_time = time
        return True

    return False

def insertion(jobs, key):
    schedule = Schedule(jobs)
    jobs.sort(key=key)

    order = []
    not_used = []
    for job in jobs:
        inserted = insert(job, order)
        if not inserted:
            not_used.append(job)

    order.extend(not_used)
    schedule.order = [job.number for job in order]
    return schedule

def insertion_weight_by_processing_time(jobs):
    return insertion(jobs, key=lambda job: -float(job.weight) / job.processing_time)

def insertion_weight(jobs):
    return insertion(jobs, key=lambda job: -job.weight)

def insertion_processing_time(jobs):
    return insertion(jobs, key=lambda job: job.processing_time)

def insertion_weight_processing_time_sum(jobs):
    return insertion(jobs, key=lambda job: job.processing_time - job.weight)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        input_file = open(sys.argv[1])
    else:
        input_file = sys.stdin

    instance = read_instance(input_file)
    schedule = insertion_weight_by_processing_time(instance)
    schedule.validate()
    print(schedule)
