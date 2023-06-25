from dataclasses import dataclass

from config import PLAYER


@dataclass
class Player:
    id: int
    hp: int = PLAYER.INITIAL_HP
    power: int = 2

    def __repr__(self) -> str:
        return f'P{self.id}: {self.hp}' if self.hp > 0 else 'KILLED'
