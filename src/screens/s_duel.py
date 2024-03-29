import random
import _thread
from typing import List, Tuple
import pygame
from src.p_server.network import Network
from src.components.button import ButtonDuels
from src.components.card import Card
from src.components.cardsInfo import CardsInfo
from src.interfaces.card_model import Deck
from duel import Duel
from src.services.getFont import loadCustomFont
from src.services.saveDeck import loadDeckOnDisk
from src.screens.menu import EndDuel


phase = {
    1: 'Draw Phase',
    2: 'Summon Phase',
    3: 'Battle Phase',
}


class DuelGame():
    def __init__(self, game, conn: Network, player: int, userName: str, duel: Duel):
        self.n, self.player, self.duel, self.game = conn, player, duel, game
        self.sideBar = max(self.game.WIDTH * 0.30, 400)
        self.handCardsPos = {'player': [
            self.sideBar + 10, self.game.HEIGHT - 150], 'opponent': [self.game.WIDTH - 110, 10]}
        self.deckCardsPos = {'player': [
            self.game.WIDTH - 120, self.game.HEIGHT - 320], 'opponent': [self.sideBar + 10, 200]}
        self.graveCardPos = {'player': [
            self.game.WIDTH - 120, self.game.HEIGHT - 480], 'opponent': [self.sideBar + 10, 360]}
        self.fieldCardPos = {
            'playerFront': [self.sideBar + 200, self.game.HEIGHT - 500],
            'opFront': [self.game.WIDTH - 342, 334],
            'playerSupport': [self.sideBar + 200, self.game.HEIGHT - 340],
            'opSupport': [self.game.WIDTH - 342, 182],
        }
        BOARD_BG = pygame.image.load("assets/images/duelBoard.png")
        CARD_HAND = pygame.image.load("assets/images/cardHand.png")
        SIDE_DETAILS = pygame.image.load("assets/images/sideDetails.png")
        self.userId, self.username, self.opUsername = userName, '', ''
        self.BOARD_BG = pygame.transform.scale(
            BOARD_BG, (self.game.WIDTH - self.sideBar, self.game.HEIGHT - 320))
        self.CARD_HAND = pygame.transform.scale(
            CARD_HAND, (self.game.WIDTH - self.sideBar, 160))
        self.SIDE_DETAILS = pygame.transform.scale(
            SIDE_DETAILS, (self.sideBar, self.game.HEIGHT))
        self.exitBtn = ButtonDuels("X", 10, 10, (250, 20, 20, 127),
                                   'nunito-bold', 45, 45, 8)
        self.lost = False
        self.hasAttacked = []
        self.mana, self.opMana, self.lifePoints, self.opLifePoints = 14, 14, 200, 200
        self.attacking, self.forceEnemyBuild, self.enemySelect = False, False, None
        self.initialDeckSended, self.timer, self.myTurn = False, 240, self.duel.isMyTurn(
            self.userId)
        self.cards = {
            'deck': [],
            'hand': [],
        }
        self.fieldSimpleCards = {
            'field': {
                'front': [],
                'support': []
            },
            'grave': []
        }
        self.handCards, self.deckCards, self.graveCards, self.opHandCards, self.opDeckCards, self.opGraveCards = list[Card](
        ), list[Card](), list[Card](), list[Card](), list[Card](), list[Card]()
        self.fieldCards, self.opFieldCards = {
            'front': list[Card](),
            'support': list[Card]()
        }, {
            'front': list[Card](),
            'support': list[Card]()
        }
        self.deckCardsSprite, self.handCardsSprite, self.fieldCardsFrontSprite, self.fieldCardsSupportSprite, self.graveCardsSprite, self.opHandCardsSprite, self.opFieldFrontCardsSprite, self.opFieldSupportCardsSprite, self.opGraveCardsSprite, self.opDeckCardsSprite = pygame.sprite.Group(
        ), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

        self.cardsInfo = CardsInfo(self.sideBar, self.game.HEIGHT, self.game,
                                   self.summonCard, self.changeBattlePhase, self.endPlayerTime, self.setAttack, self.confirmAttack, self.hasAttacked)

    def decreasingTimer(self):
        while self.run_display:
            if self.timer <= 0:
                outOfTime = {
                    'player': self.userId,
                    'action': 'changePlayerTime',
                    'cards': self.cards
                }
                self.duel: Duel = self.n.send(outOfTime)
                self.timer = 240
                self.attackingCard = None
                self.attackedCard = None
                self.attacking = False
                self.showCardsInfo([], False, False)
            if self.myTurn:
                self.timer -= 1
            pygame.time.delay(1000)

    def gameComunicate(self):
        while self.run_display:
            if self.opLifePoints <= 0 or self.lifePoints <= 0 or self.lost:
                self.run_display = False
                self.n.send({'action': 'quit'})
                break
            try:
                getAction = {
                    'player': self.userId,
                    'action': 'get',
                    'cards': self.cards
                }
                self.duel: Duel = self.n.send(getAction)
                lifesMana = self.duel.getLifeMana(self.userId)
                self.mana, self.lifePoints, self.username = lifesMana[0]
                self.opMana, self.opLifePoints, self.opUsername = lifesMana[1]
            except Exception as e:
                self.run_display = False
                print("Couldn't get game", e)
                break
            pygame.time.delay(300)

    def endGame(self):
        self.run_display = False

        if self.opLifePoints <= 0 or self.lifePoints <= 0 or self.lost:
            self.game.finishGame_screen = EndDuel(
                self.game, self.opLifePoints <= 0 and not(self.lost))
            self.game.curr_screen = self.game.finishGame_screen
            self.game.curr_screen.render_self()
        else:
            self.game.goToMenuScreen()

    def showCardsInfo(self, cards: List[Card], isField: bool = False, isMyHand: bool = False, cardPos: int = -1, isEnemy=False):
        if cardPos == - 1:
            cardPos = len(cards) - 1
        self.cardsInfo.updateDraw(
            cards, cardPos, self.myTurn, self.duel.turn,  isField, isMyHand, self.duel.round, self.attacking, isEnemy)

    def initDuel(self, playerDeck: list[Deck]):
        self.playerDeck = playerDeck[:]
        self.opCards = {
            'hand': [],
            'field': {
                'front': [],
                'support': []
            },
            'deck': [],
            'grave': []
        }
        random.shuffle(self.playerDeck)
        cardP = 'playerPri' if self.player == 0 else 'playerSec'
        for i in range(len(self.playerDeck)):
            self.playerDeck[i]['onGameId'] = cardP+str(i)
            self.cards['deck'].append(self.playerDeck[i])
            self.deckCards.append(
                Card(self.playerDeck[i], True, False))
            self.deckCards[i].rect.x = self.deckCardsPos['player'][0]
            self.deckCards[i].rect.y = (
                self.deckCardsPos['player'][1] - (2 * i))
        for i in range(4):
            self.cards['hand'].append(self.cards['deck'].pop())
            self.handCards.append(self.deckCards.pop())
            self.handCards[i].isBack = False
            self.handCards[i].build_card()
            self.handCards[i].rect.x = self.handCardsPos['player'][0] + \
                (i * 120)
            self.handCards[i].rect.y = self.handCardsPos['player'][1]

        self.handCardsSprite.add(self.handCards)
        self.deckCardsSprite.add(self.deckCards)

    def buildOpponent(self, opponent):
        if opponent == {}:
            return
        try:
            cards = opponent['cards']
        except:
            return
        if len(cards['hand']) == 0 and len(cards['deck']) == 0 and len(cards['grave']) == 0:
            return
        if(cards['deck'] != self.opCards['deck']):
            self.opDeckCards = []
            for i in range(len(cards['deck'])):
                self.opDeckCards.append(
                    Card(cards['deck'][i], True, False, flip=True))
                self.opDeckCards[i].rect.x = self.deckCardsPos['opponent'][0]
                self.opDeckCards[i].rect.y = (
                    self.deckCardsPos['opponent'][1] - (2 * i))
            self.opDeckCardsSprite = pygame.sprite.Group(self.opDeckCards)
        if(cards['hand'] != self.opCards['hand']):
            self.opHandCards = []
            self.opHandCardsSprite.empty()
            for i in range(len(cards['hand'])):
                self.opHandCards.append(
                    Card(cards['hand'][i], True, False))
                self.opHandCards[i].rect.x = self.handCardsPos['opponent'][0] - \
                    (i * 120)
                self.opHandCards[i].rect.y = self.handCardsPos['opponent'][1]
            self.opHandCardsSprite.add(self.opHandCards)
        fieldCondition = cards['field']['front'] != self.opCards['field']['front']
        supportCondition = cards['field']['support'] != self.opCards['field']['support']
        graveCondition = cards['grave'] != self.opCards['grave']
        if(fieldCondition or self.forceEnemyBuild):
            self.opFieldFrontCardsSprite.empty()
            self.opFieldCards['front'] = []
            for i in range(len(cards['field']['front'])):
                self.opFieldCards['front'].append(
                    Card(cards['field']['front'][i], False, False, self.enemySelect == cards['field']['front'][i]['onGameId'], (200, 40, 20, 255), flip=True))
                self.opFieldCards['front'][i].rect.x = self.fieldCardPos['opFront'][0] - \
                    (i * 135)
                self.opFieldCards['front'][i].rect.y = self.fieldCardPos['opFront'][1]
            self.opFieldFrontCardsSprite.add(self.opFieldCards['front'])
            self.forceEnemyBuild = False
        if(supportCondition):
            self.opFieldCards['support'] = []
            self.opFieldSupportCardsSprite.empty()
            for i in range(len(cards['field']['support'])):
                self.opFieldCards['support'].append(
                    Card(cards['field']['support'][i], True, False, flip=True))
                self.opFieldCards['support'][i].rect.x = self.fieldCardPos['opSupport'][0] - \
                    (i * 135)
                self.opFieldCards['support'][i].rect.y = self.fieldCardPos['opSupport'][1]
            self.opFieldSupportCardsSprite.add(self.opFieldCards['support'])
        if graveCondition:
            self.opGraveCards = []
            self.opGraveCardsSprite.empty()
            for i in range(len(cards['grave'])):
                self.opGraveCards.append(
                    Card(cards['grave'][i], False, False, flip=True))
                self.opGraveCards[i].rect.x = self.graveCardPos['opponent'][0]
                self.opGraveCards[i].rect.y = self.graveCardPos['opponent'][1] - \
                    (i * 2)
            self.opGraveCardsSprite.add(self.opGraveCards)
        self.opCards = cards

    def buildField(self):
        myself = self.duel.getMyFieldCards(self.userId)
        if myself == {}:
            return
        try:
            self.mana, self.life = myself['mana'], myself['life']
            cards: List[Deck] = myself['cards']
        except:
            return
        fieldCondition = cards['field']['front'] != self.fieldSimpleCards['field']['front']
        supportCondition = cards['field']['support'] != self.fieldSimpleCards['field']['support']
        graveCondition = cards['grave'] != self.fieldSimpleCards['grave']
        if(fieldCondition):
            self.fieldCards['front'] = []
            self.fieldCardsFrontSprite.empty()
            for i in range(len(cards['field']['front'])):
                self.fieldCards['front'].append(
                    Card(cards['field']['front'][i], False, False))
                self.fieldCards['front'][i].rect.x = self.fieldCardPos['playerFront'][0] + \
                    (i * 135)
                self.fieldCards['front'][i].rect.y = self.fieldCardPos['playerFront'][1]
            self.fieldCardsFrontSprite.add(self.fieldCards['front'])
        if(supportCondition):
            self.fieldCards['support'] = []
            self.fieldCardsSupportSprite.empty()
            for i in range(len(cards['field']['support'])):
                self.fieldCards['support'].append(
                    Card(cards['field']['support'][i], True, False))
                self.fieldCards['support'][i].rect.x = self.fieldCardPos['playerSupport'][0] + \
                    (i * 135)
                self.fieldCards['support'][i].rect.y = self.fieldCardPos['playerSupport'][1]
            self.fieldCardsSupportSprite.add(self.fieldCards['support'])
        if graveCondition:
            self.graveCards = []
            self.graveCardsSprite.empty()
            for i in range(len(cards['grave'])):
                self.graveCards.append(
                    Card(cards['grave'][i], False, False))
                self.graveCards[i].rect.x = self.graveCardPos['player'][0]
                self.graveCards[i].rect.y = self.graveCardPos['player'][1] + \
                    (i * 2)
            self.graveCardsSprite.add(self.graveCards)

        self.fieldSimpleCards = {
            'field': cards['field'],
            'grave': cards['grave']
        }

    def deckClick(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]
        y = self.deckCardsPos['player'][1]
        x = self.deckCardsPos['player'][0]
        if x <= x1 <= x + 100 and y <= y1 <= y + 140:
            return True
        else:
            return False

    def graveClick(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]
        y = self.graveCardPos['player'][1]
        x = self.graveCardPos['player'][0]
        if x <= x1 <= x + 100 and y <= y1 <= y + 140:
            return True
        else:
            return False

    def drawDeckCard(self, player):
        if not(self.myTurn) or self.duel.turn != 1:
            return
        if len(self.deckCards) == 0:
            self.lost = True
            return

        if len(self.handCards) <= 5:
            self.game.sound.playSound('click')
            self.cards['hand'].append(self.cards['deck'].pop())
            self.handCards.append(self.deckCards.pop())
            self.handCards[-1].isBack = False
            self.handCards[-1].build_card()
            self.handCards[-1].rect.x = self.handCardsPos['player'][0] + \
                ((len(self.handCards) - 1) * 120)
            self.handCards[-1].rect.y = self.handCardsPos['player'][1]
        drawCard = {
            'player': player,
            'action': 'drawCard',
            'cards': self.cards
        }
        self.duel: Duel = self.n.send(drawCard)
        self.showCardsInfo([], False, False)

    def updateHandPos(self):
        self.handCardsSprite.empty()
        for i in range(len(self.handCards)):
            self.handCards[i].rect.x = self.handCardsPos['player'][0] + \
                (i * 120)
            self.handCards[i].rect.y = self.handCardsPos['player'][1]
        self.handCardsSprite.add(self.handCards)

    def summonCard(self, cardPos: int):
        posString = 'player'
        if self.handCards[cardPos].card['card_type'] == 'spell' or self.handCards[cardPos].card['card_type'] == 'trap':
            fieldType = 'support'
        else:
            fieldType = 'front'
        if fieldType == 'fron' and len(self.fieldCards[fieldType]) > 2 or self.cards['hand'][cardPos]['card_cust'] > self.mana:
            return
        posString += fieldType.capitalize()
        summonedCard = self.cards['hand'].pop(cardPos)
        self.handCards.pop(cardPos).kill()

        summonCard = {
            'player': self.userId,
            'action': 'summon',
            'summoned': summonedCard,
            'cards': self.cards
        }
        self.duel: Duel = self.n.send(summonCard)
        self.updateHandPos()
        if cardPos + 1 > len(self.handCards):
            cardPos = -1
        self.showCardsInfo(self.handCards, False, True, cardPos)

    def setAttack(self, card: Card):
        if self.mana < 1:
            return
        self.attackingCard = card
        self.attacking = True
        if len(self.opCards['field']['front']) == 0:
            for card in self.fieldSimpleCards['field']['front']:
                if card['onGameId'] == self.attackingCard.cardOnDuelId:
                    attackCard = card
            combatAction = {
                'player': self.userId,
                'action': 'directAttack',
                'cards': self.cards,
                'attacking': attackCard,
            }
            self.duel: Duel = self.n.send(combatAction)
            self.attackingCard = None
            self.attackedCard = None
            self.attacking = False
            self.hasAttacked.append(attackCard)
            self.showCardsInfo([], False, False)
            return
        if len(self.opFieldCards['front']) == 1:
            self.confirmAttack(self.opFieldCards['front'][0])
            return

    def selectEnemyCard(self, card: Card):
        changeTurn = {
            'player': self.userId,
            'action': 'selectEnemyCard',
            'cards': self.cards,
            'selectedCard': card.cardOnDuelId
        }
        self.enemySelect = card.cardOnDuelId
        self.duel: Duel = self.n.send(changeTurn)
        self.forceEnemyBuild = True
        self.showCardsInfo([card], False, False, isEnemy=True)

    def confirmAttack(self, attackedCard: Deck):
        for card in self.fieldSimpleCards['field']['front']:
            if card['onGameId'] == self.attackingCard.cardOnDuelId:
                attackCard = card
        for card in self.opCards['field']['front']:
            if card['onGameId'] == attackedCard.cardOnDuelId:
                defenseCard = card
        combatAction = {
            'player': self.userId,
            'action': 'combat',
            'cards': self.cards,
            'attacking': attackCard,
            'defending': defenseCard
        }
        self.duel: Duel = self.n.send(combatAction)
        self.attackingCard = None
        self.attackedCard = None
        self.attacking = False
        self.hasAttacked.append(attackCard)
        self.showCardsInfo([], False, False)

    def endPlayerTime(self):
        changeTurn = {
            'player': self.userId,
            'action': 'changePlayerTime',
            'cards': self.cards
        }
        self.duel: Duel = self.n.send(changeTurn)
        self.showCardsInfo([], False, False)
        self.attackingCard = None
        self.attackedCard = None
        self.hasAttacked = []
        self.cardsInfo.hasAttacked = self.hasAttacked
        self.attacking = False
        self.timer = 240

    def changeBattlePhase(self):
        battlePhase = {
            'player': self.userId,
            'action': 'battlePhase',
            'cards': self.cards
        }
        self.duel: Duel = self.n.send(battlePhase)
        self.showCardsInfo([], False, False)

    def redrawWindow(self, win: pygame.Surface, player):
        win.fill((128, 128, 128))
        try:
            self.duel.connected()
        except:
            return
        self.buildOpponent(self.duel.getOpponentCards(player))
        self.buildField()
        smallFont = loadCustomFont(24)
        highFont = loadCustomFont(30)

        userText = smallFont.render(self.username, True, (50, 50, 50))
        lifeText = smallFont.render(
            "LP: " + str(self.lifePoints), True, (240, 40, 40))
        manaText = smallFont.render(
            "Mana: " + str(self.mana), True, (230, 100, 230))
        opUserText = smallFont.render(self.opUsername, True, (50, 50, 50))
        opLifeText = smallFont.render(
            "LP: " + str(self.opLifePoints), True, (240, 40, 40))
        opManaText = smallFont.render(
            "Mana: " + str(self.opMana), True, (230, 100, 230))
        countDeckCardsText = highFont.render(
            str(len(self.deckCards)), True, (230, 230, 230))
        opponentCountCardsText = highFont.render(
            str(len(self.opCards['deck'])), True, (230, 230, 230))
        win.blit(
            self.CARD_HAND, (self.sideBar, 0))
        win.blit(self.BOARD_BG, (self.sideBar, 160))
        win.blit(
            self.CARD_HAND, (self.sideBar, self.game.HEIGHT - 160))
        win.blit(self.SIDE_DETAILS, (0, 0))
        self.cardsInfo.draw(win, self.myTurn)
        self.opDeckCardsSprite.draw(win)
        self.opHandCardsSprite.draw(win)
        self.opFieldFrontCardsSprite.draw(win)
        self.opFieldSupportCardsSprite.draw(win)
        self.opGraveCardsSprite.draw(win)
        self.fieldCardsFrontSprite.draw(win)
        self.fieldCardsSupportSprite.draw(win)
        self.handCardsSprite.draw(win)
        self.deckCardsSprite.draw(win)
        self.graveCardsSprite.draw(win)
        self.exitBtn.draw(win)
        win.blit(
            opponentCountCardsText, (self.deckCardsPos['opponent'][0] + (100/2 - opponentCountCardsText.get_width()/2), self.deckCardsPos['opponent'][1] + 50))
        win.blit(
            countDeckCardsText, (self.deckCardsPos['player'][0] + (100/2 - countDeckCardsText.get_width()/2), self.deckCardsPos['player'][1] + 50))
        win.blit(userText, (self.game.WIDTH - 120, self.game.HEIGHT - 150))
        win.blit(lifeText, (self.game.WIDTH - 120, self.game.HEIGHT - 120))
        win.blit(manaText, (self.game.WIDTH - 120, self.game.HEIGHT - 90))
        win.blit(opUserText, (self.sideBar, 10))
        win.blit(opLifeText, (self.sideBar, 40))
        win.blit(opManaText, (self.sideBar, 70))
        if self.myTurn:
            timerText = highFont.render(
                "Tempo: " + str(self.timer), True, (230, 230, 230))
            win.blit(timerText, (390 - timerText.get_width(), 10))

        pygame.display.update()

    def render_self(self):
        self.run_display = True

        deck = loadDeckOnDisk()["deck"]
        self.initDuel(deck)
        clock = pygame.time.Clock()
        initedTimerThread = False
        self.showCardsInfo([])
        while self.run_display:
            try:
                self.duel.connected()
            except:
                break
            clock.tick(30)
            if self.duel:
                self.myTurn = self.duel.isMyTurn(self.userId)
            if not(initedTimerThread) and self.duel.connected():
                initedTimerThread = True

                _thread.start_new_thread(
                    self.decreasingTimer, ())
                _thread.start_new_thread(self.gameComunicate, ())

            self.check_events()
            self.redrawWindow(self.game.window, self.userId)
        self.endGame()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.finish()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                self.cardsInfo.checkClicks(pos)
                if self.exitBtn.click(pos):
                    self.game.sound.playSound('endGame')

                    self.run_display = False
                    self.n.send({'action': 'quit'})
                    break
                elif self.attacking:
                    self.attackingCard.selectCard()
                    for card in self.opFieldCards['front']:
                        if card.click(pos):
                            self.game.sound.playSound('endGame')

                            self.selectEnemyCard(card)
                            break
                elif self.deckClick(pos):
                    self.drawDeckCard(self.userId)
                else:
                    i, j, h = 0, 0, 0
                    for card in self.handCards:
                        if card.click(pos):
                            self.game.sound.playSound('viewCardInfo')

                            self.showCardsInfo(
                                self.handCards, isMyHand=True, cardPos=i)
                            break
                        i += 1
                    for card in self.fieldCards['front']:
                        if card.click(pos):
                            self.game.sound.playSound('viewCardInfo')

                            self.showCardsInfo(
                                self.fieldCards['front'], isField=True, cardPos=j)
                            break
                        j += 1
                    for card in self.fieldCards['support']:
                        if card.click(pos):
                            self.game.sound.playSound('viewCardInfo')
                            self.showCardsInfo(
                                self.fieldCards['support'], isField=True, cardPos=h)
                            break
                        h += 1
