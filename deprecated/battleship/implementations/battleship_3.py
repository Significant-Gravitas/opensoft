import uuid

from src.battleship.models import (
    AbstractBattleship,
    Game,
    GameStatus,
    ShipPlacement,
    Turn,
    TurnResponse,
)


class Battleship3(AbstractBattleship):

    games = {}

    def create_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:

        if game_id not in self.games:
            raise ValueError("Game not found!")

        if placement.ship_type not in self.SHIP_LENGTHS:
            raise ValueError("Invalid ship type")

        if placement.direction not in ["horizontal", "vertical"]:
            raise ValueError("Invalid ship direction")

        if len(self.games[game_id].ships) >= len(self.SHIP_LENGTHS):
            raise ValueError("All ships are already placed. Cannot place more ships.")

        self._validate_ship_placement(game_id, placement)

        row, col = placement.start["row"], ord(placement.start["column"]) - ord("A")
        direction = placement.direction
        ship_length = self.SHIP_LENGTHS[placement.ship_type]

        for i in range(ship_length):
            if direction == "horizontal":
                self.games[game_id].board[(row, col + i)] = placement.ship_type
            else:
                self.games[game_id].board[(row + i, col)] = placement.ship_type

        self.games[game_id].ships.append(placement)

    def _validate_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:

        row, col = placement.start["row"], ord(placement.start["column"]) - ord("A")
        direction = placement.direction
        ship_length = self.SHIP_LENGTHS[placement.ship_type]

        if direction == "horizontal" and (col + ship_length - 1) > 9:
            raise ValueError("Ship extends beyond board boundaries.")
        if direction == "vertical" and (row + ship_length - 1) > 10:
            raise ValueError("Ship extends beyond board boundaries.")

        for i in range(ship_length):
            if direction == "horizontal":
                position = (row, col + i)
            else:
                position = (row + i, col)

            if position in self.games[game_id].board:
                raise ValueError(
                    "Overlapping with another ship. Cannot place ship in the chosen position."
                )

    def create_turn(self, game_id: str, turn: Turn) -> TurnResponse:

        if game_id not in self.games:
            raise ValueError("Game not found!")

        if len(self.games[game_id].ships) < len(self.SHIP_LENGTHS):
            raise ValueError("All ships must be placed before starting turns")

        row, col = turn.target["row"], ord(turn.target["column"]) - ord("A")
        result = "miss"
        ship_type = None

        if (row, col) in self.games[game_id].board:
            result = "hit"
            ship_type = self.games[game_id].board[(row, col)]

            self.games[game_id].board[(row, col)] = result

            if self._is_ship_sunk(game_id, ship_type):
                result = "sunk"

        else:

            self.games[game_id].board[(row, col)] = result

        self.games[game_id].turns.append(turn)

        return TurnResponse(result=result, ship_type=ship_type)

    def _is_ship_sunk(self, game_id: str, ship_type: str) -> bool:
        board = self.games[game_id].board
        hits = [k for k, v in board.items() if v == "hit"]
        ship_positions = [k for k, v in board.items() if v == ship_type]

        return all(position in hits for position in ship_positions)

    def _are_all_ships_sunk(self, game_id: str) -> bool:

        for ship_type in self.SHIP_LENGTHS:
            if not self._is_ship_sunk(game_id, ship_type):
                return False
        return True

    def get_game_status(self, game_id: str) -> GameStatus:
        is_all_ships_sunk = self._are_all_ships_sunk(game_id)

        last_turn_player = (
            "Player1" if len(self.games[game_id].turns) % 2 != 0 else "Player2"
        )
        winner = last_turn_player if is_all_ships_sunk else None

        return GameStatus(is_game_over=is_all_ships_sunk, winner=winner)

    def get_winner(self, game_id: str) -> str:

        return "No winner yet"

    def get_game(self, game_id: str) -> Game:

        return self.games.get(game_id)

    def delete_game(self, game_id: str) -> None:
        if game_id in self.games:
            del self.games[game_id]

    def create_game(self, game_id: str = None) -> str:
        if not game_id:
            game_id = str(uuid.uuid4())

        self.games[game_id] = Game(
            game_id=game_id, players=[], board={}, ships=[], turns=[]
        )
        return game_id
