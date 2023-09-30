import pytest

from pages.python_injector.implementations.python_injector_1 import Pythoninjector1


@pytest.fixture
def injector():
    return Pythoninjector1()
