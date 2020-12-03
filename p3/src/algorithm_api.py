from abc import abstractmethod, ABC

from p3.src.data_api import Instance, Solution


class Algorithm(ABC):

    @abstractmethod
    def run(self, in_data: Instance) -> Solution:
        pass
