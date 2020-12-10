from p3.properties import EPS
from p3.src.data_api import Instance, Solution
from p3.src.evaluator_api import Evaluator, EvaluatorOutput


class Evaluator126828(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = 0) -> EvaluatorOutput:

        start_times_1st_machine = [0] * in_data.no_tasks
        timer = 0
        # generowanie czasów dla pierwszej maszyny. Nieograniczone przez poprzednią, można zadania dawać jedno po drugim
        for task_id in output.schedule:
            timer += in_data.tasks[task_id - 1].duration[0]
            start_times_1st_machine[task_id - 1] = timer
        if in_data.no_tasks == 50:
            print('first machine: ', start_times_1st_machine)
        # druga maszyna, czasy na generowane na podstawie swoich czasów przetwarzania oraz początku wykonywania zadania
        # ograniczonego przez koniec tego zadania z maszyny 1-wszej
        local_timer = 0
        for task_id in output.schedule:
            # timer = max z lokalnego czasu i czasu zakończenia zadania na 1wszej maszynie
            local_timer = max(local_timer, start_times_1st_machine[task_id - 1])
            # dodaj do czasu czas przetwarzania i zwiększ lokalny timer
            start_times_1st_machine[task_id - 1] = local_timer + in_data.tasks[task_id - 1].duration[1]
            local_timer += in_data.tasks[task_id - 1].duration[1]
        if in_data.no_tasks == 50:
            print('second machine: ', start_times_1st_machine)
        # trzecia maszyna analogicznie do drugiej, ale tutaj liczymy score
        local_timer = 0
        scores = []
        for task_id in output.schedule:
            # timer = max z lokalnego czasu i czasu zakończenia zadania na 1wszej maszynie
            local_timer = max(local_timer, start_times_1st_machine[task_id - 1])
            # dodaj do czasu czas przetwarzania i zwiększ lokalny timer
            start_times_1st_machine[task_id - 1] = local_timer + in_data.tasks[task_id - 1].duration[2]
            # jeżeli przekroczono due_time, oblicz wynik
            local_timer += in_data.tasks[task_id - 1].duration[1]
            scores.append(in_data.tasks[task_id - 1].weight * max(0, local_timer - in_data.tasks[task_id - 1].due_date))
        if in_data.no_tasks == 50:
            print('third machine: ', start_times_1st_machine)
        result = sum(scores) / sum(task.weight for task in in_data.tasks)

        correct = False
        if abs(output.score - result) / result < EPS or abs(output.score - result) < EPS:
            correct = True

        return EvaluatorOutput(correct, result, time)
