import pytest

from src.module_fixture.implementations.module_fixture_1 import ModuleFixture1


@pytest.fixture
def module_fixture():
    return ModuleFixture1()

@pytest.mark.mock
def test_sould_succeed_one(module_fixture):
    assert True


@pytest.mark.mock
def test_sould_succeed_two(module_fixture):
    assert True
