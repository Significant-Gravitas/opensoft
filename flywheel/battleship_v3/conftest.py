import pytest

from flywheel.battleship_v3.abstract_class import Player


@pytest.fixture
def battleship_v3(request):
    return request.param()

@pytest.fixture
def player1():
    # Here's a basic fixture for the 'player1' object. Modify it according to your needs.
    return Player(id=1, name="Player 1")

@pytest.fixture
def player2():
    # Similarly, a basic fixture for the 'player2' object.
    return Player(id=2, name="Player 2")
