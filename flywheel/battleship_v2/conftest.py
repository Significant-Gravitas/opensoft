import pytest


@pytest.fixture
def battleship_v2(request):
    return request.param()


@pytest.fixture
def ship_on_G4():
    return {
        "ship_type": "battleship",
        "start_row": 4,
        "start_column": "G",
        "direction": "horizontal",
    }


@pytest.fixture
def player1(battleship_v2):
    return battleship_v2.create_player("Alice")


@pytest.fixture
def player2(battleship_v2):
    return battleship_v2.create_player("Bob")


@pytest.fixture
def created_game_id(battleship_v2, player1, player2):
    return battleship_v2.create_game([player1, player2])
