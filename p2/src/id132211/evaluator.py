from p2.src.data_api import Instance, Solution
from p2.src.evaluator_api import EvaluatorOutput, Evaluator
from p2.properties import EPS


class Evaluator132211(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        current_time = []
        current_score = []
        for i, machine in enumerate(output.schedule):
            current_time.append(0)
            current_score.append(0)
            for task_no in machine:
                task = in_data.tasks[task_no-1]
                current_time[i] = max(current_time[i], task.ready)
                current_time[i] += task.duration * in_data.machine_speeds[i]
                current_score[i] += current_time[i] - task.ready
        score = sum(current_score) / in_data.no_tasks
        return EvaluatorOutput(abs(output.score - score) / score < EPS or abs(output.score - score) < EPS, score, time)
