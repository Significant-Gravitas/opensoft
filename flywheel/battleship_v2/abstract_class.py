from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import List, Optional
from enum import Enum


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


class Player(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    games: List["Game"] = Relationship(back_populates="players")


class Game(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    player_ids: List[UUID] = Field()
    players: List[Player] = Relationship(back_populates="games")
    turns: List["Turn"] = Relationship(back_populates="game")
    ship_placements: List["ShipPlacement"] = Relationship(back_populates="game")
    is_game_over: bool = False
    winner_id: Optional[UUID]


class ShipPlacement(SQLModel, table=True):
    id: int = Field(primary_key=True, auto_increment=True)
    game_id: UUID = Field(foreign_key="game.id")
    game: Optional[Game] = Relationship(back_populates="ship_placements")
    ship_type: ShipType
    start_row: int
    start_column: str
    direction: Direction


class Turn(SQLModel, table=True):
    id: int = Field(primary_key=True, auto_increment=True)
    game_id: UUID = Field(foreign_key="game.id")
    game: Optional[Game] = Relationship(back_populates="turns")
    target_row: int
    target_column: str
    result: TurnResult
    hit_ship_type: Optional[ShipType]


class TurnResponse(SQLModel):
    result: str  # Either "hit" or "miss"
    ship_type: str  # The type of ship hit, or None if the result is a "miss"

class AbstractBattleship(ABC):
    @abstractmethod
    def create_game(self, player_ids: List[UUID]) -> UUID:
        """
        Create a new game with the specified players.
        Returns the game_id.
        """
        pass

    @abstractmethod
    def create_ship_placement(self, game_id: UUID, placement: ShipPlacement) -> None:
        """
        Place a ship on the grid for the specified game.
        """
        pass

    @abstractmethod
    def create_turn(self, game_id: UUID, turn: Turn) -> TurnResponse:
        """
        Players take turns to target a grid cell in the specified game.
        """
        pass

    @abstractmethod
    def get_game_status(self, game_id: UUID) -> GameStatus:
        """
        Check if the game is over and get the winner if there's one, for the specified game.
        """
        pass

    @abstractmethod
    def get_game(self, game_id: UUID) -> Game:
        """
        Retrieve the state of the specified game.
        """
        pass

    @abstractmethod
    def delete_game(self, game_id: UUID) -> None:
        """
        Delete a game given its UUID.
        """
        pass
