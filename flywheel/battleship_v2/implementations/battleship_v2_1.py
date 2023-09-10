from typing import Dict

from flywheel.battleship_v2.abstract_class import AbstractBattleshipV2, Game, ShipPlacement, Turn, TurnResponse, \
    GameStatus


class BattleshipV21(AbstractBattleshipV2):
    def __init__(self):
        self.games: Dict[int, Game] = {}

    def create_game(self) -> int:
        game_id = str(len(self.games))
        new_game = Game(
            game_id=game_id,  # set game_id as the index in the list
            players=[],  # Empty list to start with
            board={},  # Empty board to start with
            ships=[],  # No ships placed yet
            turns=[],  # No turns taken yet
        )

        self.games[game_id] = new_game
        return new_game.game_id

    def create_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:
        print(
            f"Attempting to place ship for game ID {game_id} with placement: {placement}"
        )

        game = self.games.get(game_id)

        if not game:
            print(f"Game with ID {game_id} not found.")
            raise ValueError(f"Game with ID {game_id} not found.")
        if placement.direction not in ["horizontal", "vertical"]:
            print(f"Invalid ship direction {placement.direction}")
            raise ValueError("Invalid ship direction")
        # Check if all ships are already placed
        if self.all_ships_placed(game):
            print("All ships are already placed. Cannot place more ships.")
            raise ValueError("All ships are already placed. Cannot place more ships.")

        ship_length = self.SHIP_LENGTHS.get(placement.ship_type)
        if not ship_length:
            print(f"Invalid ship type {placement.ship_type}")
            raise ValueError(f"Invalid ship type {placement.ship_type}")

        start_row, start_col = placement.start["row"], ord(
            placement.start["column"]
        ) - ord("A")

        # Check for out-of-bounds placements
        if start_row < 1 or start_row > 10 or start_col < 0 or start_col > 9:
            print("Placement out of bounds")
            raise ValueError("Placement out of bounds")

        # Check if ship extends beyond boundaries
        if placement.direction == "horizontal" and start_col + ship_length > 10:
            print("Ship extends beyond board boundaries")
            raise ValueError("Ship extends beyond board boundaries")
        elif placement.direction == "vertical" and start_row + ship_length > 10:
            print("Ship extends beyond board boundaries")
            raise ValueError("Ship extends beyond board boundaries")

        # Check for overlap
        for i in range(ship_length):
            if placement.direction == "horizontal":
                if game.board.get((start_row, start_col + i)):
                    print("Ship overlaps with another ship!")
                    raise ValueError("Ship overlaps with another ship!")
            elif placement.direction == "vertical":
                if game.board.get((start_row + i, start_col)):
                    print("Ship overlaps with another ship!")
                    raise ValueError("Ship overlaps with another ship!")

        # Now place the ship on the board after overlap check
        for i in range(ship_length):
            if placement.direction == "horizontal":
                game.board[(start_row, start_col + i)] = placement.ship_type
            else:
                game.board[(start_row + i, start_col)] = placement.ship_type

        # Add the ship placement to the game's ships list
        game.ships.append(placement)
        print(
            f"Successfully placed {placement.ship_type} at starting coordinates {start_row, start_col} in direction {placement.direction}"
        )

    def create_turn(self, game_id: str, turn: Turn) -> TurnResponse:
        game = self.games.get(game_id)

        if not game:
            raise ValueError(f"Game with ID {game_id} not found.")

        if not self.all_ships_placed(game):
            raise ValueError("All ships must be placed before starting turns")

        target_row, target_col = turn.target["row"], ord(turn.target["column"]) - ord(
            "A"
        )
        hit_ship = game.board.get((target_row, target_col))

        game.turns.append(turn)

        print(
            f"Targeted position: ({target_row}, {target_col})"
        )  # Print the targeted position

        # Check if the position has already been hit
        if hit_ship == "hit":
            print("Position already hit!")
            return TurnResponse(
                result="miss", ship_type=None
            )  # or whatever is appropriate for a repeated hit

        print(f"Hit ship: {hit_ship}")  # Print the ship that got hit

        if hit_ship:
            ship_placement = next(sp for sp in game.ships if sp.ship_type == hit_ship)

        if hit_ship:
            ship_placement = next(sp for sp in game.ships if sp.ship_type == hit_ship)
            start_row, start_col = ship_placement.start["row"], ord(
                ship_placement.start["column"]
            ) - ord("A")
            ship_positions = [
                (
                    start_row + (i if ship_placement.direction == "vertical" else 0),
                    start_col + (i if ship_placement.direction == "horizontal" else 0),
                )
                for i in range(self.SHIP_LENGTHS[hit_ship])
            ]

            # Update targeted_positions before modifying the game.board
            targeted_positions = {
                (t.target["row"], ord(t.target["column"]) - ord("A"))
                for t in game.turns
            }

            print(f"Expected ship positions: {set(ship_positions)}")
            print(f"Actual targeted positions: {targeted_positions}")

            game.board[(target_row, target_col)] = "hit"

            # Determine if ship is sunk by checking if all of its positions have been targeted
            if set(ship_positions).issubset(targeted_positions):
                for pos in ship_positions:
                    game.board[pos] = "hit"
                return TurnResponse(result="sunk", ship_type=hit_ship)
            else:
                return TurnResponse(result="hit", ship_type=hit_ship)

    def get_game_status(self, game_id: str) -> GameStatus:
        game = self.games.get(game_id)

        if not game:
            raise ValueError(f"Game with ID {game_id} not found.")

        # We'll count the number of 'hit' entries in the board to determine how many positions were hit.
        hits = sum(1 for _, status in game.board.items() if status == "hit")

        # Total ships length should be the sum of lengths of all the ships placed, not the length of their names
        total_ships_length = sum(
            self.SHIP_LENGTHS[ship.ship_type] for ship in game.ships
        )

        if hits == total_ships_length:
            return GameStatus(
                is_game_over=True, winner="player"
            )  # Assuming single player for simplicity
        else:
            return GameStatus(is_game_over=False, winner=None)

    def get_winner(self, game_id: str) -> str:
        game_status = self.get_game_status(game_id)

        if game_status.is_game_over:
            return game_status.winner
        else:
            return None

    def get_game(self, game_id: str) -> Game:
        return self.games.get(game_id)

    def delete_game(self, game_id: str) -> None:
        if game_id in self.games:
            del self.games[game_id]

    def all_ships_placed(self, game: Game) -> bool:
        placed_ship_types = set([placement.ship_type for placement in game.ships])
        return placed_ship_types == set(self.SHIP_LENGTHS.keys())
