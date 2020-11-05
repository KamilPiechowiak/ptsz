import itertools
import sys

import numpy as np

P_I = 0
R_I = 1
D_I = 2
W_I = 3


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

    def is_correct_permut(self, permut):
        n = len(permut)
        flags = np.zeros(n, dtype=bool)
        for i in range(0, n):
            flags[permut[i] - 1] = True

        return all(flags)

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
        print(
            f'{instance_path}: max={mx}, min={mn}, stdev={stdev / mx}, max-best={(mx - mn) / mx}, max-avg={(mx - avg) / mx}')


def __max_score(tasks):
    score = 0
    for id in range(len(tasks)):
        p, r, d, w = tasks[id]
        score += w
    return score


def __score_func(tasks):
    def __score(permut):
        time = 0
        score = 0
        for id in permut:
            p, r, d, w = tasks[id - 1]
            time = max(r, time) + p
            if time > d:
                score += w
        return score

    return __score


def __parse_task():
    import fileinput
    import io

    string = []
    for line in fileinput.input():
        string.append(line)
    string = ''.join(string)
    string = io.StringIO(string)
    with string as file:
        n = int(file.readline())
        tasks = list(map(lambda t: list(map(int, t)), map(str.split, file.readlines())))

        assert n == len(tasks)
        return tasks, n


def with_score(method):
    def wrapped(self, *args, **kwargs):
        results = method(self, *args, **kwargs)
        return self.crit(results), list(results)

    wrapped.__name__ = method.__name__
    return wrapped


def pl(func):
    return lambda x: func(*x)


def arg_sort(array, **kwargs):
    key = kwargs['key']
    del kwargs['key']
    sorted_index = sorted([(v, i) for (i, v) in enumerate(array)], key=lambda x: key(x[0]), **kwargs)
    results = [i + 1 for v, i in sorted_index]
    return results


