import pytest


@pytest.fixture
def runner_pytest(request):
    return request.param()
