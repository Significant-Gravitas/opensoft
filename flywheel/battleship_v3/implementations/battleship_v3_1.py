from typing import List

from sqlmodel import Session

from flywheel import engine
from flywheel.battleship_v3.abstract_class import AbstractBattleshipV3, ShipPlacement, Turn, TurnResult, GameStatus, \
    Game, Player, ShipType


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
        with Session(engine) as session:
            session.add(placement)
            session.commit()


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