class Algorithm:

    def __init__(self, tasks, crit):
        self.tasks = tasks
        self.crit = crit

    SORT_BY_WEIGHT = pl(lambda _, task: task[3])
    SORT_BY_DURATION = pl(lambda _, task: -task[0])
    SORT_BY_WEIGHTED_DURATION = pl(lambda _, task: task[3] / task[0])

    @with_score
    def by_ready(self):
        return arg_sort(self.tasks, key=pl(lambda p, r, d, w: r))

    @with_score
    def by_due_date(self):
        return arg_sort(self.tasks, key=pl(lambda p, r, d, w: d))

    @with_score
    def ala_hodgson(self):
        # O(nlogn)
        base_permutation = arg_sort(self.tasks, key=pl(lambda p, r, d, w: d))

        # O(n)
        blocked = self.__get_blocks(base_permutation)

        # O(n^2logn)
        delayed = self.__try_delay(blocked, base_permutation, Algorithm.SORT_BY_WEIGHTED_DURATION)

        # O(n) lub O(nlogn)
        delayed = set(delayed)

        # O(n)
        results = self.__chain(
            [base_permutation[i] for i in range(len(base_permutation)) if i not in delayed],
            [base_permutation[i] for i in delayed]
        )

        return results

    @with_score
    def ala_hodgson_2(self):
        # O(nlogn)
        base_permutation = arg_sort(self.tasks, key=pl(lambda p, r, d, w: r))

        # O(n)
        blocked = self.__get_blocks(base_permutation)

        # O(n^2logn)
        delayed = self.__try_delay(blocked, base_permutation, Algorithm.SORT_BY_WEIGHTED_DURATION)

        # O(n) lub O(nlogn)
        delayed = set(delayed)

        # O(n)
        results = self.__chain(
            [base_permutation[i] for i in range(len(base_permutation)) if i not in delayed],
            [base_permutation[i] for i in delayed]
        )

        return results

    @with_score
    def ala_hodgson_3(self):
        # O(nlogn)
        base_permutation = arg_sort(self.tasks, key=pl(lambda p, r, d, w: r))

        # O(n)
        blocked = self.__get_blocks(base_permutation)

        # O(n^2logn)
        delayed = self.__try_delay(blocked, base_permutation, Algorithm.SORT_BY_DURATION)

        # O(n) lub O(nlogn)
        delayed = set(delayed)

        # O(n)
        results = self.__chain(
            [base_permutation[i] for i in range(len(base_permutation)) if i not in delayed],
            [base_permutation[i] for i in delayed]
        )

        return results

    @with_score
    def ala_hodgson_4(self):
        # O(nlogn)
        base_permutation = arg_sort(self.tasks, key=pl(lambda p, r, d, w: d))

        # O(n)
        blocked = self.__get_blocks(base_permutation)

        # O(n^2logn)
        delayed = self.__try_delay(blocked, base_permutation, Algorithm.SORT_BY_DURATION)

        # O(n) lub O(nlogn)
        delayed = set(delayed)

        # O(n)
        results = self.__chain(
            [base_permutation[i] for i in range(len(base_permutation)) if i not in delayed],
            [base_permutation[i] for i in delayed]
        )

        return results

    @with_score
    def prob_ala_hodgson(self):
        # O(nlogn)
        by_due_date = arg_sort(self.tasks, key=pl(lambda p, r, d, w: d))

        # O(n^2)
        blocking_table = self.__get_blocking_table(by_due_date)

        # O(n)
        blocked = self.__get_blocks(by_due_date)

        # O(n^2logn)
        delayed = self.__try_delay(blocked, by_due_date, pl(lambda j, _: blocking_table[j]))

        # O(n) lub O(nlogn)
        delayed = set(delayed)

        # O(n)
        results = self.__chain(
            [by_due_date[i] for i in range(len(by_due_date)) if i not in delayed],
            [by_due_date[i] for i in delayed]
        )

        return results

    @with_score
    def each_k_ala_hodgson(self, k=4):
        # O(nlogn)
        by_due_date = arg_sort(self.tasks, key=pl(lambda p, r, d, w: d))

        # O(n)
        blocked = self.__get_blocks(by_due_date)

        # O(n^2logn)
        delayed = self.__try_blocks_iterative(blocked, by_due_date, k)

        # O(n) lub O(nlogn)
        delayed = set(delayed)

        # O(n)
        results = self.__chain(
            [by_due_date[i] for i in range(len(by_due_date)) if i not in delayed],
            [by_due_date[i] for i in delayed]
        )

        return results

    def __get_blocking_table(self, permutation):
        return [
            sum([
                self.__get_blocking_prob(self.tasks[permutation[i] - 1], self.tasks[permutation[j] - 1])
                for j in range(i + 1, len(permutation)) if i != j])
            for i in range(len(permutation))
        ]

    def __get_blocking_prob(self, task1, task2):
        overlapping_time = max(min(task1[2], task2[2]) - max(task1[1], task2[1]), 0)
        duration_to_viable_time1 = (task1[0]) / (task1[2] - task1[1])
        duration_to_viable_time2 = (task2[0]) / (task2[2] - task2[1])
        average_overlap = overlapping_time * duration_to_viable_time1 * duration_to_viable_time2
        return average_overlap

    def __chain(self, *arrays):
        return list(itertools.chain(*arrays))

    def __try_delay(self, blocks, permutation, criteria):
        delayed = []
        # O(n)
        for row in blocks:
            crit_min = sum(map(pl(lambda _, task: task[3]), row[1:]))
            best_split = []
            # O(nlogn)
            row_by_criteria = list(map(pl(lambda j, _: j), sorted(row, key=criteria)))
            # ta i zewnętrzna pętla mają łącznie O(n) bo suma len(row) w delayed ma max n
            for i in range(1, len(row)):
                current_time = 0
                # O(n) lub O(nlogn)
                delayed_split = set(row_by_criteria[:i])
                # O(n)
                for j, (p, r, d, w) in row:
                    if j not in delayed_split:
                        next_time = max(r, current_time) + p
                        if next_time > d:
                            delayed_split.add(j)
                        current_time = next_time
                # O(n)
                crit = sum(map(lambda j: self.tasks[permutation[j] - 1][3], delayed_split))
                if crit < crit_min:
                    crit_min = crit
                    best_split = delayed_split
            delayed.extend(best_split)
        return delayed

    def __try_blocks_iterative(self, blocks, permutation, k):
        delayed = []
        # O(n)
        for row in blocks:
            crit_min = sum(map(pl(lambda _, task: task[3]), row[1:]))
            best_split = []
            # wprowadzamy stały mnożnik do złożoności
            for i in range(2, k):
                criteria = pl(lambda j, _: (j - row[0][0]) % k == k - 1)
                best_split, crit_min = self.__try_block_by_criteria(row, criteria, best_split, crit_min, permutation)
            for i in range(3, k):
                criteria = pl(lambda j, _: (j - row[0][0]) % k != k - 1)
                best_split, crit_min = self.__try_block_by_criteria(row, criteria, best_split, crit_min, permutation)
            delayed.extend(best_split)
        return delayed

    def __try_block_by_criteria(self, row, criteria, best_split, crit_min, permutation):
        # O(nlogn)
        row_by_criteria = list(map(pl(lambda j, _: j), sorted(row, key=criteria)))
        # ta i zewnętrzna pętla mają łącznie O(n) bo suma len(row) w delayed ma max n
        for i in range(1, len(row)):
            current_time = 0
            # O(n) lub O(nlogn)
            delayed_split = set(row_by_criteria[:i])
            # O(n)
            for j, (p, r, d, w) in row:
                if j not in delayed_split:
                    next_time = max(r, current_time) + p
                    if next_time > d:
                        delayed_split.add(j)
                    current_time = next_time
            # O(n)
            crit = sum(map(lambda j: self.tasks[permutation[j] - 1][3], delayed_split))
            if crit < crit_min:
                crit_min = crit
                best_split = delayed_split
        return best_split, crit_min

    def __sort_blocks(self, blocks, criteria):
        # O(n)
        for row in blocks:
            # O(nlogn)
            row.sort(key=criteria)

    def __get_blocks(self, permutation):
        blocked = []
        blocked_row = []
        current_time = 0

        # O(n)
        for i in range(len(permutation)):
            p, r, d, w = self.tasks[permutation[i] - 1]
            next_time = max(r, current_time) + p
            if next_time > d:
                if len(blocked_row) == 0:
                    blocked_row.append((i - 1, self.tasks[permutation[i - 1] - 1]))
                blocked_row.append((i, self.tasks[permutation[i] - 1]))
            elif len(blocked_row) > 0:
                blocked.append(blocked_row)
                blocked_row = []
            current_time = next_time

        if len(blocked_row) > 0:
            blocked.append(blocked_row)

        return blocked


