import argparse
import logging
import re

from p2.my_properties import INDEX
from p2.src.algorithm_api import Algorithm
from p2.src.evaluator_api import Evaluator
from p2.src.generator_api import Generator
from p2.src.utils import lmap

logging.basicConfig(format='[%(levelname)s] %(asctime)s - %(message)s', level=logging.INFO)
log = logging.getLogger()

GENERATE = 'generate'
VALIDATE = 'validate'
EVALUATE_MY = 'evaluate_my'
EVALUATE_ALL = 'evaluate_all'
TEST = 'test'


class Runner:

    def __init__(self, mode: str):
        self.run = {
            GENERATE: self.generate_all_instances,
            VALIDATE: self.validate_all_instances,
            EVALUATE_MY: self.evaluate_my_algorithm,
            EVALUATE_ALL: self.evaluate_all_algorithms,
            TEST: self.test,
        }[mode]

    # TODO
    def generate_all_instances(self):
        pass

    # TODO
    def validate_all_instances(self):
        pass

    # TODO
    def evaluate_my_algorithm(self):
        pass

    # use https://pypi.org/project/func-timeout/
    # TODO
    def evaluate_all_algorithms(self):
        pass

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
                        choices=['generate', 'validate', 'evaluate_my', 'evaluate_all', 'test'],
                        help="""
generate - generates your instances
validate - validates your instances
evaluate_my - evaluates your algorithm on your instances
evaluate_all - evaluates your algorithm
test - tests your setup
                        """)
    args = parser.parse_args()

    Runner(args.mode).run()
