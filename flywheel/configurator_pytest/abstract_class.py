from abc import ABC, abstractmethod
from typing import Tuple, Optional, Dict, List

class AbstractConfiguratorPytest(ABC):

    @abstractmethod
    def prepare_for_parameterization(self, metafunc, pytest_file_location) -> Tuple[str, List[type]]:
        """
        Prepares the necessary data for test parameterization and returns it.
        """
        pass
