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


def solve2(instance):
    n = instance.shape[0]
    instance = np.c_[instance, np.arange(n)]
    instance[:, 3] = instance[:, 3] + 1
    mask = (instance[:, 1] + instance[:, 0]) > instance[:, 2]
    rest = np.where(mask)
    keep = np.where(np.logical_not(mask))
    filtered = instance[keep]

    filtered = filtered[np.argsort(filtered[:, 1])]
    end = 0
    deleted = 0
    size = filtered.shape[0]
    for i in np.arange(size):
        end = np.maximum(end, filtered[i-deleted, 1]) + filtered[i-deleted, 0]
        if end > filtered[i-deleted, 2]:
            max_ratio_idx = np.argmax(filtered[:(i-1-deleted), 0] / filtered[:(i-1-deleted), 3])
            rest = np.append(rest, filtered[max_ratio_idx, 4])
            filtered = np.delete(filtered, max_ratio_idx, axis=0)
            deleted += 1
            end = 0
            for j in np.arange(i-deleted):
                end = np.maximum(end, filtered[j, 1]) + filtered[j, 0]
    rest = np.argsort(instance[rest, 1])
    return np.append(filtered[:, 4], rest) + 1

def solve(instance):
    return np.argsort(instance[:, 2]) + 1


if __name__ == "__main__":
    n, instance = load_instance()
    solution = solve(instance)
    objective = objective(instance, solution)
    print_solution(objective, solution)
