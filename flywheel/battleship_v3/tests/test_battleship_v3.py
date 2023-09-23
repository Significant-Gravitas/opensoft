def test_starting_a_new_game(battleship_v3, player1, player2):
    # Given the game is launched (by the presence of the `battleship_v2` fixture)

    # When I choose to start a new game
    game_id = battleship_v3.create_game([player1.id, player2.id])

    # Then the game should initiate against my opponent
    game = battleship_v3.get_game(game_id)
    assert game.player1_id == player1.id
    assert game.player2_id == player2.id
