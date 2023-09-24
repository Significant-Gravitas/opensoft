import pytest


@pytest.mark.mock
def test_sould_succeed_one(module_fixture):
    assert True


@pytest.mark.mock
def test_sould_succeed_two(module_fixture):
    assert True
