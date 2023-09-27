import pytest

from src.battleship.models import ShipPlacement, Turn


@pytest.fixture
def battleship(request):
    return request.param()


@pytest.fixture
def initialized_game_id(battleship):

    game_id = battleship.create_game()

    sample_ship_placements = [
        ShipPlacement(
            ship_type="carrier", start={"row": 1, "column": "A"}, direction="horizontal"
        ),
        ShipPlacement(
            ship_type="battleship",
            start={"row": 2, "column": "A"},
            direction="horizontal",
        ),
        ShipPlacement(
            ship_type="cruiser", start={"row": 3, "column": "A"}, direction="horizontal"
        ),
        ShipPlacement(
            ship_type="submarine",
            start={"row": 4, "column": "A"},
            direction="horizontal",
        ),
        ShipPlacement(
            ship_type="destroyer",
            start={"row": 5, "column": "A"},
            direction="horizontal",
        ),
    ]

    for ship_placement in sample_ship_placements:

        battleship.create_ship_placement(game_id, ship_placement)

    return game_id


@pytest.fixture
def game_over_fixture(battleship, initialized_game_id):

    for row in range(1, 11):
        for column in list("ABCDEFGHIJ"):

            turn = Turn(target={"row": row, "column": column})
            battleship.create_turn(initialized_game_id, turn)

            battleship.create_turn(initialized_game_id, turn)

    return initialized_game_id
