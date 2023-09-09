from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, List

class AbstractConfiguratorPytest(ABC):

    @abstractmethod
    def setup_parameterization(self, metafunc) -> Tuple[str, List[type]]:
        """
        Prepares the necessary data for test parameterization and returns it.
        """
        pass
