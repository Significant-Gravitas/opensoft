import pytest


@pytest.fixture
def configurator_pytest(request):
    return request.param()
