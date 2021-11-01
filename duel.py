from typing import List

plays = {
    "R": {"R": -1, "S": 0, "P": 1},
    "S": {"S": -1, "P": 0, "R": 1},
    "P": {"P": -1, "R": 0, "S": 1}
}


class Duel:
    def __init__(self, id: str):
        self.p1Went: bool = False
        self.p2Went: bool = False
        self.ready: bool = False
        self.id: str = id
        self.moves: List[str | None] = [None, None]
        self.wins: List[int] = [0, 0]
        self.ties: int = 0

    def get_player_move(self, p: 0 | 1) -> str:
        return self.moves[p]

    def play(self, player: int, move: str):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self) -> bool:
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went

    def winner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = plays[p1][p2]
        return winner

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
