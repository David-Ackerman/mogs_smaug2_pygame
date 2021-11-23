import pprint
from src.server.duel import Duel
from src.interfaces.card_model import Deck


class Combat:
    def __init__(self, id: str, duel: Duel):
        self.duelInit = False
        self.selectedAttackedP1 = ''
        self.selectedAttackedP2 = ''
        self.ready: bool = False
        self.turnCounts = 0
        self.game: Duel = duel
        self.id: str = id

    def changePlayerTime(self):
        if self.game.playerTime == 1:
            self.game.playerTime = 0
        else:
            self.game.playerTime = 1
        self.game.turn = 1
        self.game.round += 1
        self.turnCounts += 1
        if self.turnCounts % 2 == 0:
            for key in self.game.players:
                self.game.players[key]['mana'] += 3

    def setPlayerCards(self, username: str, newCards):
        self.game.players[username] = {
            'mana': self.game.players[username]['mana'],
            'life': self.game.players[username]['life'],
            'cards': {
                'deck': newCards['deck'],
                'hand': newCards['hand'],
                'field': self.game.players[username]['cards']['field'],
                'grave': self.game.players[username]['cards']['grave'],
            },
            'enemySelected': self.selectedAttackedP2 if int(username[-1:]) == 0 else self.selectedAttackedP2
        }

    def setBattlePhase(self):
        self.game.turn = 3

    def changeTurn(self):
        if self.game.turn < 3:
            self.game.turn += 1
        else:
            self.changePlayerTime()

    def combat(self, username: str, attack: Deck, defense: Deck = None):
        for player in self.game.players.keys():
            if player == username:
                attacker: str = player
            else:
                defender: str = player

        self.game.players[attacker]['mana'] -= 1
        if defense == None:
            self.game.players[defender]['life'] -= attack['card_attack']
            if self.game.players[defender]['life'] < 0:
                self.game.players[defender]['life'] = 0
            return
        diference = attack['card_attack'] - defense['card_def']
        if diference > 0:
            self.game.players[defender]['life'] -= diference
            if self.game.players[defender]['life'] < 0:
                self.game.players[defender]['life'] = 0
            self.destroyCard(defender, defense)
        elif diference == 0:
            self.destroyCard(defender, defense)
            self.destroyCard(username, attack)
        elif diference < 0:
            self.game.players[attacker]['life'] += diference
            if self.game.players[attacker]['life'] < 0:
                self.game.players[attacker]['life'] = 0
            self.destroyCard(username, attack)

    def summonCard(self, username: str, card: Deck):
        cardPos = 'front' if card['card_type'] != 'spell' and card['card_type'] != 'trap' else 'support'
        self.game.players[username]['cards']['field'][cardPos].append(card)
        if cardPos == 'support':
            return
        self.game.players[username]['mana'] -= card['card_cust']
        return

    def destroyCard(self, playerDestroyed, cardDestroyed: Deck, cardPos='front'):
        player = self.game.players[playerDestroyed]
        cardIndex = player['cards']['field'][cardPos].index(
            cardDestroyed)
        player['cards']['grave'].append(
            player['cards']['field'][cardPos].pop(cardIndex))

    def selectEnemyCard(self, username, enemyCard):
        if int(username[-1:]) == 0:
            self.game.selectedAttackedP1 = enemyCard
        else:
            self.game.selectedAttackedP1 = enemyCard
