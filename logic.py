from dataclasses import dataclass
import math


@dataclass
class Player:
    id: int
    hp: int = 10
    power: int = 2

    def __repr__(self) -> str:
        return f'P{self.id}: {self.hp}' if self.hp > 0 else 'KILLED'


class _GridController:
    def __init__(self) -> None:
        _grid = self._init_grid()
        self.grid = self._fill_grid(_grid)

    def get_grid(self):
        return self.grid

    def _fill_grid(self, grid: list[list[Player | None]]):
        new_grid = grid.copy()
        new_grid[0][0] = Player(id=1, hp=10)
        new_grid[-1][-1] = Player(id=2, hp=10)
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

    def modify_player(self, x, y, damage: int):
        cell = self.grid[x][y]
        if not isinstance(cell, Player):
            print('Attacking empty cell instead of player!')
            return
    
        cell.hp -= damage



GridController = _GridController()


class _MoveController:
    def __init__(self) -> None:
        self.selected_pos = None

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
        player1 = GridController.get_by_xy(start[0], start[1])
        if not isinstance(player1, Player):
            print(f"Cell {start, end} not contains fighter")
            return
        
        GridController.modify_player(end[0], end[1], player1.power)

    def move(self, row, column):
        current_cell = GridController.get_by_xy(row, column)
        if not self.selected_pos:
            if isinstance(current_cell, Player) and current_cell.id == 1:
                self.selected_pos = (row, column)
                print(f"Selected cell {self.selected_pos} - {(row, column)}")
        else:
            initial_cell: Player = GridController.get_by_xy(*self.selected_pos)
            if not isinstance(current_cell, Player):
                if not self.is_valid_move(self.selected_pos, (row, column)):
                    print("Invalid move")
                    return

                print(f"Move cell {self.selected_pos} to {(row, column)}")
                GridController.swap((row, column), self.selected_pos)
                self.selected_pos = None
            elif isinstance(current_cell, Player) and current_cell.id != 1:
                if self.is_fight(initial_cell, current_cell):
                    print(f'Fight: {initial_cell} vs {current_cell}')
                    GridController.modify_player(row, column, initial_cell.power)
                    return
                print(f"Deseleted cell: {self.selected_pos}")
                self.selected_pos = None


MoveController = _MoveController()
