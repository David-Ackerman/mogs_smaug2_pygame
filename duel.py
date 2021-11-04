from typing import List
from interfaces.card_model import Deck

plays = {
    "R": {"R": -1, "S": 0, "P": 1},
    "S": {"S": -1, "P": 0, "R": 1},
    "P": {"P": -1, "R": 0, "S": 1}
}


class Duel:
    def __init__(self, id: str, playerI: 0 | 1):
        self.playerTime = playerI
        self.duelInit = False
        self.turn = 0
        self.player1 = {}
        self.player2 = {}
        self.p1Went: bool = False
        self.p2Went: bool = False
        self.ready: bool = False
        self.id: str = id
        self.moves: List[str | None] = [None, None]
        self.wins: List[int] = [0, 0]
        self.ties: int = 0

    def isMyTurn(self, player: int):
        if player == self.playerTime:
            return True
        else:
            return False

    def changePlayerTime(self):
        if self.playerTime == 1:
            self.playerTime = 0
        else:
            self.playerTime = 1
        self.turn = 1

    def setPlayerCards(self, player, newCards):
        if player == 0:
            self.player1 = {
                'deck': newCards['deck'],
                'hand': newCards['hand'],
                'grave': newCards['grave']
            }
        else:
            self.player2 = {
                'deck': newCards['deck'],
                'hand': newCards['hand'],
                'grave': newCards['grave']
            }

    def getOpponentCards(self, player):
        if player == 0:
            return self.player2
        else:
            return self.player1

    def changeTurn(self):
        if self.turn < 3:
            self.turn += 1
        else:
            self.changePlayerTime()

    def connected(self) -> bool:
        return self.ready

    def get_player_move(self, p: 0 | 1) -> str:
        return self.moves[p]

    def play(self, player: int, move: str):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True
