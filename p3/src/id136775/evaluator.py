from p3.properties import EPS
from p3.src.data_api import Instance, Solution, Schedule
from p3.src.evaluator_api import EvaluatorOutput, Evaluator


class Evaluator136775(Evaluator):

    def score(self, in_data: Instance, schedule: Schedule):
        score = 0

        w_sum = 0
        times = [0 for _ in range(in_data.no_machines)]
        for i, i_task in enumerate(schedule):
            i_task = i_task - 1
            task = in_data.tasks[i_task]
            durations = task.duration
            times[0] += durations[0]
            for i in range(1, in_data.no_machines):
                times[i] = max(times[i - 1] + durations[i], times[i] + durations[i])
            w_sum += task.weight
            score += task.weight * max(0, times[in_data.no_machines - 1] - task.due_date)

        return score / w_sum

    def evaluate(self, in_data: Instance, output: Solution, alg_time: float = None) -> EvaluatorOutput:
        correct = len(output.schedule) == in_data.no_tasks
        claimed_score = output.score

        score = self.score(in_data, output.schedule)

        correct &= score > claimed_score - EPS
        correct &= score < claimed_score + EPS
        return EvaluatorOutput(value=score, correct=correct, time=alg_time)
