from typing import List

from sqlmodel import Session

from flywheel import engine
from flywheel.battleship_v3.abstract_class import AbstractBattleshipV3, ShipPlacement, Turn, TurnResult, GameStatus, \
    Game, Player, ShipType, Direction


class BattleshipV31(AbstractBattleshipV3):

    @classmethod
    def create_game(cls, player_ids: List[int]) -> int:
        new_game = Game(player1_id=player_ids[0], player2_id=player_ids[1], is_game_over=False)

        with Session(engine) as session:
            session.add(new_game)
            session.commit()
            game_id = new_game.id

        return game_id

    @classmethod
    def create_ship_placement(cls, game_id: int, placement: ShipPlacement) -> None:
        # 1. Calculate all occupied grid squares for the new placement
        occupied_squares = cls.get_occupied_squares(placement)

        with Session(engine) as session:
            # 2. Check if any of the occupied squares are already taken by another ship for the same game
            for square in occupied_squares:
                existing_ship = session.query(ShipPlacement).filter(
                    ShipPlacement.game_id == game_id,
                    ShipPlacement.start_row == square[0],
                    ShipPlacement.start_column == square[1]
                ).first()

                if existing_ship:
                    raise ValueError("Ships overlap.")

            session.add(placement)
            session.commit()

    @classmethod
    def get_occupied_squares(cls, placement: ShipPlacement) -> List[tuple]:
        length = cls.SHIP_LENGTHS[placement.ship_type]
        occupied_squares = [(placement.start_row, placement.start_column)]

        for _ in range(1, length):
            if placement.direction == Direction.HORIZONTAL:
                occupied_squares.append(
                    (occupied_squares[-1][0], chr(ord(occupied_squares[-1][1]) + 1))
                )
            else:
                occupied_squares.append(
                    (occupied_squares[-1][0] + 1, occupied_squares[-1][1])
                )

        return occupied_squares


    @classmethod
    def create_turn(cls, game_id: int, turn: Turn) -> TurnResult:
        # TODO: implement this method
        pass

    @classmethod
    def get_game_status(cls, game_id: int) -> GameStatus:
        # TODO: implement this method
        pass

    @classmethod
    def get_game(cls, game_id: int) -> Game:
        with Session(engine) as session:
            return session.query(Game).filter(Game.id == game_id).first()

    @classmethod
    def delete_game(cls, game_id: int) -> None:
        # TODO: implement this method
        pass

    @classmethod
    def create_player(cls, name: str) -> int:
        # TODO: implement this method
        pass

    @classmethod
    def get_player(cls, player_id: int) -> Player:
        # TODO: implement this method
        pass

    @classmethod
    def get_ship_placement(cls, game_id: int, ship_type: ShipType) -> ShipPlacement:
        with Session(engine) as session:
            return session.query(ShipPlacement).filter(ShipPlacement.game_id == game_id, ShipPlacement.ship_type == ship_type).first()
