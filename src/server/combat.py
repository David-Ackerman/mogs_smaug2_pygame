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
            self.game.player1['mana'] += 3
            self.game.player2['mana'] += 3

    def setPlayerCards(self, player, newCards):
        if player == 0:
            self.game.player1 = {
                'mana': self.game.player1['mana'],
                'life': self.game.player1['life'],
                'cards': {
                    'deck': newCards['deck'],
                    'hand': newCards['hand'],
                    'field': self.game.player1['cards']['field'],
                    'grave': self.game.player1['cards']['grave'],
                },
                'enemySelected': self.selectedAttackedP2
            }
        else:
            self.game.player2 = {
                'mana': self.game.player2['mana'],
                'life': self.game.player2['life'],
                'cards': {
                    'deck': newCards['deck'],
                    'hand': newCards['hand'],
                    'field': self.game.player2['cards']['field'],
                    'grave': self.game.player2['cards']['grave'],
                },
                'enemySelected': self.selectedAttackedP1
            }

    def setBattlePhase(self):
        self.game.turn = 3

    def changeTurn(self):
        if self.game.turn < 3:
            self.game.turn += 1
        else:
            self.changePlayerTime()

    def combat(self, player, attack: Deck, defense: Deck = None):
        if player == 0:
            playerDefending = 1
            attacker = self.game.player1
            defender = self.game.player2
        else:
            playerDefending = 0
            attacker = self.game.player2
            defender = self.game.player1

        attacker['mana'] -= 1
        if defense == None:
            defender['life'] -= attack['card_attack']
            if defender['life'] < 0:
                defender['life'] = 0
            return
        diference = attack['card_attack'] - defense['card_def']
        if diference > 0:
            defender['life'] -= diference
            if defender['life'] < 0:
                defender['life'] = 0
            self.destroyCard(playerDefending, defense)
        elif diference == 0:
            self.destroyCard(playerDefending, defense)
            self.destroyCard(player, attack)
        elif diference < 0:
            attacker['life'] += diference
            if attacker['life'] < 0:
                attacker['life'] = 0
            self.destroyCard(player, attack)

    def summonCard(self, player, card: Deck):
        cardPos = 'front' if card['card_type'] != 'spell' and card['card_type'] != 'trap' else 'support'
        if player == 0:
            self.game.player1['mana'] -= card['card_cust']
            self.game.player1['cards']['field'][cardPos].append(card)
            return
        else:
            self.game.player2['mana'] -= card['card_cust']
            self.game.player2['cards']['field'][cardPos].append(card)
            return

    def destroyCard(self, playerDestroyed, cardDestroyed: Deck, cardPos='front'):
        player = self.game.player1 if playerDestroyed == 0 else self.game.player2
        cardIndex = player['cards']['field'][cardPos].index(
            cardDestroyed)
        player['cards']['grave'].append(
            player['cards']['field'][cardPos].pop(cardIndex))

    def selectEnemyCard(self, player, enemyCard):
        if player == 0:
            self.game.selectedAttackedP1 = enemyCard
        else:
            self.game.selectedAttackedP1 = enemyCard
