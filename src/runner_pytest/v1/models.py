from abc import ABC, abstractmethod
from typing import Tuple


class PytestFailureBase(ABC):
    pass
class PytestFailureRead(PytestFailureBase):
    pass

class PytestFailureCreate(PytestFailureBase):
    pass


class AbstractRunnerPytest(ABC):
    @abstractmethod
    def get_pytest_failure(self, n: int, module: str) -> Tuple[str, str]:

        pass
