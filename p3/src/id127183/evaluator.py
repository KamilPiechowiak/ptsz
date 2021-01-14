from p3.src.data_api import Instance, Solution
from p3.src.evaluator_api import EvaluatorOutput, Evaluator
from p3.properties import EPS


class Evaluator127183(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        currMoments = [0, 0, 0]
        score, denom = 0, 0
        for currTaskIdx in output.schedule:
            currentTask = in_data.tasks[currTaskIdx - 1]
            for index, machineMoment in enumerate(currMoments):
                if index == 0:
                    currMoments[index] += currentTask.duration[index]
                else:
                    possiblePartTaskStart = max(currMoments[index-1], currMoments[index])
                    currMoments[index] = possiblePartTaskStart + currentTask.duration[index]
            endMoment = max(currMoments)
            lateness = max(0, endMoment - currentTask.due_date)
            score += lateness * currentTask.weight
            denom += currentTask.weight
        score /= denom
        correct = abs(score - output.score) <= EPS
        value = score
        return EvaluatorOutput(correct, value, time)
