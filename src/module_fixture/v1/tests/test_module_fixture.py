import pytest

from src.module_fixture.v1.b1.endpoint import ModuleFixture1


@pytest.fixture
def module_fixture():
    return ModuleFixture1()

@pytest.mark.mock
def test_sould_succeed_one(module_fixture):
    assert True


@pytest.mark.mock
def test_sould_succeed_two(module_fixture):
    assert True
