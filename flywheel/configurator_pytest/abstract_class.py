from abc import ABC, abstractmethod
from typing import List, Tuple


class AbstractConfiguratorPytest(ABC):
    @abstractmethod
    def setup_parameterization(self, metafunc) -> Tuple[str, List[type]]:

        pass
