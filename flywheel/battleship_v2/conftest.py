import pytest


@pytest.fixture
def battleship_v2(request):
    return request.param()
