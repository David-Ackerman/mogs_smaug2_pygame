import random
from typing import List, Tuple
import pygame
from duel import Duel
from interfaces.card_model import Deck
from components.card import Card
from network import Network
from services.saveDeck import loadDeckOnDisk
pygame.font.init()

width = 1280
height = 880
surf = pygame.Surface((width, height))
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')


class Button:
    def __init__(self, text: str, x: int, y: int,  color: tuple[int, int, int], width: int = 160, height: int = 100):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 35)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                 self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


exitBtn = Button("X", 10, 10, (250, 20, 20), 50, 50)


class Client():
    def __init__(self, game):
        self.step = 0
        self.initialDeckSended = False
        self.handCardsPos = {'player': [
            410, height - 150], 'opponent': [width - 110, 10]}
        self.deckCardsPos = {'player': [
            width - 110, height - 340], 'opponent': [410, 180]}
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

    def initDuel(self, playerDeck: list[Deck]):
        self.step = 1
        self.playerDeck = playerDeck[:]
        self.opCards = {
            'hand': [],
            'deck': [],
            'grave': []
        }
        random.shuffle(self.playerDeck)
        for i in range(len(self.playerDeck)):
            self.cards['deck'].append(self.playerDeck[i])
            self.deckCards.append(Card(self.playerDeck[i], True, False))
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
            self.opDeckCardsSprite.empty()
            for i in range(len(cards['deck'])):
                self.opDeckCards.append(Card(cards['deck'][i], True, False))
                self.opDeckCards[i].rect.x = self.deckCardsPos['opponent'][0]
                self.opDeckCards[i].rect.y = (
                    self.deckCardsPos['opponent'][1] + (2 * i))
            self.opDeckCardsSprite.add(self.opDeckCards)
        if(cards['hand'] != self.opCards['hand']):
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
        if self.step == 1 and len(self.handCards) <= 5:
            self.cards['hand'].append(self.cards['deck'].pop())
            self.handCards.append(self.deckCards.pop())
            self.handCards[-1].isBack = False
            self.handCards[-1].build_card()
            self.handCards[-1].rect.x = self.handCardsPos['player'][0] + \
                ((len(self.handCards) - 1) * 120)
            self.handCards[-1].rect.y = self.handCardsPos['player'][1]
        getAction = {
            'player': player,
            'action': 'get',
            'cards': self.cards
        }
        self.duel: Duel = self.n.send(getAction)

    def redrawWindow(self, win: pygame.Surface, duel: Duel, player):
        win.fill((128, 128, 128))

        if not(duel.connected()):
            font = pygame.font.SysFont("comicsans", 70)
            text = font.render("Waiting for Player...", True, (255, 0, 0))
            win.blit(text, (width/2 - text.get_width() /
                            2, height/2 - text.get_height()/2))
        else:
            self.buildOpponent(duel.getOpponentCards(player))
            font = pygame.font.SysFont("sansserif", 40)
            countDeckCardsText = font.render(
                str(len(self.deckCards)), True, (230, 230, 230))
            opponentCountCardsText = font.render(
                str(len(self.opCards['deck'])), True, (230, 230, 230))
            win.blit(
                self.CARD_HAND, (400, 0))
            win.blit(self.BOARD_BG, (400, 160))
            win.blit(
                self.CARD_HAND, (400, height - 160))
            self.opHandCardsSprite.update()
            self.opHandCardsSprite.draw(self.game.window)
            self.opDeckCardsSprite.update()
            self.opDeckCardsSprite.draw(self.game.window)
            self.handCardsSprite.update()
            self.handCardsSprite.draw(self.game.window)
            self.deckCardsSprite.update()
            self.deckCardsSprite.draw(self.game.window)
            win.blit(self.SIDE_DETAILS, (0, 0))
            exitBtn.draw(win)
            win.blit(
                opponentCountCardsText, (self.deckCardsPos['opponent'][0] + (100/2 - opponentCountCardsText.get_width()/2), self.deckCardsPos['opponent'][1] + 50))
            win.blit(
                countDeckCardsText, (self.deckCardsPos['player'][0] + (100/2 - countDeckCardsText.get_width()/2), self.deckCardsPos['player'][1] + 50))
        pygame.display.update()

    def main(self):
        run = True
        clock = pygame.time.Clock()
        self.n = Network()
        player = int(self.n.getP()['player'])

        while run:
            clock.tick(30)
            try:
                if self.initialDeckSended:
                    self.duel: Duel = self.n.send({'action': 'standby'})
                else:
                    getAction = {
                        'player': player,
                        'action': 'get',
                        'cards': self.cards
                    }
                    self.duel: Duel = self.n.send(getAction)
                    self.initialDeckSended = True
            except Exception as e:
                run = False
                print("Couldn't get game", e)
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for card in self.handCards:
                        if card.click(pos) and self.duel.connected():
                            print('clicado no card: ', card)
                            break
                        elif self.deckClick(pos) and self.duel.connected():
                            self.drawDeckCard(player)
                            break
            self.redrawWindow(win, self.duel, player)

    def render_self(self):
        self.game.DISPLAY_H = 850
        self.game.window = win
        self.game.display = surf
        run = True
        clock = pygame.time.Clock()
        deck = loadDeckOnDisk()["deck"]
        while run:
            clock.tick(30)
            win.fill((128, 128, 128))
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Click to search a duel!", 1, (255, 40, 67))
            win.blit(text, (width/2 - text.get_width() /
                            2, height/2 - text.get_height()/2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False
        self.initDuel(deck)
        self.main()
