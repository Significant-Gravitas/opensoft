from typing import List

from sqlmodel import Session

from pages import engine
from pages.battleship_v3.models import (
    AbstractBattleshipV3,
    Direction,
    Game,
    GameStatus,
    GameStatusEnum,
    Player,
    ShipPlacement,
    ShipType,
    Turn,
    TurnResult,
)


class BattleshipV31(AbstractBattleshipV3):
    @classmethod
    def create_game(cls, player_ids: List[int]) -> int:
        new_game = Game(
            player1_id=player_ids[0], player2_id=player_ids[1], is_game_over=False
        )

        with Session(engine) as session:
            session.add(new_game)
            session.commit()
            game_id = new_game.id

        return game_id

    @classmethod
    def create_ship_placement(
        cls, game_id: int, player_id: int, placement: ShipPlacement
    ) -> None:
        placement.player_id = player_id

        occupied_squares = cls._get_occupied_squares(placement)

        with Session(engine) as session:

            for square in occupied_squares:
                existing_ship = (
                    session.query(ShipPlacement)
                    .filter(
                        ShipPlacement.game_id == game_id,
                        ShipPlacement.start_row == square[0],
                        ShipPlacement.start_column == square[1],
                        ShipPlacement.player_id == player_id,
                    )
                    .first()
                )

                if existing_ship:
                    raise ValueError("Ships overlap.")

            session.add(placement)
            session.commit()

    @classmethod
    def _get_occupied_squares(cls, placement: ShipPlacement) -> List[tuple]:
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
        with Session(engine) as session:

            turn_count = session.query(Turn).filter(Turn.game_id == game_id).count()
            current_player_id = (turn_count % 2) + 1

            player1_ships_placed = session.query(ShipPlacement).filter(
                ShipPlacement.game_id == game_id,
                ShipPlacement.player_id == current_player_id,
            ).count() == len(cls.SHIP_LENGTHS)

            other_player_id = 1 if current_player_id == 2 else 2
            player2_ships_placed = session.query(ShipPlacement).filter(
                ShipPlacement.game_id == game_id,
                ShipPlacement.player_id == other_player_id,
            ).count() == len(cls.SHIP_LENGTHS)

            if not (player1_ships_placed and player2_ships_placed):
                raise ValueError("All ships must be placed before starting to hit")

            target_ship_placement = (
                session.query(ShipPlacement)
                .filter(
                    ShipPlacement.game_id == game_id,
                    ShipPlacement.start_row <= turn.target_row,
                    ShipPlacement.start_column <= turn.target_column,
                )
                .first()
            )

            if not target_ship_placement:
                turn.result = TurnResult.MISS
                session.add(turn)
                session.commit()
                return TurnResult.MISS

            occupied_squares = cls._get_occupied_squares(target_ship_placement)

            if (turn.target_row, turn.target_column) in occupied_squares:
                turn.result = TurnResult.HIT

                all_squares_hit = all(
                    session.query(Turn)
                    .filter(
                        Turn.game_id == game_id,
                        Turn.target_row == square[0],
                        Turn.target_column == square[1],
                        Turn.result == TurnResult.HIT,
                    )
                    .first()
                    for square in occupied_squares
                    if (square[0] != turn.target_row or square[1] != turn.target_column)
                )

                if (
                    all_squares_hit
                    and len(occupied_squares)
                    == cls.SHIP_LENGTHS[target_ship_placement.ship_type]
                ):
                    turn.result = TurnResult.SUNK

                session.add(turn)
                session.commit()
                return turn.result

            turn.result = TurnResult.MISS
            session.add(turn)
            session.commit()
            return TurnResult.MISS

    @classmethod
    def get_game_status(cls, game_id: int) -> GameStatus:
        with Session(engine) as session:
            game = session.query(Game).filter(Game.id == game_id).first()

            if game.is_game_over:
                return GameStatus(
                    is_game_over=True,
                    winner_id=game.winner_id,
                    status=GameStatusEnum.PLAYER1_WIN
                    if game.winner_id == game.player1_id
                    else GameStatusEnum.PLAYER2_WIN,
                )

            def are_all_ships_sunk(player_ships):
                all_sunk = all(
                    all(
                        session.query(Turn)
                        .filter(
                            Turn.game_id == game_id,
                            Turn.target_row == square[0],
                            Turn.target_column == square[1],
                            Turn.result == TurnResult.HIT,
                        )
                        .first()
                        for square in cls._get_occupied_squares(ship)
                    )
                    for ship in player_ships
                )
                return all_sunk

            player1_ships = (
                session.query(ShipPlacement)
                .filter(
                    ShipPlacement.game_id == game_id,
                    ShipPlacement.player_id == game.player1_id,
                )
                .all()
            )

            if are_all_ships_sunk(player1_ships):
                game.is_game_over = True
                game.winner_id = game.player2_id
                session.commit()
                return GameStatus(
                    is_game_over=True,
                    winner_id=game.player2_id,
                    status=GameStatusEnum.PLAYER2_WIN,
                )

            player2_ships = (
                session.query(ShipPlacement)
                .filter(
                    ShipPlacement.game_id == game_id,
                    ShipPlacement.player_id == game.player2_id,
                )
                .all()
            )

            if are_all_ships_sunk(player2_ships):
                game.is_game_over = True
                game.winner_id = game.player1_id
                session.commit()
                return GameStatus(
                    is_game_over=True,
                    winner_id=game.player1_id,
                    status=GameStatusEnum.PLAYER1_WIN,
                )

        return GameStatus(
            is_game_over=False, winner_id=None, status=GameStatusEnum.ONGOING
        )

    @classmethod
    def get_game(cls, game_id: int) -> Game:
        with Session(engine) as session:
            return session.query(Game).filter(Game.id == game_id).first()

    @classmethod
    def delete_game(cls, game_id: int) -> None:

        pass

    @classmethod
    def create_player(cls, name: str) -> int:

        pass

    @classmethod
    def get_player(cls, player_id: int) -> Player:

        pass

    @classmethod
    def get_ship_placement(cls, game_id: int, ship_type: ShipType) -> ShipPlacement:
        with Session(engine) as session:
            return (
                session.query(ShipPlacement)
                .filter(
                    ShipPlacement.game_id == game_id,
                    ShipPlacement.ship_type == ship_type,
                )
                .first()
            )
