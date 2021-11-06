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
pygame.font.init()

width = 1280
height = 880
surf = pygame.Surface((width, height))
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')

phase = {
    1: 'Draw Phase',
    2: 'Summon Phase',
    3: 'Battle Phase',
}

exitBtn = ButtonDuels("X", 10, 10, (250, 20, 20, 127), 45, 45, 8)


class Client():
    def __init__(self, game, conn):
        self.n = conn
        self.initialDeckSended = False
        self.handCardsPos = {'player': [
            410, height - 150], 'opponent': [width - 110, 10]}
        self.deckCardsPos = {'player': [
            width - 110, height - 340], 'opponent': [410, 200]}
        self.cards = {
            'deck': [],
            'hand': [],
            'grave': []
        }
        self.handCards: List[Card] = []
        self.deckCards: List[Card] = []
        self.graveCards: List[Card] = []
        self.opHandCards: List[Card] = []
        self.opDeckCards: List[Card] = []
        self.opGraceCards: List[Card] = []
        self.game = game
        self.BOARD_BG = pygame.image.load("assets/duelBoard.png")
        self.CARD_HAND = pygame.image.load("assets/cardHand.png")
        self.SIDE_DETAILS = pygame.image.load("assets/sideDetails.png")
        self.deckCardsSprite = pygame.sprite.Group()
        self.handCardsSprite = pygame.sprite.Group()
        self.opHandCardsSprite = pygame.sprite.Group()
        self.opDeckCardsSprite = pygame.sprite.Group()
        self.cardsInfo = CardsInfo()
        self.timer = 240

    def decreasingTimer(self):
        while True:
            if self.timer <= 0:
                outOfTime = {
                    'player': self.player,
                    'action': 'changePlayerTime',
                    'cards': self.cards
                }
                self.duel: Duel = self.n.send(outOfTime)
            if self.duel.isMyTurn(self.player):
                self.timer -= 1
            pygame.time.delay(1000)

    def showCardsInfo(self, cards: List[Card], isMyHand: bool = False, cardPos: int = -1):
        print('showCardDetails', cards, isMyHand, cardPos)
        self.cardsInfo.updateDraw(cards, cardPos)

    def initDuel(self, playerDeck: list[Deck]):
        self.playerDeck = playerDeck[:]
        self.opCards = {
            'hand': [],
            'deck': [],
            'grave': []
        }
        random.shuffle(self.playerDeck)
        for i in range(len(self.playerDeck)):
            idCard = 'p' + str(i)
            self.cards['deck'].append(self.playerDeck[i])
            self.deckCards.append(
                Card(self.playerDeck[i], True, False, id=idCard))
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

    def buildOpponent(self, cards):
        if cards == {}:
            return
        if len(cards['hand']) == 0 and len(cards['deck']) == 0 and len(cards['grave']) == 0:
            return
        if(cards['deck'] != self.opCards['deck']):
            self.opDeckCards = []
            for i in range(len(cards['deck'])):
                self.opDeckCards.append(Card(cards['deck'][i], True, False))
                self.opDeckCards[i].rect.x = self.deckCardsPos['opponent'][0]
                self.opDeckCards[i].rect.y = (
                    self.deckCardsPos['opponent'][1] - (2 * i))
            self.opDeckCardsSprite = pygame.sprite.Group(self.opDeckCards)
        if(cards['hand'] != self.opCards['hand']):
            self.opHandCards = []
            self.opHandCardsSprite.empty()
            for i in range(len(cards['hand'])):
                self.opHandCards.append(Card(cards['deck'][i], True, False))
                self.opHandCards[i].rect.x = self.handCardsPos['opponent'][0] - \
                    (i * 120)
                self.opHandCards[i].rect.y = self.handCardsPos['opponent'][1]
            self.opHandCardsSprite.add(self.opHandCards)
        self.opCards = cards

    def deckClick(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]
        y = self.deckCardsPos['player'][1]
        x = self.deckCardsPos['player'][0]
        if x <= x1 <= x + 100 and y <= y1 <= y + 140:
            return True
        else:
            return False

    def drawDeckCard(self, player):
        if not(self.duel.isMyTurn(player)) or self.duel.turn != 1:
            self.showCardsInfo([self.deckCards], True)
            return
        if len(self.handCards) <= 5:
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
        self.handCardsSprite.draw(win)
        self.deckCardsSprite.draw(win)

        exitBtn.draw(win)
        win.blit(
            opponentCountCardsText, (self.deckCardsPos['opponent'][0] + (100/2 - opponentCountCardsText.get_width()/2), self.deckCardsPos['opponent'][1] + 50))
        win.blit(
            countDeckCardsText, (self.deckCardsPos['player'][0] + (100/2 - countDeckCardsText.get_width()/2), self.deckCardsPos['player'][1] + 50))
        win.blit(timerText, (390 - timerText.get_width(), 10))
        pygame.display.update()

    def render_self(self):
        self.duel: Duel = self.n.send({'action': 'standby'})
        self.run_display = True
        self.initDuel()
        self.player = int(self.n.getP()['player'])
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

            if not(initedTimerThread) and self.duel.connected():
                initedTimerThread = True
                self.threadId = _thread.start_new_thread(
                    self.decreasingTimer, ())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not(self.duel.connected()):
                        break
                    if exitBtn.click(pos):
                        run = False
                        self.runDisplay = False
                        self.game.goToMenuScreen()
                        _thread.exit()
                    elif self.deckClick(pos):
                        self.drawDeckCard(self.player)
                    else:
                        i = 0
                        for card in self.handCards:
                            if card.click(pos):
                                self.showCardsInfo(self.handCards, True, i)
                                break
                            i += 1
            self.redrawWindow(win, self.player)
