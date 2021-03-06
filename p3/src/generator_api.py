from abc import ABC, abstractmethod

from p3.src.data_api import Instance


class Generator(ABC):

    @abstractmethod
    def generate(self, no_tasks: int, no_machines: int) -> Instance:
        pass