if __name__ == '__main__':
    tasks, n = __parse_task()
    criteria = __score_func(tasks)

    # validator = Validator()
    # validator.evaluate_instance(sys.argv[1])

    algorithm = Algorithm(tasks, criteria)
    methods = [
        algorithm.ala_hodgson,
        algorithm.ala_hodgson_2,
        algorithm.ala_hodgson_3,
        algorithm.ala_hodgson_4
    ]
    results = sorted(list(map(lambda x: (x.__name__, x()), methods)), key=pl(lambda name, x: x[0]))

    print(f'{results[0][1][0]}')
    print(f'{" ".join(map(str, results[0][1][1]))}', end='')


    # import glob
    # import time
    # total_results = {}
    # acc = 0
    # k = 0
    # for file in glob.glob("1/instances/136780*250.in"):
    #     start = time.time()
    #     sys.argv[1] = file
    #     tasks, n = __parse_task(sys.argv[1])
    #     criteria = __score_func(tasks)
    #
    #     # validator = Validator()
    #     # validator.evaluate_instance(sys.argv[1])
    #
    #     algorithm = Algorithm(tasks, criteria)
    #     methods = [
    #         # algorithm.by_ready,
    #         # algorithm.by_due_date,
    #         algorithm.ala_hodgson,
    #         algorithm.ala_hodgson_2,
    #         algorithm.ala_hodgson_3,
    #         algorithm.ala_hodgson_4,
    #         # algorithm.each_k_ala_hodgson,
    #         # algorithm.prob_ala_hodgson
    #     ]
    #     results = sorted(list(map(lambda x: (x.__name__, x()), methods)), key=pl(lambda name, x: x[0]))
    #     for name, result in results:
    #         if name not in total_results:
    #             total_results[name] = 0
    #         total_results[name] += result[0] / __max_score(tasks)
    #
    #     # print(file)
    #     print(f'{results[0][1][0]}')
    #     print(f'{" ".join(map(str, results[0][1][1]))}')
    #
    #     c = criteria([i + 1 for i in range(len(tasks))])
    #     acc += (c - results[0][1][0]) / c * 100
    #     k += 1
    #     print(file, acc/k)
    # print(acc/k)
