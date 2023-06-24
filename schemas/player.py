from dataclasses import dataclass


@dataclass
class Player:
    id: int
    hp: int = 10
    power: int = 2

    def __repr__(self) -> str:
        return f'P{self.id}: {self.hp}' if self.hp > 0 else 'KILLED'
