from flywheel.battleship_v2.abstract_class import ShipPlacement, Turn


def test_turns_and_results(battleship_v2, initialized_game_id):
    # Now make a turn
    turn = Turn(target={"row": 1, "column": "A"})
    response = battleship_v2.create_turn(initialized_game_id, turn)

    assert response.result in ["hit", "miss"]
    if response.result == "hit":
        assert response.ship_type == "carrier"
    game = battleship_v2.get_game(initialized_game_id)
    assert turn in game.turns


def test_game_status_and_winner(battleship_v2):
    game_id = battleship_v2.create_game()
    status = battleship_v2.get_game_status(game_id)
    assert isinstance(status.is_game_over, bool)
    if status.is_game_over:
        winner = battleship_v2.get_winner(game_id)
        assert winner is not None


def test_delete_game(battleship_v2):
    game_id = battleship_v2.create_game()
    battleship_v2.delete_game(game_id)
    assert battleship_v2.get_game(game_id) is None


def test_ship_rotation(battleship_v2):
    game_id = battleship_v2.create_game()
    placement_horizontal = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "B"}, direction="horizontal"
    )
    battleship_v2.create_ship_placement(game_id, placement_horizontal)
    placement_vertical = ShipPlacement(
        ship_type="cruiser", start={"row": 3, "column": "D"}, direction="vertical"
    )
    battleship_v2.create_ship_placement(game_id, placement_vertical)
    game = battleship_v2.get_game(game_id)
    assert placement_horizontal in game.ships
    assert placement_vertical in game.ships


def test_game_state_updates(battleship_v2, initialized_game_id):
    # Attack a known position where a "submarine" is placed
    turn = Turn(target={"row": 3, "column": "A"})
    battleship_v2.create_turn(initialized_game_id, turn)

    # Retrieve the updated game state
    game = battleship_v2.get_game(initialized_game_id)

    # Assert that the target has been updated correctly
    target_key = (3, ord("A") - ord("A"))
    assert target_key in game.board and game.board[target_key] == "hit"


def test_ship_sinking_feedback(battleship_v2, initialized_game_id):
    # Battleship is already placed by the fixture at row 2 starting from column 'A'
    hits = ["A", "B", "C", "D"]
    static_moves = [
        {"row": 1, "column": "E"},
        {"row": 1, "column": "F"},
        {"row": 1, "column": "G"},
        {"row": 1, "column": "H"},
    ]

    for index, hit in enumerate(hits):
        # Player hits the battleship
        turn = Turn(target={"row": 2, "column": hit})
        response = battleship_v2.create_turn(initialized_game_id, turn)
        assert response.ship_type == "battleship"

        # Print out the response after each hit for debugging
        print(f"Hit {index + 1}: {response.result}")

        # Other player makes a static move
        static_turn = Turn(target=static_moves[index])
        battleship_v2.create_turn(initialized_game_id, static_turn)

    assert response.result == "sunk"


def test_restart_game(battleship_v2):
    game_id = battleship_v2.create_game()
    battleship_v2.delete_game(game_id)
    game_id = (
        battleship_v2.create_game()
    )  # Use the returned game_id after recreating the game
    game = battleship_v2.get_game(game_id)
    assert game is not None


def test_ship_edge_overlapping(battleship_v2):
    game_id = battleship_v2.create_game()

    # Place a battleship horizontally
    first_ship = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "A"}, direction="horizontal"
    )
    battleship_v2.create_ship_placement(game_id, first_ship)

    # Try placing a cruiser next to the battleship_v2, horizontally
    next_ship = ShipPlacement(
        ship_type="cruiser", start={"row": 1, "column": "E"}, direction="horizontal"
    )
    battleship_v2.create_ship_placement(game_id, next_ship)

    # Assert that both ships are placed without overlap
    game = battleship_v2.get_game(game_id)
    assert first_ship in game.ships
    assert next_ship in game.ships


def test_game_state_after_ship_placement(battleship_v2):
    game_id = battleship_v2.create_game()

    # Place a ship
    ship_placement = ShipPlacement(
        ship_type="battleship", start={"row": 1, "column": "A"}, direction="horizontal"
    )
    battleship_v2.create_ship_placement(game_id, ship_placement)

    # Check the game state after placement
    game = battleship_v2.get_game(game_id)
    assert ship_placement in game.ships


def test_game_state_after_turn(initialized_game_id, battleship_v2):
    turn = Turn(target={"row": 1, "column": "A"})
    response = battleship_v2.create_turn(initialized_game_id, turn)

    # Check the game state after the turn
    game = battleship_v2.get_game(initialized_game_id)

    # You'll need additional logic here to verify that the board has been updated correctly
    # Depending on your representation, an example assertion might look like this:
    if response.result == "hit":
        # This assumes a dictionary-based representation of the board
        assert game.board[(1, 0)] == "hit"
    else:
        assert game.board[1][0] == "miss"


def test_multiple_hits_on_ship(battleship_v2, initialized_game_id):
    hit_positions = ["A", "B", "C", "D", "E"]

    for index, pos in enumerate(hit_positions):
        # Player 1 makes an attempt to hit
        turn = Turn(target={"row": 1, "column": pos})
        response = battleship_v2.create_turn(initialized_game_id, turn)

        # Check if it's the last hit on the ship
        if index == len(hit_positions) - 1:
            assert response.result == "sunk"
        else:
            assert response.result == "hit"


def test_game_over_condition(battleship_v2, initialized_game_id):
    # Assuming 10x10 grid, target all possible positions
    for row in range(1, 11):
        for column in list("ABCDEFGHIJ"):
            # Player 1 takes a turn
            turn = Turn(target={"row": row, "column": column})
            battleship_v2.create_turn(initialized_game_id, turn)

            # Player 2 takes a turn, targeting the same position as Player 1
            battleship_v2.create_turn(initialized_game_id, turn)

    status = battleship_v2.get_game_status(initialized_game_id)
    assert status.is_game_over
