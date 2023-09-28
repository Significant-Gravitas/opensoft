from abc import ABC, abstractmethod
from typing import Tuple


class PytestFailureBase(ABC):
    pass
class PytestFailureRead(PytestFailureBase):
    pass

class PytestFailureCreate(PytestFailureBase):
    pass
