from flywheel.battleship_v2.abstract_class import (
    Direction,
    GameStatusEnum,
    Player,
    ShipPlacement,
    ShipType,
    Turn,
    TurnResult,
)


def test_start_new_game(battleship_v2):
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    assert game_id is not None
    game = battleship_v2.get_game(game_id)
    assert game.player1_id == player1.id
    assert game.player2_id == player2.id


def test_ship_positioning(battleship_v2):
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    placement = ShipPlacement(
        game_id=game_id,
        ship_type=ShipType.CARRIER,
        start_row=1,
        start_column="A",
        direction=Direction.HORIZONTAL,
    )
    battleship_v2.create_ship_placement(game_id, placement)


def test_ship_rotation(battleship_v2):
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    placement = ShipPlacement(
        game_id=game_id,
        ship_type=ShipType.CARRIER,
        start_row=1,
        start_column="A",
        direction=Direction.VERTICAL,
    )
    battleship_v2.create_ship_placement(game_id, placement)


def test_hit_ship(battleship_v2):

    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    turn = Turn(game_id=game_id, target_row=1, target_column="A")
    response = battleship_v2.create_turn(game_id, turn)

    assert response.result == TurnResult.HIT


def test_miss_ship(battleship_v2):

    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    turn = Turn(game_id=game_id, target_row=4, target_column="D")
    response = battleship_v2.create_turn(game_id, turn)

    assert response.result == TurnResult.MISS


def test_game_over(battleship_v2):

    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    status = battleship_v2.get_game_status(game_id)
    assert status.is_game_over is True
    assert status.winner_id is not None


def test_full_game_play(battleship_v2):

    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    for ship, length in battleship_v2.SHIP_LENGTHS.items():
        placement1 = ShipPlacement(
            game_id=game_id,
            ship_type=ship,
            start_row=1,
            start_column=chr(65 + length),
            direction=Direction.VERTICAL,
        )
        battleship_v2.create_ship_placement(game_id, placement1)
        placement2 = ShipPlacement(
            game_id=game_id,
            ship_type=ship,
            start_row=1,
            start_column=chr(75 - length),
            direction=Direction.VERTICAL,
        )
        battleship_v2.create_ship_placement(game_id, placement2)

    for ship, length in battleship_v2.SHIP_LENGTHS.items():
        for i in range(length):
            turn = Turn(
                game_id=game_id, target_row=i + 1, target_column=chr(75 - length)
            )
            response = battleship_v2.create_turn(game_id, turn)
            assert response.result == TurnResult.HIT
            if i == length - 1:
                assert response.ship_type == ship

    for i in range(10):
        turn = Turn(game_id=game_id, target_row=i + 1, target_column="J")
        response = battleship_v2.create_turn(game_id, turn)
        assert response.result == TurnResult.MISS

    status = battleship_v2.get_game_status(game_id)
    assert status.is_game_over is True
    assert status.winner_id == player1.id

    status = battleship_v2.get_game_status(game_id)
    assert status.is_game_over is True
    assert status.status == GameStatusEnum.DRAW
