import math
from controllers.grid import GridController
from controllers.player import PlayerController
from logger import logger

from schemas.player import Player


class _MoveController:
    def __init__(self) -> None:
        self.selected_pos = None
        # XXX: Player 1 always starts first
        self._turn_player_id = 1

    def get_turn_player_id(self):
        return self._turn_player_id

    @staticmethod
    def is_valid_move(start, end) -> bool:
        diff = math.floor(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
        return True if diff == 1 else False
    
    @staticmethod
    def is_fight(cell1, cell2) -> bool:
        if isinstance(cell1, Player):
            if isinstance(cell2, Player):
                return True
        return False
    
    def fight(self, start, end):
        player1 = GridController.get_by_xy(*start)
        if not isinstance(player1, Player):
            logger.info(f"Cell {start} not contains fighter")
            return
        
        # if killed don't pass move
        if not GridController.modify_player(*end, damage=player1.power):
            player_id = GridController.get_by_xy(*end).id
            logger.info(f'Player {player_id} killed!')
            GridController.flush_cell(*end)
            PlayerController.verify_elimination(player_id)

    def move(self, row, column):
        current_cell = GridController.get_by_xy(row, column)
        previous_cell: Player | None = None
        if self.selected_pos:
            previous_cell = GridController.get_by_xy(*self.selected_pos)
        if not self.selected_pos:
            if isinstance(current_cell, Player) and current_cell.id == self._turn_player_id:
                self.selected_pos = (row, column)
                logger.info(f"Player {self._turn_player_id}: Selected cell {self.selected_pos} - {(row, column)}")
        else:
            initial_cell: Player = GridController.get_by_xy(*self.selected_pos)
            if not isinstance(current_cell, Player):
                if not self.is_valid_move(self.selected_pos, (row, column)):
                    logger.info("Invalid move")
                    return

                logger.info(f"Player {self._turn_player_id}: Move cell {self.selected_pos} to {(row, column)}")
                GridController.swap((row, column), self.selected_pos)
                self.selected_pos = None
                self._turn_player_id = PlayerController.get_next_player(self._turn_player_id).id
            elif isinstance(current_cell, Player) and previous_cell and previous_cell.id != current_cell.id:
                if self.is_fight(initial_cell, current_cell):
                    logger.info(f'Fight: {initial_cell} vs {current_cell}')
                    MoveController.fight(self.selected_pos, (row, column))
                logger.info(f"Player {self._turn_player_id}: Deseleted cell: {self.selected_pos}")
                self.selected_pos = None


MoveController = _MoveController()
