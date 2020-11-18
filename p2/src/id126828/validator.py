from p2.src.data_api import Instance, Solution
from p2.src.evaluator_api import EvaluatorOutput, Evaluator
import time as t


class Evaluator126828(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        # for every task check tasks
        global_solution = 0
        acc_time = t.time()
        for machine in range(in_data.no_machines):
            # set acctual timer to 0
            timer = 0
            partial_solution = 0
            # for every machine check tasks
            for task_id in output.schedule[machine]:
                acc_task = in_data.tasks[task_id]
                if timer < acc_task.ready:
                    timer = timer + acc_task.ready + acc_task.duration
                else:
                    timer = timer + acc_task.duration
                # add to partial solution next found value
                partial_solution = partial_solution + timer - acc_task.ready
            # at the end of loop counting partial solution, add it to global solution
            global_solution = global_solution + partial_solution
        is_correct = False
        if global_solution == output.score:
            is_correct = True
        end_time = t.time()
        time = end_time - acc_time
        return EvaluatorOutput(is_correct, global_solution, time)

