from typing import List
from interfaces.card_model import Deck


class Duel:
    def __init__(self, id: str, playerI: 0 | 1):
        self.playerTime = playerI
        self.duelInit = False
        self.turn = 0
        self.round = 1
        self.player1 = {}
        self.player2 = {}
        self.selectedAttackedP1 = ''
        self.selectedAttackedP2 = ''
        self.ready: bool = False
        self.id: str = id

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
        self.round += 1

    def setPlayerCards(self, player, newCards):
        if player == 0:
            self.player1 = {
                'deck': newCards['deck'],
                'hand': newCards['hand'],
                'field': newCards['field'],
                'grave': newCards['grave'],
                'enemySelected': self.selectedAttackedP2
            }
        else:
            self.player2 = {
                'deck': newCards['deck'],
                'hand': newCards['hand'],
                'field': newCards['field'],
                'grave': newCards['grave'],
                'enemySelected': self.selectedAttackedP1
            }

    def setBattlePhase(self):
        self.turn = 3

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

    def combat(self, player, attack: Deck, defense: Deck):
        if attack['card_attack'] > defense['card_def']:
            print('destroy defense card')
        elif attack['card_attack'] == defense['card_def']:
            print('destroy two cards')
        elif defense['card_def'] > attack['card_attack']:
            print('destroy attack card')

    def selectEnemyCard(self, player, enemyCard):
        if player == 0:
            self.selectedAttackedP1 = enemyCard
        else:
            self.selectedAttackedP1 = enemyCard

    def connected(self) -> bool:
        return self.ready
