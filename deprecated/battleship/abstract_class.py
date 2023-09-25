from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel, validator


class ShipPlacement(BaseModel):
    ship_type: str
    start: dict
    direction: str

    @validator("start")
    def validate_start(cls, start):
        row, column = start.get("row"), start.get("column")

        if not (1 <= row <= 10):
            raise ValueError("Row must be between 1 and 10 inclusive.")

        if column not in list("ABCDEFGHIJ"):
            raise ValueError("Column must be one of A, B, C, D, E, F, G, H, I, J.")

        return start


class Turn(BaseModel):
    target: dict


class TurnResponse(BaseModel):
    result: str
    ship_type: Optional[str]


class GameStatus(BaseModel):
    is_game_over: bool
    winner: Optional[str]


from typing import List


class Game(BaseModel):
    game_id: str
    players: List[str]
    board: dict
    ships: List[ShipPlacement]
    turns: List[Turn]


class AbstractBattleship(ABC):
    SHIP_LENGTHS = {
        "carrier": 5,
        "battleship": 4,
        "cruiser": 3,
        "submarine": 3,
        "destroyer": 2,
    }

    @abstractmethod
    def create_ship_placement(self, game_id: str, placement: ShipPlacement) -> None:

        pass

    @abstractmethod
    def create_turn(self, game_id: str, turn: Turn) -> TurnResponse:

        pass

    @abstractmethod
    def get_game_status(self, game_id: str) -> GameStatus:

        pass

    @abstractmethod
    def get_winner(self, game_id: str) -> str:

        pass

    @abstractmethod
    def get_game(self) -> Game:

        pass

    @abstractmethod
    def delete_game(self, game_id: str) -> None:

        pass

    @abstractmethod
    def create_game(self) -> None:

        pass
