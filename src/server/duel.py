class Duel:
    def __init__(self, id: str, playerI: 0 | 1):
        self.playerTime = playerI
        self.duelInit = False
        self.turn = 0
        self.round = 1
        self.players = {}
        self.selectedAttackedP1 = ''
        self.selectedAttackedP2 = ''
        self.ready: bool = False
        self.id: str = id

    def getLifeMana(self, username: str):
        for player in self.players.keys():
            if player == username:
                p1 = self.players[player]
                p1name = username[:-1]
            else:
                p2 = self.players[player]
                p2name = username[:-1]

        return [(p1['mana'], p1['life'], p1name), (p2['mana'], p2['life'], p2name)]

    def isMyTurn(self, username: str):
        if int(username[-1:]) == self.playerTime:
            return True
        else:
            return False

    def getOpponentCards(self, username: str):
        for player in self.players.keys():
            if player != username:
                return self.players[player]

    def getMyFieldCards(self, username: str):
        return self.players[username]

    def connected(self) -> bool:
        return self.ready
