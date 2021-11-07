import random
import _thread
from typing import List, Tuple
import pygame
from components.button import ButtonDuels
from components.cardsInfo import CardsInfo
from duel import Duel
from interfaces.card_model import Deck
from components.card import Card
from network import Network
from services.getFont import loadCustomFont
from services.saveDeck import loadDeckOnDisk

width = 1280
height = 880
handCardsPos = {'player': [
    410, height - 150], 'opponent': [width - 110, 10]}
deckCardsPos = {'player': [
    width - 110, height - 340], 'opponent': [410, 200]}
fieldCardPos = {
    'playerFront': [600, 450],
    'opFront': [width - 342, 304],
    'playerSupport': [600, 584],
    'opSupport': [width - 342, 172],
}

BOARD_BG = pygame.image.load("assets/duelBoard.png")
CARD_HAND = pygame.image.load("assets/cardHand.png")
SIDE_DETAILS = pygame.image.load("assets/sideDetails.png")

phase = {
    1: 'Draw Phase',
    2: 'Summon Phase',
    3: 'Battle Phase',
}


exitBtn = ButtonDuels("X", 10, 10, (250, 20, 20, 127), 45, 45, 8)


class DuelGame():
    def __init__(self, game, conn: Network, player: int, duel: Duel):
        self.n, self.player, self.duel, self.game = conn, player, duel, game
        self.initialDeckSended, self.finishThread, self.timer, self.myTurn = False, False, 240, self.duel.isMyTurn(
            self.player)
        self.cards = {
            'deck': [],
            'hand': [],
            'field': {
                'front': [],
                'support': []
            },
            'grave': []
        }
        self.handCards, self.deckCards, self.graveCards, self.opHandCards, self.opDeckCards, self.opGraceCards = list[Card](
        ), list[Card](), list[Card](), list[Card](), list[Card](), list[Card]()
        self.fieldCards, self.opFieldCards = {
            'front': list[Card](),
            'support': list[Card]()
        }, {
            'front': list[Card](),
            'support': list[Card]()
        }
        self.BOARD_BG, self.CARD_HAND, self.SIDE_DETAILS = BOARD_BG, CARD_HAND, SIDE_DETAILS
        self.deckCardsSprite, self.handCardsSprite, self.fieldCardsSprite, self.graveCardsSprite, self.opHandCardsSprite, self.opFieldCardsSprite, self.opGraveCardsSprite, self.opDeckCardsSprite = pygame.sprite.Group(
        ), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()

        self.cardsInfo = CardsInfo(self.summonCard)

    def decreasingTimer(self):
        while True:
            if self.finishThread:
                break
            if self.timer <= 0:
                outOfTime = {
                    'player': self.player,
                    'action': 'changePlayerTime',
                    'cards': self.cards
                }
                self.duel: Duel = self.n.send(outOfTime)
                self.timer = 240
            if self.myTurn:
                self.timer -= 1
            pygame.time.delay(1000)

    def showCardsInfo(self, cards: List[Card], isField: bool = False, isMyHand: bool = False, cardPos: int = -1):
        if cardPos == - 1:
            cardPos = len(cards) - 1
        self.cardsInfo.updateDraw(
            cards, cardPos, self.myTurn, self.duel.turn,  isField, isMyHand)

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
        for i in range(len(self.playerDeck)):
            idCard = 'p' + str(i)
            self.cards['deck'].append(self.playerDeck[i])
            self.deckCards.append(
                Card(self.playerDeck[i], True, False, id=idCard))
            self.deckCards[i].rect.x = deckCardsPos['player'][0]
            self.deckCards[i].rect.y = (
                deckCardsPos['player'][1] - (2 * i))
        for i in range(4):
            self.cards['hand'].append(self.cards['deck'].pop())
            self.handCards.append(self.deckCards.pop())
            self.handCards[i].isBack = False
            self.handCards[i].build_card()
            self.handCards[i].rect.x = handCardsPos['player'][0] + \
                (i * 120)
            self.handCards[i].rect.y = handCardsPos['player'][1]

        self.handCardsSprite.add(self.handCards)
        self.deckCardsSprite.add(self.deckCards)

    def buildOpponent(self, cards):
        if cards == {}:
            return
        if len(cards['hand']) == 0 and len(cards['deck']) == 0 and len(cards['grave']) == 0:
            return
        if(cards['deck'] != self.opCards['deck']):
            self.opDeckCards = []
            for i in range(len(cards['deck'])):
                self.opDeckCards.append(
                    Card(cards['deck'][i], True, False, flip=True))
                self.opDeckCards[i].rect.x = deckCardsPos['opponent'][0]
                self.opDeckCards[i].rect.y = (
                    deckCardsPos['opponent'][1] - (2 * i))
            self.opDeckCardsSprite = pygame.sprite.Group(self.opDeckCards)
        if(cards['hand'] != self.opCards['hand']):
            self.opHandCards = []
            self.opHandCardsSprite.empty()
            for i in range(len(cards['hand'])):
                self.opHandCards.append(
                    Card(cards['hand'][i], True, False, flip=True))
                self.opHandCards[i].rect.x = handCardsPos['opponent'][0] - \
                    (i * 120)
                self.opHandCards[i].rect.y = handCardsPos['opponent'][1]
            self.opHandCardsSprite.add(self.opHandCards)
        if(cards['field']['front'] != self.opCards['field']['front']):
            self.opFieldCards['front'] = []
            self.opFieldCardsSprite.empty()
            for i in range(len(cards['field']['front'])):
                self.opFieldCards['front'].append(
                    Card(cards['field']['front'][i], False, False, flip=True))
                self.opFieldCards['front'][i].rect.x = fieldCardPos['opFront'][0] - \
                    (i * 135)
                self.opFieldCards['front'][i].rect.y = fieldCardPos['opFront'][1]
            self.opFieldCardsSprite.add(self.opFieldCards['front'])
        if(cards['field']['support'] != self.opCards['field']['support']):
            self.opFieldCards['support'] = []
            self.opFieldCardsSprite.empty()
            for i in range(len(cards['field']['support'])):
                self.opFieldCards['support'].append(
                    Card(cards['field']['support'][i], True, False, flip=True))
                self.opFieldCards['support'][i].rect.x = fieldCardPos['opSupport'][0] - \
                    (i * 135)
                self.opFieldCards['support'][i].rect.y = fieldCardPos['opSupport'][1]
            self.opFieldCardsSprite.add(self.opFieldCards['support'])
        self.opCards = cards

    def deckClick(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]
        y = deckCardsPos['player'][1]
        x = deckCardsPos['player'][0]
        if x <= x1 <= x + 100 and y <= y1 <= y + 140:
            return True
        else:
            return False

    def drawDeckCard(self, player):
        if not(self.myTurn) or self.duel.turn != 1:
            return
        if len(self.handCards) <= 5:
            self.cards['hand'].append(self.cards['deck'].pop())
            self.handCards.append(self.deckCards.pop())
            self.handCards[-1].isBack = False
            self.handCards[-1].build_card()
            self.handCards[-1].rect.x = handCardsPos['player'][0] + \
                ((len(self.handCards) - 1) * 120)
            self.handCards[-1].rect.y = handCardsPos['player'][1]
        drawCard = {
            'player': player,
            'action': 'drawCard',
            'cards': self.cards
        }
        self.duel: Duel = self.n.send(drawCard)

    def updateHandPos(self):
        for i in range(len(self.handCards)):
            self.handCards[i].rect.x = handCardsPos['player'][0] + (i * 120)
            self.handCards[i].rect.y = handCardsPos['player'][1]

    def summonCard(self, cardPos: int):
        posString = 'player'
        if self.handCards[cardPos].card['card_type'] == 'magic':
            fieldType = 'support'
        else:
            fieldType = 'front'
        if len(self.fieldCards[fieldType]) > 2:
            return
        posString += fieldType.capitalize()
        self.cards['field'][fieldType].append(self.cards['hand'].pop(cardPos))
        self.fieldCards[fieldType].append(self.handCards.pop(cardPos))
        self.fieldCards[fieldType][-1].rect.x = fieldCardPos[posString][0] + \
            ((len(self.fieldCards[fieldType]) - 1) * 135)
        self.fieldCards[fieldType][-1].rect.y = fieldCardPos[posString][1]
        summonCard = {
            'player': self.player,
            'action': 'get',
            'cards': self.cards
        }
        self.duel: Duel = self.n.send(summonCard)
        self.updateHandPos()
        if cardPos + 1 > len(self.handCards):
            cardPos = -1
        self.showCardsInfo(self.handCards, False, True, cardPos)
        self.fieldCardsSprite.add(self.fieldCards[fieldType])

    def redrawWindow(self, win: pygame.Surface, player):
        win.fill((128, 128, 128))

        self.buildOpponent(self.duel.getOpponentCards(player))
        font = loadCustomFont(30)
        timerText = font.render(
            "Tempo: " + str(self.timer), True, (230, 230, 230))
        countDeckCardsText = font.render(
            str(len(self.deckCards)), True, (230, 230, 230))
        opponentCountCardsText = font.render(
            str(len(self.opCards['deck'])), True, (230, 230, 230))
        win.blit(
            self.CARD_HAND, (400, 0))
        win.blit(self.BOARD_BG, (400, 160))
        win.blit(
            self.CARD_HAND, (400, height - 160))
        win.blit(self.SIDE_DETAILS, (0, 0))
        self.cardsInfo.draw(win)
        self.opDeckCardsSprite.draw(win)
        self.opHandCardsSprite.draw(win)
        self.opFieldCardsSprite.draw(win)
        self.fieldCardsSprite.draw(win)
        self.handCardsSprite.draw(win)
        self.deckCardsSprite.draw(win)

        exitBtn.draw(win)
        win.blit(
            opponentCountCardsText, (deckCardsPos['opponent'][0] + (100/2 - opponentCountCardsText.get_width()/2), deckCardsPos['opponent'][1] + 50))
        win.blit(
            countDeckCardsText, (deckCardsPos['player'][0] + (100/2 - countDeckCardsText.get_width()/2), deckCardsPos['player'][1] + 50))
        if self.myTurn:
            win.blit(timerText, (390 - timerText.get_width(), 10))
        pygame.display.update()

    def render_self(self):
        self.run_display = True
        deck = loadDeckOnDisk()["deck"]
        self.initDuel(deck)
        clock = pygame.time.Clock()
        initedTimerThread = False
        while self.duel.connected() and self.run_display:
            clock.tick(30)
            try:
                if self.initialDeckSended:
                    self.duel: Duel = self.n.send({'action': 'standby'})
                else:
                    getAction = {
                        'player': self.player,
                        'action': 'get',
                        'cards': self.cards
                    }
                    self.duel: Duel = self.n.send(getAction)
                    self.initialDeckSended = True
            except Exception as e:
                self.run_display = False
                print("Couldn't get game", e)
                break
            self.myTurn = self.duel.isMyTurn(self.player)
            if not(initedTimerThread) and self.duel.connected():
                initedTimerThread = True
                self.threadId = _thread.start_new_thread(
                    self.decreasingTimer, ())
            self.check_events()
            self.redrawWindow(self.game.window, self.player)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                self.cardsInfo.checkClicks(pos)
                if exitBtn.click(pos):
                    self.run_display = False
                    self.finishThread = True
                    self.n.send({'action': 'quit'})
                    self.game.goToMenuScreen()
                    break
                elif self.deckClick(pos):
                    self.drawDeckCard(self.player)
                else:
                    i = 0
                    for card in self.handCards:
                        if card.click(pos):
                            self.showCardsInfo(
                                self.handCards, isMyHand=True, cardPos=i)
                            break
                        i += 1
