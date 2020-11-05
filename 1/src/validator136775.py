import argparse
import random
import subprocess

import numpy as np
from io import StringIO

import time


class Validator:

    def __init__(self, no_evaluations=2000):
        self.no_evaluations = no_evaluations

    def __max_score(self, tasks):
        score = 0
        for id in range(len(tasks)):
            p, r, d, w = tasks[id]
            score += w
        return score

    def __score(self, tasks, permut):
        time = 0
        score = 0
        for id in permut:
            p, r, d, w = tasks[id - 1]
            if time < r:
                time = r + p
            else:
                time += p
            if time > d:
                score += w
        return score

    def __parse_task(self, instance_path):
        with open(instance_path) as file:
            n = int(file.readline())
            tasks = list(map(lambda t: list(map(int, t)), map(str.split, file.readlines())))

            assert n == len(tasks)
            return tasks, n

    def __parse_result(self, results):
        wu = int(results[0])
        permut = list(map(int, results[1].split(' ')))
        return permut, wu

    def __parse_result_file(self, output_path):
        with open(output_path) as file:
            return self.__parse_result(file.readlines())

    def evaluate_instance(self, instance_path):
        tasks, n = self.__parse_task(instance_path)

        base_permut = np.arange(1, n + 1)
        evals = np.arange(0, self.no_evaluations)
        evals = list(map(lambda _: self.__score(tasks, np.random.permutation(base_permut)), evals))
        mx = self.__max_score(tasks)
        mn = np.min(evals)
        avg = np.average(evals)
        stdev = np.std(evals)
        print(f'{instance_path}: max={mx}, stdev={stdev / mx}, max-best={(mx - mn) / mx}, max-avg={(mx - avg) / mx}')

    def __is_correct_permut(self, permut):
        n = len(permut)
        flags = np.zeros(n, dtype=bool)
        for i in range(0, n):
            flags[permut[i] - 1] = True

        return all(flags)

    def validate_result(self, instance_path, output_path):
        correct = False
        score = -1

        try:
            tasks, n = self.__parse_task(instance_path)
            permut, wu = self.__parse_result_file(output_path)

            score = self.__score(tasks, permut)
            correct_permut = self.__is_correct_permut(permut)
            correct = correct_permut and n == len(permut) and score == wu
        except:
            correct = False

        print(f'{1 if correct else 0} {score}')

    def validate_algorithm(self, instance_path, cmd):
        correct = False
        score = -1
        total_time = -1

        try:
            tasks, n = self.__parse_task(instance_path)

            start_time = time.time()
            res_output = subprocess.check_output([*cmd.split(' '), instance_path]).decode("utf-8")
            total_time = time.time() - start_time

            permut, wu = self.__parse_result(res_output.split('\n'))

            score = self.__score(tasks, permut)
            correct_permut = self.__is_correct_permut(permut)
            correct = correct_permut and n == len(permut) and score == wu

        except:
            correct = False

        print(f'{1 if correct else 0} {score} {total_time*1000}', end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('mode')
    parser.add_argument('output')
    parser.add_argument('by', nargs='?', default=50, type=int)
    args = parser.parse_args()

    random.seed(0xB16B00B5)

    val = Validator()
    if args.mode == 'i':
        for i in range(int(args.input), int(args.output), args.by):
            val.evaluate_instance(f'1/instances/136775_{i}.in')
    elif args.mode == 'o':
        val.validate_result(args.input, args.output)
    elif args.mode == 'p':
        val.validate_algorithm(args.input, args.output)
