from p3.src.data_api import Instance, Solution, Schedule
from p3.src.evaluator_api import EvaluatorOutput, Evaluator
from p3.properties import EPS


def getScore(in_data: Instance, schedule: Schedule):
    currMoments = [0, 0, 0]
    score = 0
    denom = 0
    for currTaskIdx in schedule:
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
    return score / denom


class Evaluator136810(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        score = getScore(in_data, output.schedule)

        correct = abs(score - output.score) <= EPS
        value = score
        return EvaluatorOutput(correct, value, time)
