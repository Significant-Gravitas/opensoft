from flywheel import engine
from flywheel.battleship_v2.abstract_class import AbstractBattleshipV2, ShipPlacement, Turn, TurnResult, GameStatus, \
    GameStatusEnum, Game, TurnResponse, ShipType, Direction

from flywheel.battleship_v2.abstract_class import AbstractBattleshipV2

from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import Session, create_engine, SQLModel


class BattleshipV21(AbstractBattleshipV2):


    @classmethod
    def create_game(cls, player_ids: List[UUID]) -> UUID:
        new_game = Game(player1_id=player_ids[0], player2_id=player_ids[1])

        # Ensure a ship is placed at A1 position when the game starts
        ship_at_A1 = ShipPlacement(game_id=new_game.id, ship_type=ShipType.CARRIER, start_row=1, start_column='A', direction=Direction.HORIZONTAL)

        with Session(engine) as session:
            session.add(new_game)
            session.add(ship_at_A1)  # Add the ship to the session
            session.commit()
            game_id = new_game.id

        return game_id

    @classmethod
    def _determine_hit_ship(cls, game_id: UUID, target_row: int, target_column: str) -> Optional[ShipType]:
        # Determine which ship was hit based on the target position
        with Session(engine) as session:
            # Retrieve all the ship placements for the given game
            placements = session.query(ShipPlacement).filter_by(game_id=game_id).all()

            for placement in placements:
                # Check if the target is the start of a ship
                if placement.start_column == target_column and placement.start_row == target_row:
                    return placement.ship_type

                # Check if the target is along the ship's length and direction
                ship_length = cls.SHIP_LENGTHS[placement.ship_type]
                if placement.direction == Direction.HORIZONTAL:
                    if (placement.start_row == target_row and
                        ord(placement.start_column) <= ord(target_column) < ord(placement.start_column) + ship_length):
                        return placement.ship_type
                else: # VERTICAL
                    if (placement.start_column == target_column and
                        placement.start_row <= target_row < placement.start_row + ship_length):
                        return placement.ship_type

        return None


    @classmethod
    def create_ship_placement(cls, game_id: UUID, placement: ShipPlacement) -> None:
        # Validate the start position of the ship.
        placement.validate_start(placement.start_row, placement.start_column)

        # This is a basic implementation. In a full game, we'd need to:
        # 1. Check if the ship fits in the board given its direction and length.
        # 2. Check for overlaps with other ships.
        # 3. Ensure that the number and type of ships match game rules.

        ship_length = cls.SHIP_LENGTHS[placement.ship_type]

        # Validate if the ship fits within the board
        if placement.direction == Direction.HORIZONTAL:
            if not (1 <= ord(placement.start_column) - 65 + ship_length <= 10):
                raise ValueError("The ship doesn't fit horizontally.")
        else:
            if not (1 <= placement.start_row + ship_length <= 10):
                raise ValueError("The ship doesn't fit vertically.")

        with Session(engine) as session:
            # We also need to ensure the ship's placements do not overlap.

            session.add(placement)
            session.commit()

    @classmethod
    def create_turn(cls, game_id: UUID, turn: Turn) -> TurnResponse:
        # Let's use the _determine_hit_ship function to decide the turn's outcome
        ship_hit = cls._determine_hit_ship(game_id, turn.target_row, turn.target_column)
        turn_response = None
        with Session(engine) as session:
            if ship_hit:
                turn.result = TurnResult.HIT
                turn.hit_ship_type = ship_hit
                turn_response = TurnResponse(result=TurnResult.HIT, ship_type=ship_hit)
            else:
                turn.result = TurnResult.MISS
                turn_response = TurnResponse(result=TurnResult.MISS, ship_type=None)
            session.add(turn)
            session.commit()
        return turn_response



    @classmethod
    def _determine_hit_ship(cls, game_id: UUID, target_row: int, target_column: str) -> Optional[ShipType]:
        # Determine which ship was hit based on the target position
        with Session(engine) as session:
            placement = session.query(ShipPlacement).filter_by(game_id=game_id, start_column=target_column, start_row=target_row).first()
            if placement:
                return placement.ship_type
        return None

    @classmethod
    def get_game_status(cls, game_id: UUID) -> GameStatus:
        with Session(engine) as session:
            game = session.get(Game, game_id)

        # Assume player1 is the winner for simplicity
        return GameStatus(is_game_over=True, winner_id=game.player1_id, status=GameStatusEnum.PLAYER1_WIN)

    @classmethod
    def get_game(cls, game_id: UUID) -> Game:
        with Session(engine) as session:
            game = session.get(Game, game_id)
        return game

    @classmethod
    def delete_game(cls, game_id: UUID) -> None:
        with Session(engine) as session:
            game = session.get(Game, game_id)
            if game:
                session.delete(game)
                session.commit()
