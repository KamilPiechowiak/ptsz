#!/usr/bin/env python3
import sys
import numpy as np


def load_instance():
    n = int(sys.stdin.readline())
    instance = np.loadtxt(sys.stdin, dtype=np.int)
    return n, instance


def print_solution(objective, solution):
    np.savetxt(sys.stdout, solution.reshape((1, solution.shape[0])), fmt='%i', header=str(objective), comments='')


def objective(instance, solution):
    instance = instance[solution - 1]
    end = 0
    objective = 0
    for task in instance:
        end = np.maximum(end, task[1]) + task[0]
        objective += int(end > task[2]) * task[3]
    return objective


def solve(instance):
    P = 0; R = 1; D = 2; W = 3; I = 4
    n = instance.shape[0]
    tmp = np.zeros((n, 5), dtype=int)
    tmp[:, :-1] = instance
    tmp[:, -1] = np.arange(n)
    instance = tmp
    ratio = instance[:, W]/instance[:, P]
    instance = instance[np.argsort(instance[:, R])]
    rejected = instance[:, R] + instance[:, P] > instance[:, D]
    C = 0
    for i, job in enumerate(instance):
        if rejected[i]:
            continue
        C = np.maximum(C, instance[i, R]) + instance[i, P]
        if C > instance[i, D]:
            max_ratio = ratio[0]
            max_ratio_idx = 0
            for j, r in enumerate(ratio[:i]):
                if rejected[j]:
                    continue
                if r > max_ratio:
                    max_ratio = r
                    max_ratio_idx = j
            rejected[max_ratio_idx] = True
            C = 0
            for k in np.arange(i):
                if rejected[k]:
                    continue
                C = np.maximum(C, instance[k, R]) + instance[k, P]

    accepted = np.logical_not(rejected)
    return np.append(instance[accepted, I], instance[rejected, I]) + 1



if __name__ == "__main__":
    n, instance = load_instance()
    solution = solve(instance)
    test = np.sort(solution)
    objective = objective(instance, solution)
    print_solution(objective, solution)
