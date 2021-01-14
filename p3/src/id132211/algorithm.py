from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule

from p3.src.id132211.evaluator import Evaluator132211


class Algorithm132211(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        jobs = [{'index': i,
                 'weight': job.weight,
                 'due_date': job.due_date,
                 'durations': (job.duration[0], job.duration[1], job.duration[2])}
                for i, job in enumerate(in_data.tasks, start=1)]

        avg_p = sum([sum(j['durations']) for j in jobs])/in_data.no_tasks/3
        timestamps = [0, 0, 0]
        schedule = []

        def modified_weight(job):
            t_0 = timestamps[0] + job['durations'][0]
            t_1 = max(t_0 + job['durations'][1], timestamps[1] + job['durations'][1])
            t_2 = max(t_1 + job['durations'][2], timestamps[2] + job['durations'][2])
            return max(0, avg_p + t_2 - job['due_date']) * (job['weight']/sum(job['durations']))
        while len(jobs) > 0:
            j = max(jobs, key=modified_weight)
            timestamps[0] += j['durations'][0]
            timestamps[1] = max(timestamps[1] + j['durations'][1], timestamps[0] + j['durations'][1])
            timestamps[1] = max(timestamps[2] + j['durations'][2], timestamps[1] + j['durations'][2])
            jobs = list(filter(lambda x: x['index'] != j['index'], jobs))
            schedule.append(j['index'])
            if len(jobs) > 0:
                avg_p = max([sum([j['durations'][x] for j in jobs]) for x in range(3)])/len(jobs)
        
        schedule = Schedule(in_data.no_tasks, schedule)
        sol = Solution(0.0, schedule)
        score = Evaluator132211().evaluate(in_data, sol).value
        sol = Solution(score, schedule)
        return sol
