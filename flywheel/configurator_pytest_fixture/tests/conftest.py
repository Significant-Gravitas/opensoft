import pytest


@pytest.fixture
def configurator_pytest_fixture(request):
    return request.param()
