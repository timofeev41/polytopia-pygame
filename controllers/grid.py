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
        for row in range(10):
            grid.append([])
            for _ in range(10):
                grid[row].append(None)
        return grid
    
    def get_by_xy(self, x, y):
        return self.grid[x][y]
    
    def swap(self, start, end):
        self.grid[start[0]][start[1]] = self.grid[end[0]][end[1]] 
        self.grid[end[0]][end[1]] = None

    def modify_player(self, x: int, y: int, damage: int):
        cell = self.grid[x][y]
        if not isinstance(cell, Player):
            print('Attacking empty cell instead of player!')
            return
    
        cell.hp -= damage


GridController = _GridController()
