from logger import logger
from schemas.player import Player


class _PlayerController:
    def __init__(self) -> None:
        self.players = {1: Player(id=1), 2: Player(id=2)}

    def get_player(self, id: int) -> Player:
        if not (player := self.players.get(id)):
            raise ValueError('Player not found')
        
        return player
    
    def get_next_player(self, id: int) -> Player:
        if not self.players.get(id):
            raise ValueError('Player not found')

        if not (next_player := self.players.get((id % len(self.players)) + 1)):
            raise ValueError('Next player not found')
        
        return next_player

    def verify_elimination(self, id: int):
        from controllers.grid import GridController

        if not GridController.check_alive_units(id):
            logger.info(f'eliminated player {id}, game ended')
            del self.players[id]


PlayerController = _PlayerController()