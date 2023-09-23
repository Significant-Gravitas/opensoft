import pytest


@pytest.fixture
def battleship_v3(request):
    return request.param()
