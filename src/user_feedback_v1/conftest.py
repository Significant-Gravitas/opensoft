import pytest


@pytest.fixture
def user_feedback_v1(request):
    return request.param()
