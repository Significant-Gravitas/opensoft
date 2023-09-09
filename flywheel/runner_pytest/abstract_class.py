from abc import ABC, abstractmethod
from typing import Tuple, Optional

class AbstractRunnerPytest(ABC):

    @abstractmethod
    def get_pytest_failure(self, n: int, module: str) -> Tuple[str, str]:
        """
        Retrieve both the test code and result for the Nth failure in the specified module.
        """
        pass
