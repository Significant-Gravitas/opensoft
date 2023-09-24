from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

from src.base_class import BaseClass


class Direction(str, Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class ShipType(str, Enum):
    CARRIER = "carrier"
    BATTLESHIP = "battleship"
    CRUISER = "cruiser"
    SUBMARINE = "submarine"
    DESTROYER = "destroyer"


class TurnResult(str, Enum):
    HIT = "hit"
    MISS = "miss"
    SUNK = "sunk"


class GameStatusEnum(str, Enum):
    ONGOING = "ongoing"
    DRAW = "draw"
    PLAYER1_WIN = "player1_win"
    PLAYER2_WIN = "player2_win"


class Player(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str


class Game(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    player1_id: int = Field(foreign_key="player.id")
    player2_id: int = Field(foreign_key="player.id")
    is_game_over: bool = Field(default=False)
    winner_id: Optional[int] = Field(None, foreign_key="player.id")


class ShipPlacement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    ship_type: ShipType
    start_row: int
    start_column: str
    direction: Direction

    @staticmethod
    def validate_start(row, column):
        if not (1 <= row <= 10):
            raise ValueError("Row must be between 1 and 10 inclusive.")
        if column not in list("ABCDEFGHIJ"):
            raise ValueError("Column must be one of A, B, C, D, E, F, G, H, I, J.")
        return row, column


class Turn(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    target_row: int
    target_column: str
    result: TurnResult
    hit_ship_type: Optional[ShipType]


class GameStatus(BaseModel):
    is_game_over: bool
    winner_id: Optional[int]
    status: GameStatusEnum


class AbstractBattleshipV2(ABC, BaseClass):
    SHIP_LENGTHS = {
        "carrier": 5,
        "battleship": 4,
        "cruiser": 3,
        "submarine": 3,
        "destroyer": 2,
    }

    @classmethod
    @abstractmethod
    def create_game(cls, player_ids: List[int]) -> int:

        pass

    @classmethod
    @abstractmethod
    def create_ship_placement(cls, game_id: int, placement: ShipPlacement) -> None:

        pass

    @classmethod
    @abstractmethod
    def create_turn(cls, game_id: int, turn: Turn) -> TurnResult:

        pass

    @classmethod
    @abstractmethod
    def get_game_status(cls, game_id: int) -> GameStatus:

        pass

    @classmethod
    @abstractmethod
    def get_game(cls, game_id: int) -> Game:

        pass

    @classmethod
    @abstractmethod
    def delete_game(cls, game_id: int) -> None:

        pass

    @classmethod
    @abstractmethod
    def delete_game(cls, game_id: int) -> None:

        pass

    @classmethod
    @abstractmethod
    def create_player(cls, name: str) -> int:
        pass

    @classmethod
    @abstractmethod
    def get_player(cls, player_id: int) -> Player:
        pass


class TurnResponse(BaseModel):
    result: TurnResult
    ship_type: Optional[ShipType]
