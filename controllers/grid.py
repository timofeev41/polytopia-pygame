from config import GRID
from controllers.player import PlayerController
from schemas.player import Player


class _GridController:
    def __init__(self) -> None:
        _grid = self._init_grid()
        self.grid = self._fill_grid(_grid)

    def get_grid(self):
        return self.grid

    def _fill_grid(self, grid: list[list[Player | None]]):
        new_grid = grid.copy()
        new_grid[0][0] = PlayerController.get_player(1)
        new_grid[-1][-1] = PlayerController.get_player(2)
        return new_grid

    def _init_grid(self):
        """Create simple 10x10 grid."""
        grid = []
        for row in range(GRID.GRID_SIZE):
            grid.append([])
            for _ in range(GRID.GRID_SIZE):
                grid[row].append(None)
        return grid
    
    def get_by_xy(self, x, y):
        return self.grid[x][y]
    
    def swap(self, start, end):
        self.grid[start[0]][start[1]] = self.grid[end[0]][end[1]] 
        self.grid[end[0]][end[1]] = None

    def modify_player(self, x: int, y: int, damage: int) -> bool:
        """returns true if modified, false if not (may be killed)"""
        cell = self.grid[x][y]
        if not isinstance(cell, Player):
            raise ValueError('Attacking empty cell instead of player!')
            
        if cell.hp - damage <= 0:
            return False
        cell.hp -= damage
        return True
    
    def flush_cell(self, x: int, y: int):
        self.grid[x][y] = None

    def check_alive_units(self, id: int) -> bool:
        """if all units are dead return false else true"""
        for row in self.grid:
            for val in row:
                if isinstance(val, Player):
                    if val.id == id:
                        return True
        return False

        


GridController = _GridController()


def create_game(amount_players: int = 2):
    return GridController.get_grid()

