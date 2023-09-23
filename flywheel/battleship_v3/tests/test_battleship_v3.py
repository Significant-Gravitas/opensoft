from flywheel.battleship_v3.abstract_class import ShipPlacement, ShipType, Direction


def test_starting_a_new_game(battleship_v3, player1, player2):
    # Given the game is launched (by the presence of the `battleship_v2` fixture)

    # When I choose to start a new game
    game_id = battleship_v3.create_game([player1.id, player2.id])

    # Then the game should initiate against my opponent
    game = battleship_v3.get_game(game_id)
    assert game.player1_id == player1.id
    assert game.player2_id == player2.id

def test_positioning_ships_on_the_grid(battleship_v3, player1, game):
    # Given it's my turn to position ships
    # This is ensured by creating a new game for the player1

    # When I place a ship on the 10x10 grid
    placement = ShipPlacement(
        game_id=game.id,
        ship_type=ShipType.BATTLESHIP,
        start_row=3,
        start_column='B',
        direction=Direction.HORIZONTAL
    )
    battleship_v3.create_ship_placement(game.id, placement)

    # Then the ship should occupy its specified grid squares
    saved_placement = battleship_v3.get_ship_placement(game.id, ShipType.BATTLESHIP)
    assert saved_placement.start_row == 3
    assert saved_placement.start_column == 'B'
    assert saved_placement.direction == Direction.HORIZONTAL

from flywheel.battleship_v3.abstract_class import ShipPlacement, ShipType, Direction

def test_rotating_ships_during_placement(battleship_v3, player1, game):
    # Given I am positioning a ship
    placement = ShipPlacement(
        game_id=game.id,
        ship_type=ShipType.BATTLESHIP,
        start_row=3,
        start_column='B',
        direction=Direction.HORIZONTAL
    )
    battleship_v3.create_ship_placement(game.id, placement)

    # When I choose to rotate it
    updated_placement = ShipPlacement(
        game_id=game.id,
        ship_type=ShipType.BATTLESHIP,
        start_row=3,
        start_column='B',
        direction=Direction.VERTICAL
    )
    battleship_v3.create_ship_placement(game.id, updated_placement)

    # Then the ship should change its orientation
    saved_placement = battleship_v3.get_ship_placement(game.id, ShipType.BATTLESHIP)
    assert saved_placement.direction == Direction.VERTICAL
