import sys
from functools import reduce


class Job:
    def __init__(self, id, r, d, p, w):
        self.id = id
        self.r = r
        self.d = d
        self.p = p
        self.w = w


def find_late_jobs(jobs, clock):
    return list(reduce(lambda acc, curr: acc if curr.d >= clock + curr.p else [*acc, curr],
                       jobs,
                       []))


def bestWeightPerTime(readyJobs):
    return reduce(
        lambda acc, curr: acc if curr.w / curr.p <= acc['best'] else {'best': curr.w / curr.p, 'job': curr},
        readyJobs,
        {'best': 0, 'job': False}
    )['job']


def answerSolve(jobs):
    availableJobsByReadiness = jobs[:]
    lateJobs = list(filter(lambda x: x.w == 0, availableJobsByReadiness))
    availableJobsByReadiness = list(filter(lambda x: x.w != 0, availableJobsByReadiness))
    availableJobsByReadiness.sort(key=lambda x: x.r)
    readyJobs = []
    doneJobs = []
    clock = 0
    while len(availableJobsByReadiness) != 0 or len(readyJobs) != 0:
        late = find_late_jobs(readyJobs, clock)
        for i in range(len(late)):
            readyJobs = list(filter(lambda x: x.id != late[i].id, readyJobs))
            lateJobs.append(late[i])

        if len(readyJobs) > 0:
            job = bestWeightPerTime(readyJobs)
            readyJobs = list(filter(lambda x: x.id != job.id, readyJobs))
            doneJobs.append(job)
            clock += job.p
            while len(availableJobsByReadiness) > 0 and availableJobsByReadiness[0].r <= clock:
                readyJobs.append(availableJobsByReadiness.pop(0))
        elif len(availableJobsByReadiness) > 0:
            job = []
            while True:
                job = availableJobsByReadiness.pop(0)
                readyJobs.append(job)
                if len(availableJobsByReadiness) == 0 or job.r != availableJobsByReadiness[0].r:
                    break
            if job:
                clock = job.r
    answer = doneJobs + lateJobs
    answer = list(map(lambda x: x.id, answer))
    sum = calculate_weighted_sum(jobs, answer)
    return f'{sum}\n{" ".join(list(map(lambda x: f"{x}", answer)))}'


def calculate_weighted_sum(jobs, answer):
    clock = 0
    weighted_sum = 0
    for id in answer:
        if clock < jobs[id - 1].r:
            clock = jobs[id - 1].r + jobs[id - 1].p
        else:
            clock += jobs[id - 1].p
        if clock > jobs[id - 1].d:
            weighted_sum += jobs[id - 1].w
    return weighted_sum


def dummy_solution(n):
    ans = '0\n'
    for i in range(n):
        ans = f'{ans}{i + 1} '
    return ans


def parse_jobs(processes):
    jobs = []

    for i, job in enumerate(processes[1:], 1):
        prdw = job.split(' ')
        prdw = list(map(lambda x: int(x), prdw))
        jobs.append(Job(i, prdw[1], prdw[2], prdw[0], prdw[3]))
    return jobs


if __name__ == '__main__':
    processes = sys.stdin.read()
    processes = processes.strip()
    processes = processes.split('\n')
    n = int(processes[0])
    # solution = dummy_solution(n)
    jobs = parse_jobs(processes)
    solution = answerSolve(jobs)
    solution = solution.strip()
    sys.stdout.write(f'{solution}')
