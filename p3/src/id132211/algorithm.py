from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule

from p3.src.id132211.evaluator import Evaluator132211


class Algorithm132211(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        schedule = Schedule(in_data.no_tasks,
                            [i[0] for i in sorted(enumerate(in_data.tasks, start=1), key=lambda x: x[1].due_date)])
        return Solution(Evaluator132211().evaluate(in_data, Solution(0.0, schedule)).value, schedule)
