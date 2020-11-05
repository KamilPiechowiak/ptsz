#!/usr/bin/env python3
import sys

LENGTH = 0
READY = 1
DUE = 2
WEIGHT = 3

max_due = 0
max_weight = 0


def read_files(instance_file: str):
    instance_file = open(instance_file, "r+")
    return int(instance_file.readline().rstrip()), [[int(x) for x in line.strip().split(' ')] for line in
                                                    instance_file.readlines()]


def find_next(jobs, current_time, ranked_jobs):
    candidate = None
    max_function_val = -1000
    late_jobs = []
    for i in range(len(jobs)):
        if i + 1 not in ranked_jobs and current_time > jobs[i][READY]:
            function_val = 2 * jobs[i][WEIGHT] / max_weight - jobs[i][DUE] / max_due
            if current_time + jobs[i][LENGTH] > jobs[i][DUE]:
                late_jobs.append(i)
            elif function_val > max_function_val:
                max_function_val = function_val
                candidate = i

    if candidate is None and late_jobs.__len__() != 0:
        candidate = late_jobs.pop()
    return candidate


def rank_jobs(jobs_count, jobs):
    global max_due, max_weight
    for i in range(len(jobs)):
        if jobs[i][DUE] > max_due:
            max_due = jobs[i][DUE]
        if jobs[i][WEIGHT] > max_weight:
            max_weight = jobs[i][WEIGHT]
    ranked_jobs = []
    current_time = 0
    result_criteria = 0
    while jobs_count != ranked_jobs.__len__():
        candidate_index = find_next(jobs, current_time, ranked_jobs)
        if candidate_index is None:
            current_time += 1
        else:
            current_time += jobs[candidate_index][LENGTH]
            if current_time > jobs[candidate_index][DUE]:
                result_criteria += jobs[candidate_index][WEIGHT]
            ranked_jobs.append(candidate_index + 1)
    return result_criteria, ranked_jobs


def main(argv):
    instance_file = argv[0]
    result_file = open(f'seq.out', 'w+')
    jobs_count, jobs = read_files(instance_file)
    criteria, ranked_jobs = rank_jobs(jobs_count, jobs)
    result_file.write(f'{criteria.__str__()}\n')
    for i in range(len(ranked_jobs)):
        result_file.write(f'{ranked_jobs[i].__str__()} ')
    result_file.close()


if __name__ == "__main__":
    main(sys.argv[1:])
