# import pytest
#
# from flywheel.battleship_v3.abstract_class import (
#     Direction,
#     GameStatusEnum,
#     ShipPlacement,
#     ShipType,
#     TurnResult,
# )
#
#
# def test_starting_a_new_game(battleship_v3, player1, player2):
#
#     game_id = battleship_v3.create_game([player1.id, player2.id])
#
#     game = battleship_v3.get_game(game_id)
#     assert game.player1_id == player1.id
#     assert game.player2_id == player2.id
#
#
# def test_ensuring_ships_do_not_overlap(battleship_v3, player1, game):
#
#     placement1 = ShipPlacement(
#         game_id=game.id,
#         ship_type=ShipType.BATTLESHIP,
#         start_row=3,
#         start_column="B",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v3.create_ship_placement(game.id, player1.id, placement1)
#
#     placement2 = ShipPlacement(
#         game_id=game.id,
#         ship_type=ShipType.CRUISER,
#         start_row=3,
#         start_column="B",
#         direction=Direction.HORIZONTAL,
#     )
#
#     try:
#         battleship_v3.create_ship_placement(game.id, player1.id, placement2)
#         assert False, "Expected a ValueError due to overlapping ships."
#     except ValueError:
#
#         pass
#
#
# from flywheel.battleship_v3.abstract_class import ShipType, Turn
#
#
# def test_guessing_a_grid_square(battleship_v3, player1, player2, game, place_all_ships):
#
#     turn = Turn(game_id=game.id, target_row=4, target_column="E")
#     result = battleship_v3.create_turn(game.id, turn)
#
#
# def test_getting_another_turn_after_a_successful_hit(
#     battleship_v3, player1, player2, game, place_all_ships
# ):
#
#     assert place_all_ships
#
#     ship_placement = ShipPlacement(
#         game_id=game.id,
#         ship_type=ShipType.SUBMARINE,
#         start_row=5,
#         start_column="F",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v3.create_ship_placement(game.id, player1.id, ship_placement)
#
#     turn1 = Turn(game_id=game.id, target_row=5, target_row_column="F")
#     result1 = battleship_v3.create_turn(game.id, turn1)
#
#     assert result1 == TurnResult.HIT
#
#
# from flywheel.battleship_v3.abstract_class import (
#     Direction,
#     ShipPlacement,
#     ShipType,
#     TurnResult,
# )
#
#
# def test_positioning_ships_on_the_grid(battleship_v3, player1, game):
#
#     placement = ShipPlacement(
#         game_id=game.id,
#         ship_type=ShipType.BATTLESHIP,
#         start_row=6,
#         start_column="F",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v3.create_ship_placement(game.id, player1.id, placement)
#
#     turn1 = Turn(game_id=game.id, target_row=6, target_column="F")
#     result1 = battleship_v3.create_turn(game.id, turn1)
#
#     turn2 = Turn(game_id=game.id, target_row=6, target_column="G")
#     result2 = battleship_v3.create_turn(game.id, turn2)
#
#     turn3 = Turn(game_id=game.id, target_row=6, target_column="H")
#     result3 = battleship_v3.create_turn(game.id, turn3)
#
#     turn4 = Turn(game_id=game.id, target_row=6, target_column="I")
#     result4 = battleship_v3.create_turn(game.id, turn4)
#
#     assert result1 == TurnResult.HIT
#     assert result2 == TurnResult.HIT
#     assert result3 == TurnResult.HIT
#     assert result4 == TurnResult.SUNK
#
#
# from flywheel.battleship_v3.abstract_class import (
#     Direction,
#     ShipPlacement,
#     ShipType,
#     TurnResult,
# )
#
#
# def test_informing_the_opponent_of_a_sunk_ship(battleship_v3, player1, player2, game):
#
#     ship_placement = ShipPlacement(
#         game_id=game.id,
#         player_id=player1.id,
#         ship_type=ShipType.DESTROYER,
#         start_row=3,
#         start_column="D",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v3.create_ship_placement(game.id, player1.id, ship_placement)
#
#     turn1 = Turn(game_id=game.id, target_row=3, target_column="D")
#     turn2 = Turn(game_id=game.id, target_row=3, target_column="E")
#
#     battleship_v3.create_turn(game.id, turn1)
#     battleship_v3.create_turn(game.id, turn2)
#
#     game_status = battleship_v3.get_game_status(game.id)
#
#     turns_with_sunk_result = [
#         turn
#         for turn in [turn1, turn2]
#         if battleship_v3.create_turn(game.id, turn) == TurnResult.SUNK
#     ]
#     assert (
#         turns_with_sunk_result
#     ), "The opponent should be informed that they have sunk a ship"
#
#     assert game_status.status != GameStatusEnum.ONGOING
#
#
# from flywheel.battleship_v3.abstract_class import (
#     Direction,
#     GameStatusEnum,
#     ShipPlacement,
#     ShipType,
#     TurnResult,
# )
#
#
# def test_ensuring_ships_do_not_overlap(battleship_v3, player1, game):
#
#     ship_placement = ShipPlacement(
#         game_id=game.id,
#         player_id=player1.id,
#         ship_type=ShipType.CRUISER,
#         start_row=4,
#         start_column="B",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v3.create_ship_placement(game.id, player1.id, ship_placement)
#
#     overlapping_ship_placement = ShipPlacement(
#         game_id=game.id,
#         player_id=player1.id,
#         ship_type=ShipType.SUBMARINE,
#         start_row=4,
#         start_column="B",
#         direction=Direction.HORIZONTAL,
#     )
#
#     with pytest.raises(ValueError, match="Ships overlap"):
#         battleship_v3.create_ship_placement(
#             game.id, player1.id, overlapping_ship_placement
#         )
#
#
# from flywheel.battleship_v3.abstract_class import GameStatusEnum
#
#
# def test_prevent_hitting_ships_before_placement(battleship_v3, player1, player2, game):
#     turn = Turn(game_id=game.id, target_row=3, target_column="D")
#
#     with pytest.raises(
#         ValueError, match="All ships must be placed before starting to hit"
#     ):
#         battleship_v3.create_turn(game.id, turn)
#
#     game_status = battleship_v3.get_game_status(game.id)
#     assert game_status.status == GameStatusEnum.ONGOING
