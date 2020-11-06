import argparse
import logging
import os
import re
import sys

from func_timeout import func_timeout, FunctionTimedOut

sys.path.append(".")

from p2.my_properties import INDEX
from p2.properties import INDICES
from p2.src.algorithm_api import Algorithm
from p2.src.evaluator_api import Evaluator
from p2.src.generator_api import Generator
from p2.src.data_api import Instance, Solution
from p2.src.utils import lmap

logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s', level=logging.INFO)
log = logging.getLogger()

GENERATE = 'generate'
VALIDATE = 'validate'
EVALUATE_MY = 'evaluate_my'
EVALUATE_ALL = 'evaluate_all'
TEST = 'test'

# TODO determine correct timeout
TIMEOUT = 1


class Runner:

    def __init__(self, mode: str):
        self.run = {
            GENERATE: self.generate_all_instances,
            VALIDATE: self.validate_all_instances,
            EVALUATE_MY: self.evaluate_my_algorithm,
            EVALUATE_ALL: self.evaluate_all_algorithms,
            TEST: self.test,
        }[mode]

    def get_instance_path(self, index, n):
        return os.path.join(os.path.dirname(__file__), "instances", f"{index}_{n}.in")

    def generate_all_instances(self):
        gen: Generator = self.__index_setup()[0][INDEX][0]()
        for n in range(50, 501, 50):
            instance: Instance = gen.generate(n, 5)
            instance.dump(self.get_instance_path(INDEX, n))

    def validate_all_instances(self):
        eval: Evaluator = self.__index_setup()[1][INDEX][0]()
        results = []
        for index in INDICES:
            for n in range(50, 501, 50):
                instance = Instance.load(self.get_instance_path(index, n))
                evaluator_output = eval.validate_schedule(instance, Solution.get_dummy_solution(n, 5))
                results.append(evaluator_output.value)
        log.info("\n".join([str(round(value, 2)) for value in results]))

    def evaluate_my_algorithm(self):
        _, evals, algs = self.__index_setup()
        eval: Evaluator = evals[INDEX][0]()
        alg: Algorithm = algs[INDEX][0]()
        relative_losses_sum = 0.0
        relative_losses_count = 0
        for index in INDICES:
            for n in range(50, 501, 50):
                instance = Instance.load(self.get_instance_path(index, n))
                seq_ouput = eval.validate_schedule(instance, Solution.get_dummy_solution(n, 5))
                alg_ouput = eval.validate_algorithm(instance, alg)
                relative_loss = (seq_ouput.value - alg_ouput.value) / seq_ouput.value
                if index == INDEX:
                    log.info("\t".join(map(lambda x: str(round(x, 2)),
                                        [n, seq_ouput.value, alg_ouput.value, 100 * relative_loss, alg_ouput.time])))
                relative_losses_sum += relative_loss
                relative_losses_count += 1

        log.info(f"\nMean relative improvement: {round(100 * relative_losses_sum / relative_losses_count, 2)}")

    def evaluate_all_algorithms(self):
        _, evals, algs = self.__index_setup()
        eval: Evaluator = evals[INDEX][0]()

        losses, times = [], []
        for n in range(50, 501, 50):
            instance = Instance.load(self.get_instance_path(INDEX, n))
            losses_row, times_row = [], []
            for index in INDICES:
                if index not in algs.keys():
                    loss, ti = "", ""
                else:
                    try:
                        alg_output = func_timeout(TIMEOUT, eval.validate_algorithm, args=(instance, algs[index][0]()))
                        if alg_output.correct:
                            loss, ti = str(round(alg_output.value, 2)), str(round(alg_output.time, 2))
                        else:
                            loss, ti = "", ""
                    except FunctionTimedOut:
                        loss, ti = "", ""
                losses_row.append(loss)
                times_row.append(ti)
            losses.append(losses_row)
            times.append(times_row)
        log.info("\n".join(["\t".join(row) for row in losses]), end="\n\n")
        log.info("\n".join(["\t".join(row) for row in times]), end="\n\n")

    # TODO - some actual testing
    def test(self):
        log.info('Discovering setup...')
        log.info(f'Found index: {INDEX}\n')
        gens, evals, algs = self.__index_setup()

        log.info('Detected components:')
        log.info(f'\t{gens}')
        log.info(f'\t{evals}')
        log.info(f'\t{algs}\n')

        log.info(f'You own:')
        log.info(f'{gens[INDEX]}')
        log.info(f'{evals[INDEX]}')
        log.info(f'{algs[INDEX]}')

    def __index_setup(self):
        tup = [[self.__index(cls) for cls in cat] for cat in
               map(lambda x: x.__subclasses__(), [Generator, Evaluator, Algorithm])]

        def array_to_dict_array(array):
            res = {}
            for id, cls in array:
                if id not in res:
                    res[id] = []
                res[id].append(cls)
            return res

        tup = lmap(array_to_dict_array, tup)
        return tup

    def __index(self, cls):
        id = next(re.finditer(r'\d+', cls.__name__)).group(0)
        return id, cls


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('mode',
                        choices=[GENERATE, VALIDATE, EVALUATE_MY, EVALUATE_ALL, TEST],
                        help="""
generate - generates your instances
validate - validates all instances
evaluate_my - evaluates your algorithm on your instances
evaluate_all - evaluates all algorithms on your instances
test - tests your setup
                        """)
    args = parser.parse_args()

    Runner(args.mode).run()
