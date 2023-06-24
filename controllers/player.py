from schemas.player import Player


class _PlayerController:
    def __init__(self) -> None:
        self.players = {1: Player(id=1, hp=10), 2: Player(id=2, hp=10)}

    def get_player(self, id: int) -> Player:
        if not (player := self.players.get(id)):
            raise ValueError('Player not found')
        
        return player

PlayerController = _PlayerController()