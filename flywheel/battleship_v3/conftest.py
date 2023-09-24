import pytest

from flywheel.battleship_v3.abstract_class import Player


@pytest.fixture
def battleship_v3(request):
    return request.param()


@pytest.fixture
def player1():

    return Player(id=1, name="Player 1")


@pytest.fixture
def player2():

    return Player(id=2, name="Player 2")


@pytest.fixture
def game(player1, player2, battleship_v3):
    game_id = battleship_v3.create_game([player1.id, player2.id])
    return battleship_v3.get_game(game_id)


import pytest

from flywheel.battleship_v3.abstract_class import Direction, ShipPlacement, ShipType


@pytest.fixture
def place_all_ships(battleship_v3, player1, player2, game):
    ship_placements = [
        (ShipType.CARRIER, "A", 1),
        (ShipType.BATTLESHIP, "C", 1),
        (ShipType.CRUISER, "E", 1),
        (ShipType.SUBMARINE, "G", 1),
        (ShipType.DESTROYER, "I", 1),
    ]

    for ship_type, start_column, start_row in ship_placements:
        placement1 = ShipPlacement(
            game_id=game.id,
            ship_type=ship_type,
            start_row=start_row,
            start_column=start_column,
            direction=Direction.HORIZONTAL,
        )
        battleship_v3.create_ship_placement(game.id, player1.id, placement1)

        placement2 = ShipPlacement(
            game_id=game.id,
            ship_type=ship_type,
            start_row=start_row,
            start_column=start_column,
            direction=Direction.HORIZONTAL,
        )
        battleship_v3.create_ship_placement(game.id, player2.id, placement2)

    return True
