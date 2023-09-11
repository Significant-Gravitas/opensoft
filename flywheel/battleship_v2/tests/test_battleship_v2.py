from flywheel.battleship_v2.abstract_class import ShipPlacement, Turn, GameStatusEnum, TurnResult, Player, ShipType, \
    Direction

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

    placement = ShipPlacement(game_id=game_id, ship_type=ShipType.CARRIER, start_row=1, start_column='A', direction=Direction.HORIZONTAL)
    battleship_v2.create_ship_placement(game_id, placement)

    # You can add more validations here

def test_ship_rotation(battleship_v2):
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    placement = ShipPlacement(game_id=game_id, ship_type=ShipType.CARRIER, start_row=1, start_column='A', direction=Direction.VERTICAL)
    battleship_v2.create_ship_placement(game_id, placement)

    # You can add more validations here

# 2. Tests related to Gameplay

def test_hit_ship(battleship_v2):
    # Assume ships are placed
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    turn = Turn(game_id=game_id, target_row=1, target_column='A')
    response = battleship_v2.create_turn(game_id, turn)

    assert response.result == TurnResult.HIT

def test_miss_ship(battleship_v2):
    # Assume ships are placed but not on D4
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    turn = Turn(game_id=game_id, target_row=4, target_column='D')
    response = battleship_v2.create_turn(game_id, turn)

    assert response.result == TurnResult.MISS

# 3. Tests related to Endgame

def test_game_over(battleship_v2):
    # Assume ships are placed and all but one grid is left
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    status = battleship_v2.get_game_status(game_id)
    assert status.is_game_over is True
    assert status.winner_id is not None

# 5. Full Game Play Scenario

def test_full_game_play(battleship_v2):
    # Setup
    player1 = Player(name="Alice")
    player2 = Player(name="Bob")

    game_id = battleship_v2.create_game([player1.id, player2.id])

    # Players place their ships
    for ship, length in battleship_v2.SHIP_LENGTHS.items():
        placement1 = ShipPlacement(game_id=game_id, ship_type=ship, start_row=1, start_column=chr(65 + length), direction=Direction.VERTICAL)
        battleship_v2.create_ship_placement(game_id, placement1)
        placement2 = ShipPlacement(game_id=game_id, ship_type=ship, start_row=1, start_column=chr(75 - length), direction=Direction.VERTICAL)
        battleship_v2.create_ship_placement(game_id, placement2)

    # Player 1 tries to hit Player 2's ships
    for ship, length in battleship_v2.SHIP_LENGTHS.items():
        for i in range(length):
            turn = Turn(game_id=game_id, target_row=i+1, target_column=chr(75 - length))
            response = battleship_v2.create_turn(game_id, turn)
            assert response.result == TurnResult.HIT
            if i == length - 1:
                assert response.ship_type == ship

    # Player 2 tries to miss Player 1's ships deliberately
    for i in range(10):
        turn = Turn(game_id=game_id, target_row=i+1, target_column='J')
        response = battleship_v2.create_turn(game_id, turn)
        assert response.result == TurnResult.MISS

    # Assert that the game has ended and Player 1 has won
    status = battleship_v2.get_game_status(game_id)
    assert status.is_game_over is True
    assert status.winner_id == player1.id


    # Assert that the game has ended and it's a draw
    status = battleship_v2.get_game_status(game_id)
    assert status.is_game_over is True
    assert status.status == GameStatusEnum.DRAW

