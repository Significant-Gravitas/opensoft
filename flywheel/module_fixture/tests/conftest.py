import pytest


@pytest.fixture
def module_fixture(request):
    return request.param()
