
from typing import List, Tuple

import pygame
from src.components.button import ButtonDuels
from src.components.buttonImg import ButtonImage
from src.components.card import Card
from src.services.getFont import loadCustomFont
from src.services.renders import blit_complex_text

width = 1280
height = 980

cardsInfoBtns = {
    'summon': ButtonImage('summon', 20, height - 95),
    'attack': ButtonImage('attack', 154, height - 95),
    'confirmAttack': ButtonDuels('confirmar', 154, height - 95, (159, 187, 193), 100, 30, 14, 20),
    'effect': ButtonImage('activate', 280, height - 95),
    'phaseAttack': ButtonImage('attackPhase', 20, height - 50),
    'endTurn': ButtonImage('endPhase', 220, height - 50),
    'goLeft': ButtonImage('left', 20, 430),
    'goRight': ButtonImage('right', 350, 430),
}


class CardsInfo:
    def __init__(self, summon, battlePhase, endPhase, attack, confirmattack):
        self.cards = []
        self.pos = -1
        self.turn = 1
        self.isField = False
        self.isHand = False
        self.isMyTurn = True
        self.round = 0
        self.summonCard = summon
        self.battlePhase = battlePhase
        self.endPhase = endPhase
        self.attack = attack
        self.confirmattack = confirmattack
        self.cardSelected = None
        self.isAttack = False
        self.isEnemy = False

    def changeCard(self, action: str):
        self.cardSelected.deselectCard()
        if action == 'left' and self.pos > 0:
            self.pos -= 1
        elif action == 'right' and self.pos + 1 < len(self.cards):
            self.pos += 1
        if self.cards:
            self.cardSelected = self.cards[self.pos]
            self.cardSelected.selectCard()

    def updateDraw(self, cards: List[Card], init: int, isMyTurn: bool, turn: int, isField: bool, isHand: bool, roundCount: int, isAttack: bool, isEnemy: bool):
        if (self.cardSelected):
            self.cardSelected.deselectCard()

        self.cards = cards
        self.pos = init
        self.turn = turn
        self.round = roundCount
        self.isField = isField
        self.isHand = isHand
        self.isMyTurn = isMyTurn
        self.isAttack = isAttack
        self.isEnemy = isEnemy
        self.font = loadCustomFont(24, 'nunito')
        if self.cards:
            self.cardSelected = self.cards[self.pos]
            if not (self.isAttack and self.isEnemy):
                self.cardSelected.selectCard()
        else:
            self.cardSelected = None

    def checkClicks(self, pos: Tuple[int, int], ):
        if cardsInfoBtns['goLeft'].click(pos):
            self.changeCard('left')
        elif cardsInfoBtns['goRight'].click(pos):
            self.changeCard('right')
        elif cardsInfoBtns['attack'].click(pos) and not(self.isEnemy):
            self.attack(self.cardSelected)
        elif cardsInfoBtns['effect'].click(pos):
            print('effect')
        elif cardsInfoBtns['confirmAttack'].click(pos) and self.isAttack and self.isEnemy:
            self.confirmattack(self.cardSelected)
        elif cardsInfoBtns['summon'].click(pos) and self.isHand and self.isMyTurn and self.turn == 2:
            self.summonCard(self.pos)
        elif cardsInfoBtns['phaseAttack'].click(pos) and self.isMyTurn and self.turn == 2 and self.round > 1:
            self.battlePhase()
        elif cardsInfoBtns['endTurn'].click(pos) and self.isMyTurn and self.turn > 1:
            self.endPhase()

    def draw(self, win: pygame.Surface, myTurn):
        self.isMyTurn = myTurn
        if len(self.cards) > 0:
            pygame.draw.rect(
                win, (0, 0, 0, 0), (10, 70, 380, 780))

            cardType = self.cardSelected.card['card_type']
            cardImg = pygame.image.load(self.cardSelected.card['card_image'])
            cardImg = pygame.transform.scale(cardImg, (370, 400))
            name = self.font.render(
                self.cardSelected.card['card_name'], True, (233, 233, 233))
            cust = self.font.render(
                "Custo de mana: " + str(self.cardSelected.card['card_cust']), True, (233, 233, 233))
            win.blit(cardImg, (15, 78))
            win.blit(name, (18, 480))
            win.blit(cust, (18, 515))
            if self.cardSelected.card['card_type'] != 'spell' and self.cardSelected.card['card_type'] != 'trap':
                element = self.font.render(
                    "Elemento: " + self.cardSelected.card['card_element'], True, (233, 233, 233))
                attack = self.font.render(
                    "Ataque: " + str(self.cardSelected.card['card_attack']), True, (233, 233, 233))
                defense = self.font.render(
                    "Defesa: " + str(self.cardSelected.card['card_def']), True, (233, 233, 233))
                win.blit(element, (18, 550))
                win.blit(attack, (238, 515))
                win.blit(defense, (238, 550))

            blit_complex_text(
                win, "Descrição: " + self.cardSelected.card['card_description'], (18, 585), self.font, 364, (233, 233, 233))

            if len(self.cards) >= 2 and self.pos > 0:
                cardsInfoBtns['goLeft'].draw(win)
            if self.pos + 1 < len(self.cards):
                cardsInfoBtns['goRight'].draw(win)

        print(self.isMyTurn)
        if myTurn:
            if self.turn > 1:
                cardsInfoBtns['endTurn'].draw(win)
            if self.round > 1 and self.turn == 2:
                cardsInfoBtns['phaseAttack'].draw(win)
            if len(self.cards) > 0:
                if self.isAttack and self.isEnemy:
                    cardsInfoBtns['confirmAttack'].draw(win)
                elif self.isHand:
                    if self.turn == 2:
                        cardsInfoBtns['summon'].draw(win)
                    if cardType == 'spell':
                        cardsInfoBtns['effect'].draw(win)
                elif self.isField:
                    if cardType == 'spell' or cardType == 'monster effect':
                        cardsInfoBtns['effect'].draw(win)
                    if self.turn == 3 and cardType != 'spell' and self.turn == 3 and cardType != 'trap':
                        cardsInfoBtns['attack'].draw(win)
