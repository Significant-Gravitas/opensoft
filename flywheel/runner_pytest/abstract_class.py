from abc import ABC, abstractmethod
from typing import Tuple


class AbstractRunnerPytest(ABC):
    @abstractmethod
    def get_pytest_failure(self, n: int, module: str) -> Tuple[str, str]:

        pass
