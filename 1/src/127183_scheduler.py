import nltk
import sys
import numpy as np


def read_instance():
    n = int(sys.stdin.readline())
    jobs = np.loadtxt(sys.stdin, dtype=np.int)
    return n, jobs


def tokenize_jobs(jobs):
    indexes, tokenized_jobs = [], []
    for i in range(1, len(jobs)+1):
        indexes.append(i)
        tokenized_jobs.append(nltk.word_tokenize(jobs[i-1]))
    initial_jobs_dictionary = dict(zip(indexes, tokenized_jobs))
    return initial_jobs_dictionary


def remove_tardy_jobs(initial_jobs_dictionary):
    jobs_dictionary = initial_jobs_dictionary.copy()
    removed_indexes = []
    for index in jobs_dictionary:
        p, r, d = int(jobs_dictionary[index][0]), int(
            jobs_dictionary[index][1]), int(jobs_dictionary[index][2])
        if(p + r > d):
            removed_indexes.append(index)
    for index in removed_indexes:
        jobs_dictionary.pop(index)
    return jobs_dictionary, removed_indexes


def sort_jobs(jobs_dictionary):
    sorted_jobs_dictionary = sorted(jobs_dictionary.items(
    ), key=lambda x: float(x[1][3])/(float(x[1][1])+float(x[1][0])), reverse=True)
    return sorted_jobs_dictionary


def get_weighted_tardiness(sorted_jobs, i_j_d, removed_indexes):
    tardiness_indicator, timer = 0, 0
    for job in sorted_jobs:
        p, r, d, w = int(job[1][0]), int(
            job[1][1]), int(job[1][2]), int(job[1][3])
        if(timer < r):
            timer = r
        timer += p
        if(timer > d):
            tardiness_indicator += w
    for index in removed_indexes:
        w = int(i_j_d[index][3])
        tardiness_indicator += w
    return tardiness_indicator


def write_output(sorted_jobs, i_j_d, removed_indexes, n):
    tardiness_indicator = get_weighted_tardiness(
        sorted_jobs, i_j_d, removed_indexes)
    print(tardiness_indicator)
    for job in sorted_jobs:
        index = job[0]
        print(index, end=' ')
    for index in removed_indexes:
        print(index, end=' ')


if __name__ == "__main__":
    n, jobs = read_instance()
    initial_jobs_dictionary = tokenize_jobs(jobs)
    jobs_dictionary, removed_indexes = remove_tardy_jobs(
        initial_jobs_dictionary)
    sorted_jobs = sort_jobs(jobs_dictionary)
    write_output(sorted_jobs, initial_jobs_dictionary,
                 removed_indexes, n)
