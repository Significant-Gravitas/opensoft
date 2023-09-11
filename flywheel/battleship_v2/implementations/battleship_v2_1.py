from typing import List, Optional

from sqlmodel import Session

from flywheel import engine
from flywheel.battleship_v2.abstract_class import (
    AbstractBattleshipV2,
    Direction,
    Game,
    GameStatus,
    GameStatusEnum,
    Player,
    ShipPlacement,
    ShipType,
    Turn,
    TurnResponse,
    TurnResult,
)


class BattleshipV21(AbstractBattleshipV2):
    @classmethod
    def create_game(cls, player_ids: List[int]) -> int:
        new_game = Game(player1_id=player_ids[0], player2_id=player_ids[1])

        with Session(engine) as session:
            session.add(new_game)
            session.commit()
            game_id = new_game.id

        return game_id

    @classmethod
    def _determine_hit_ship(
        cls, game_id: int, target_row: int, target_column: str
    ) -> Optional[ShipType]:
        with Session(engine) as session:
            placements = session.query(ShipPlacement).filter_by(game_id=game_id).all()

            for placement in placements:
                ship_length = cls.SHIP_LENGTHS[placement.ship_type]

                if placement.direction == Direction.HORIZONTAL:
                    if (
                        placement.start_row == target_row
                        and ord(placement.start_column)
                        <= ord(target_column)
                        <= ord(placement.start_column) + ship_length - 1
                    ):
                        return placement.ship_type
                else:
                    if (
                        placement.start_column == target_column
                        and placement.start_row
                        <= target_row
                        <= placement.start_row + ship_length - 1
                    ):
                        return placement.ship_type

        return None

    @classmethod
    def create_ship_placement(cls, game_id: int, placement: ShipPlacement) -> None:

        placement.validate_start(placement.start_row, placement.start_column)

        ship_length = cls.SHIP_LENGTHS[placement.ship_type]

        if placement.direction == Direction.HORIZONTAL:
            if not (1 <= ord(placement.start_column) - 65 + ship_length <= 10):
                raise ValueError("The ship doesn't fit horizontally.")
        else:
            if not (1 <= placement.start_row + ship_length <= 10):
                raise ValueError("The ship doesn't fit vertically.")

        with Session(engine) as session:

            existing_placements = (
                session.query(ShipPlacement).filter_by(game_id=game_id).all()
            )
            for existing in existing_placements:

                pass

            session.add(placement)
            session.commit()

    @classmethod
    def create_turn(cls, game_id: int, turn: Turn) -> TurnResponse:

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
    def get_game_status(cls, game_id: int) -> GameStatus:
        with Session(engine) as session:
            game = session.get(Game, game_id)

        if not game:
            raise ValueError(f"No game found with the ID: {game_id}")

        if game.is_game_over:
            return GameStatus(
                is_game_over=True,
                winner_id=game.winner_id,
                status=GameStatusEnum.PLAYER1_WIN
                if game.winner_id == game.player1_id
                else GameStatusEnum.PLAYER2_WIN,
            )
        else:
            return GameStatus(
                is_game_over=False,
                winner_id=None,
                status=GameStatusEnum.ONGOING,
            )

    @classmethod
    def get_game(cls, game_id: int) -> Game:
        with Session(engine) as session:
            game = session.get(Game, game_id)
        return game

    @classmethod
    def delete_game(cls, game_id: int) -> None:
        with Session(engine) as session:
            game = session.get(Game, game_id)
            if game:
                session.delete(game)
                session.commit()

    @classmethod
    def create_player(cls, name: str) -> int:
        new_player = Player(name=name)

        with Session(engine) as session:
            session.add(new_player)
            session.commit()
            player_id = new_player.id

        return player_id

    @classmethod
    def get_player(cls, player_id: int) -> Player:
        with Session(engine) as session:
            player = session.get(Player, player_id)
        return player
