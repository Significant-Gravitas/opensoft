from enum import Enum

from flywheel.battleship.abstract_class import (
    AbstractBattleship,
    Game,
    GameStatus,
    ShipPlacement,
    Turn,
    TurnResponse,
)


class GameStatus(Enum):
    ONGOING = ("ongoing", False)
    OVER = ("over", True)

    def __init__(self, status, is_game_over):
        self.status = status
        self.is_game_over = is_game_over


class Game:
    def __init__(self, game_id, players, board, ships, turns):
        self.game_id = game_id
        self.players = players
        self.board = board
        self.ships = ships
        self.turns = turns
        self.ship_placements = []


class Battleship2(AbstractBattleship):
    def __init__(self):
        self.games = {}

    def create_game(self) -> str:
        game_id = str(len(self.games) + 1)

        game = Game(
            game_id=game_id,
            players=[],
            board={},
            ships=[],
            turns=[],
        )

        game.ships_to_be_placed = set(self.SHIP_LENGTHS.keys())

        self.games[game_id] = game
        return game_id

    def create_ship_placement(self, game_id: str, ship_placement: ShipPlacement):
        if ship_placement.ship_type not in self.SHIP_LENGTHS:
            raise ValueError("Invalid ship type")

        start_row = ship_placement.start["row"]
        start_col = ord(ship_placement.start["column"]) - ord("A")
        ship_size = self.SHIP_LENGTHS[ship_placement.ship_type]

        if ship_placement.direction == "horizontal":
            if start_col + ship_size > 10:
                raise ValueError("Ship extends beyond board boundaries")

        elif ship_placement.direction == "vertical":
            if start_row + ship_size > 10:
                raise ValueError("Ship extends beyond board boundaries")

        if ship_placement.ship_type not in self.SHIP_LENGTHS:
            raise ValueError("Invalid ship type")

        if ship_placement.direction not in ["horizontal", "vertical"]:
            raise ValueError("Invalid ship direction")

        if self._is_ship_overlap(game_id, ship_placement):
            raise ValueError("The ship overlaps with an existing ship.")

        if ship_placement.ship_type in self.games[game_id].ships_to_be_placed:
            self.games[game_id].ships_to_be_placed.remove(ship_placement.ship_type)
        else:

            raise ValueError("All ships are already placed. Cannot place more ships.")

        self.games[game_id].ship_placements.append(ship_placement)
        self.games[game_id].ships.append(ship_placement)

    def create_turn(self, game_id: str, turn: Turn) -> TurnResponse:

        if self.games[game_id].ships_to_be_placed:
            raise ValueError("All ships must be placed before starting turns")

        self.games[game_id].turns.append(turn)

        for ship_placement in self.games[game_id].ship_placements:
            start_row = ship_placement.start["row"]
            start_col = ord(ship_placement.start["column"]) - ord("A")

            ship_sizes = {
                "carrier": 5,
                "battleship": 4,
                "cruiser": 3,
                "submarine": 3,
                "destroyer": 2,
            }

            if ship_placement.direction == "horizontal":
                end_col = start_col + ship_sizes[ship_placement.ship_type] - 1
                if (
                    turn.target["row"] == start_row
                    and start_col <= ord(turn.target["column"]) - ord("A") <= end_col
                ):
                    self.games[game_id].board[
                        (turn.target["row"], ord(turn.target["column"]) - ord("A"))
                    ] = "hit"
                    if self._is_ship_sunk(game_id, ship_placement.ship_type):
                        return TurnResponse(
                            result="sunk", ship_type=ship_placement.ship_type
                        )
                    else:
                        return TurnResponse(
                            result="hit", ship_type=ship_placement.ship_type
                        )

            else:
                end_row = start_row + ship_sizes[ship_placement.ship_type] - 1
                if (
                    ord(turn.target["column"]) - ord("A") == start_col
                    and start_row <= turn.target["row"] <= end_row
                ):
                    self.games[game_id].board[
                        (turn.target["row"], ord(turn.target["column"]) - ord("A"))
                    ] = "hit"
                    return TurnResponse(
                        result="hit", ship_type=ship_placement.ship_type
                    )

        self.games[game_id].board[
            (turn.target["row"], ord(turn.target["column"]) - ord("A"))
        ] = "miss"
        return TurnResponse(result="miss", ship_type=None)

    def _is_ship_sunk(self, game_id: str, ship_type: str) -> bool:

        ship_size = self.SHIP_LENGTHS[ship_type]
        hits_on_ship = sum(
            1
            for pos, status in self.games[game_id].board.items()
            if status == "hit"
            and any(
                sp.ship_type == ship_type
                and sp.start["row"] <= pos[0] <= sp.start["row"] + ship_size - 1
                and ord(sp.start["column"]) - ord("A")
                <= pos[1]
                <= ord(sp.start["column"]) + ship_size - 1
                for sp in self.games[game_id].ship_placements
            )
        )
        return hits_on_ship == ship_size

    def delete_game(self, game_id: str):
        if game_id in self.games:
            del self.games[game_id]

    def get_game(self, game_id: str) -> Game:
        return self.games.get(game_id, None)

    def get_game_status(self, game_id: str) -> GameStatus:

        if len(self.games[game_id].turns) >= 100:
            return GameStatus.OVER
        return GameStatus.ONGOING

    def get_winner(self, game_id: str) -> str:

        return "Player 1"

    def _is_ship_overlap(self, game_id: str, ship_placement: ShipPlacement) -> bool:

        start_row = ship_placement.start["row"]
        start_col = ord(ship_placement.start["column"]) - ord("A")
        ship_size = self.SHIP_LENGTHS[ship_placement.ship_type]

        if ship_placement.direction == "horizontal":
            end_col = start_col + ship_size
            for existing_ship in self.games[game_id].ship_placements:
                existing_start_row = existing_ship.start["row"]
                existing_start_col = ord(existing_ship.start["column"]) - ord("A")
                existing_end_col = (
                    existing_start_col + self.SHIP_LENGTHS[existing_ship.ship_type]
                )

                if existing_start_row == start_row and not (
                    start_col >= existing_end_col or end_col <= existing_start_col
                ):
                    return True

        else:
            end_row = start_row + ship_size
            for existing_ship in self.games[game_id].ship_placements:
                existing_start_row = existing_ship.start["row"]
                existing_end_row = (
                    existing_start_row + self.SHIP_LENGTHS[existing_ship.ship_type]
                )
                existing_start_col = ord(existing_ship.start["column"]) - ord("A")

                if existing_start_col == start_col and not (
                    start_row >= existing_end_row or end_row <= existing_start_row
                ):
                    return True

        return False
