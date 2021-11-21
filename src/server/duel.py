class Duel:
    def __init__(self, id: str, playerI: 0 | 1):
        self.playerTime = playerI
        self.duelInit = False
        self.turn = 0
        self.round = 1
        self.player1 = {
            'mana': 14,
            'life': 200,
            'cards': {
                'hand': [],
                'deck': [],
                'field': {
                    'front': [],
                    'support': []
                },
                'grave': [],
            }
        }
        self.player2 = {
            'mana': 14,
            'life': 200,
            'cards': {
                'hand': [],
                'deck': [],
                'field': {
                    'front': [],
                    'support': []
                },
                'grave': [],
            }
        }
        self.selectedAttackedP1 = ''
        self.selectedAttackedP2 = ''
        self.ready: bool = False
        self.id: str = id

    def getLifeMana(self, player: int):
        if player == 0:
            return [(self.player1['mana'], self.player1['life']), (self.player2['mana'], self.player2['life'])]
        else:
            return [(self.player2['mana'], self.player2['life']), (self.player1['mana'], self.player1['life'])]

    def isMyTurn(self, player: int):
        if player == self.playerTime:
            return True
        else:
            return False

    def getOpponentCards(self, player):
        if player == 0:
            return self.player2
        else:
            return self.player1

    def getMyFieldCards(self, player):
        if player == 0:
            return self.player1
        else:
            return self.player2

    def connected(self) -> bool:
        return self.ready
