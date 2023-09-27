# import pytest
#
# from src.battleship_v2.models import (
#     Direction,
#     GameStatusEnum,
#     ShipPlacement,
#     ShipType,
#     Turn,
#     TurnResult,
# )
#
#
# def generate_id():
#     id_ = 1
#     while True:
#         yield id_
#         id_ += 1
#
#
# id_generator = generate_id()
#
#
# def new_id():
#     return next(id_generator)
#
#
# def test_start_new_game(battleship_v2, created_game_id, player1, player2):
#     game = battleship_v2.get_game(created_game_id)
#     assert game.player1_id == player1
#     assert game.player2_id == player2
#
#
# def test_ship_positioning(battleship_v2, created_game_id):
#     placement = ShipPlacement(
#         game_id=created_game_id,
#         ship_type=ShipType.CARRIER,
#         start_row=1,
#         start_column="A",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v2.create_ship_placement(created_game_id, placement)
#
#
# def test_ship_rotation(battleship_v2, created_game_id):
#     placement = ShipPlacement(
#         game_id=created_game_id,
#         ship_type=ShipType.CARRIER,
#         start_row=1,
#         start_column="A",
#         direction=Direction.VERTICAL,
#     )
#     battleship_v2.create_ship_placement(created_game_id, placement)
#
#
# def test_hit_ship(battleship_v2, created_game_id):
#     ship_placement = ShipPlacement(
#         game_id=created_game_id,
#         ship_type=ShipType.SUBMARINE,
#         start_row=1,
#         start_column="A",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v2.create_ship_placement(created_game_id, ship_placement)
#
#     turn = Turn(game_id=created_game_id, target_row=1, target_column="A")
#     response = battleship_v2.create_turn(created_game_id, turn)
#
#     assert response.result == TurnResult.HIT
#
#
# def test_miss_ship(battleship_v2, created_game_id):
#     turn = Turn(game_id=created_game_id, target_row=4, target_column="D")
#     response = battleship_v2.create_turn(created_game_id, turn)
#
#     assert response.result == TurnResult.MISS
#
#
# def test_create_game(battleship_v2):
#     player1_id = battleship_v2.create_player("Alice")
#     player2_id = battleship_v2.create_player("Bob")
#
#     game_id = battleship_v2.create_game([player1_id, player2_id])
#     assert game_id is not None
#
#
# def test_ship_placement(battleship_v2):
#     player1_id = battleship_v2.create_player("Alice")
#     player2_id = battleship_v2.create_player("Bob")
#
#     game_id = battleship_v2.create_game([player1_id, player2_id])
#
#     placement = ShipPlacement(
#         game_id=game_id,
#         ship_type="carrier",
#         start_row=1,
#         start_column="A",
#         direction="horizontal",
#     )
#     battleship_v2.create_ship_placement(game_id, placement)
#
#
# def test_make_turn_and_miss(battleship_v2):
#     player1_id = battleship_v2.create_player("Alice")
#     player2_id = battleship_v2.create_player("Bob")
#
#     game_id = battleship_v2.create_game([player1_id, player2_id])
#
#     turn = Turn(game_id=game_id, target_row=5, target_column="F")
#
#     result = battleship_v2.create_turn(game_id, turn)
#     assert result.result == TurnResult.MISS
#
#
# def test_make_turn_and_hit(battleship_v2):
#
#     player1_id = battleship_v2.create_player("player1")
#     player2_id = battleship_v2.create_player("player2")
#     game_id = battleship_v2.create_game([player1_id, player2_id])
#
#     ship_on_G4 = ShipPlacement(
#         game_id=game_id,
#         ship_type=ShipType.BATTLESHIP,
#         start_row=4,
#         start_column="G",
#         direction=Direction.HORIZONTAL,
#     )
#     battleship_v2.create_ship_placement(game_id, ship_on_G4)
#
#     turn = Turn(game_id=game_id, target_row=4, target_column="G")
#     result = battleship_v2.create_turn(game_id, turn)
#
#     assert result.result == TurnResult.HIT
#
#
# def test_sunk_ship(battleship_v2, created_game_id, ship_on_G4):
#
#     player1_id = battleship_v2.create_player("Player1")
#     player2_id = battleship_v2.create_player("Player2")
#     created_game_id = battleship_v2.create_game([player1_id, player2_id])
#     assert isinstance(created_game_id, int)
#
#
# def test_create_player(battleship_v2):
#     player_name = "John Doe"
#     player_id = battleship_v2.create_player(player_name)
#     assert isinstance(player_id, int)
#     player = battleship_v2.get_player(player_id)
#     assert player.name == player_name
#
#
# def test_turn_miss(battleship_v2, created_game_id):
#     turn_result = battleship_v2.create_turn(
#         created_game_id, Turn(target_row=1, target_column="A")
#     )
#     assert turn_result.result == TurnResult.MISS
#
#
# def test_game_status_ongoing(battleship_v2, game_id):
#     status = battleship_v2.get_game_status(game_id)
#     assert status.is_game_over == False
#     assert status.status == GameStatusEnum.ONGOING
#
#
# def test_game_status_win(battleship_v2, game_id, ship_on_G4):
#     battleship_v2.create_ship_placement(game_id, ShipPlacement(**ship_on_G4))
#     for i, col in enumerate(["G", "H", "I", "J"], start=4):
#         battleship_v2.create_turn(game_id, Turn(target_row=i, target_column=col))
#     status = battleship_v2.get_game_status(game_id)
#     assert status.is_game_over == True
#     assert (
#         status.status == GameStatusEnum.PLAYER1_WIN
#         or status.status == GameStatusEnum.PLAYER2_WIN
#     )
#
#
# def test_delete_game(battleship_v2, game_id):
#     battleship_v2.delete_game(game_id)
#     with pytest.raises(Exception):
#         game = battleship_v2.get_game(game_id)
