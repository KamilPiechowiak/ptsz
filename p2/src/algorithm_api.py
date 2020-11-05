from abc import abstractmethod, ABC

from p2.src.data_api import Instance, Solution


class Algorithm(ABC):

    @abstractmethod
    def run(self, in_data: Instance) -> Solution:
        pass
