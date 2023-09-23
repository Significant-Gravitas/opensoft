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


def test_ensuring_ships_do_not_overlap(battleship_v3, player1, game):
    # Given I already have a ship placed on specific grid squares
    placement1 = ShipPlacement(
        game_id=game.id,
        ship_type=ShipType.BATTLESHIP,
        start_row=3,
        start_column='B',
        direction=Direction.HORIZONTAL
    )
    battleship_v3.create_ship_placement(game.id, placement1)

    # When I try to place another ship on the same squares
    placement2 = ShipPlacement(
        game_id=game.id,
        ship_type=ShipType.CRUISER,
        start_row=3,
        start_column='B',
        direction=Direction.HORIZONTAL
    )

    try:
        battleship_v3.create_ship_placement(game.id, placement2)
        assert False, "Expected a ValueError due to overlapping ships."
    except ValueError:
        # Then I should be prevented from doing so
        pass
