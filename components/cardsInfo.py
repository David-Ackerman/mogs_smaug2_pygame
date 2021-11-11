
from typing import Dict, List, Tuple

import pygame
from components.button import ButtonDuels
from components.card import Card
from services.getFont import loadCustomFont
from services.renders import blit_complex_text

width = 1280
height = 880

cardsInfoBtns = {
    'summon': ButtonDuels('Invocar', 20, height - 80, (159, 187, 193), 100, 30, 14, 20),
    'attack': ButtonDuels('Atacar', 154, height - 80, (159, 187, 193), 100, 30, 14, 20),
    'effect': ButtonDuels('Ativar', 280, height - 80, (159, 187, 193), 100, 30, 14, 20),
    'phaseAttack': ButtonDuels('fase de ataque', 20, height - 40, (159, 187, 193), 100, 30, 14, 20),
    'endTurn': ButtonDuels('encerrar turno', 280, height - 40, (159, 187, 193), 100, 30, 14, 20),
    'goLeft': ButtonDuels('<', 20, 430, (159, 187, 193), 30, 20, 10, 25),
    'goRight': ButtonDuels('>', 350, 430, (159, 187, 193), 30, 20, 10, 25),
}


class CardsInfo:
    def __init__(self, summon, battlePhase, endPhase):
        self.cards = []
        self.pos = -1
        self.turn = 1
        self.isField = False
        self.isHand = False
        self.isMyTurn = True
        self.summonCard = summon
        self.battlePhase = battlePhase
        self.endPhase = endPhase

    def changeCard(self, action: str):
        if action == 'left' and self.pos > 0:
            self.pos -= 1
        elif action == 'right' and self.pos + 1 < len(self.cards):
            self.pos += 1

    def updateDraw(self, cards: List[Card], init: int, isMyTurn: bool, turn: int, isField: bool, isHand: bool):
        self.cards = cards
        self.pos = init
        self.turn = turn
        self.isField = isField
        self.isHand = isHand
        self.isMyTurn = isMyTurn

    def checkClicks(self, pos: Tuple[int, int], ):
        if cardsInfoBtns['goLeft'].click(pos):
            self.changeCard('left')
        elif cardsInfoBtns['goRight'].click(pos):
            self.changeCard('right')
        elif cardsInfoBtns['attack'].click(pos):
            print('attack')
        elif cardsInfoBtns['effect'].click(pos):
            print('effect')
        elif cardsInfoBtns['summon'].click(pos) and self.isHand and self.isMyTurn and self.turn == 2:
            self.summonCard(self.pos)
        elif cardsInfoBtns['phaseAttack'].click(pos) and self.isMyTurn and self.turn == 2:
            self.battlePhase()
        elif cardsInfoBtns['summon'].click(pos) and self.isMyTurn and self.turn > 1:
            self.summonCard()

    def draw(self, win: pygame.Surface):
        if len(self.cards) == 0:
            return
        self.cardSelected = self.cards[self.pos]
        font = loadCustomFont(24, 'nunito')
        cardType = self.cardSelected.card['card_type']
        cardImg = pygame.image.load(self.cardSelected.card['card_image'])
        cardImg = pygame.transform.scale(cardImg, (370, 400))
        pygame.draw.rect(
            win, (0, 0, 0, 0), (10, 70, 380, 800))
        win.blit(cardImg, (15, 80))
        blit_complex_text(
            win, self.cardSelected.card['card_description'], (18, 480), font, 364, (233, 233, 233))

        if len(self.cards) >= 3:
            if self.pos > 0:
                cardsInfoBtns['goLeft'].draw(win)
            if self.pos + 1 < len(self.cards):
                cardsInfoBtns['goRight'].draw(win)

        if self.isMyTurn:

            if self.isHand:
                # if self.turn == 2:
                cardsInfoBtns['summon'].draw(win)
                # elif self.turn == 3:
                cardsInfoBtns['attack'].draw(win)
                # if cardType == 'magic' or cardType == 'effectMonster':
                cardsInfoBtns['effect'].draw(win)
            elif self.isField:
                if cardType == 'magic' or cardType == 'effectMonster':
                    cardsInfoBtns['effect'].draw(win)
            if self.turn == 2:
                cardsInfoBtns['phaseAttack'].draw(win)
            if self.turn > 1:
                cardsInfoBtns['endTurn'].draw(win)
