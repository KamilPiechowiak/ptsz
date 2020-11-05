import time
import sys
import os
import subprocess as sp

INDEX = 0
JOB = 1
LENGTH = 0
READY = 1
DUE = 2
WEIGHT = 3


def sort_by_length(job):
    return job[JOB][READY]/(job[JOB][WEIGHT])


def instance_test_args(instance_file: str):
    if instance_file is None:
        print(f'Invalid argument provided: {instance_file}')
        exit(-1)

    instance_file = open(instance_file, "r+")
    return int(instance_file.readline().rstrip()), [[int(x) for x in line.strip().split(' ')] for line in
                                                    instance_file.readlines()]


def find_candidate(jobs, current_time, late_jobs):
    for indexed_job in jobs:
        if indexed_job[JOB][DUE] - current_time - indexed_job[JOB][LENGTH] < 0:
            late_jobs.append(indexed_job)
            jobs.remove(indexed_job)
    if len(jobs) > 0:
        return jobs[0]
    else:
        return None


def rank_jobs(jobs_count, jobs):
    ranked_jobs = []
    late_jobs = []
    current_time = 0
    result_criteria = 0
    jobs.sort(key=sort_by_length)
    for i in range(jobs_count):
        candidate = find_candidate(jobs, current_time, late_jobs)
        if candidate is None:
            break
        current_time += max(candidate[JOB][READY] - current_time, 0) + candidate[JOB][LENGTH]
        if current_time > candidate[JOB][DUE]:
            result_criteria += candidate[JOB][WEIGHT]
        ranked_jobs.append(candidate[INDEX])
        jobs.remove(candidate)
    for job in late_jobs:
        result_criteria += job[JOB][WEIGHT]
        ranked_jobs.append(job[INDEX])
    return result_criteria, ranked_jobs


def main(argv):
    output = open('seq.out', 'w+')
    instance_file = argv[0]
    jobs_count, jobs = instance_test_args(instance_file)
    indexed_jobs = [[i + 1, jobs[i]] for i in range(len(jobs))]
    criteria, ranked_jobs = rank_jobs(jobs_count, indexed_jobs)
    print(criteria)
    for i in range(len(ranked_jobs)):
        print(ranked_jobs[i], end=' ')


if __name__ == "__main__":
    main(sys.argv[1:])
