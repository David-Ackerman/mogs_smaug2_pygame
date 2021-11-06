
from typing import List

import pygame
from components.card import Card
from services.getFont import loadCustomFont
from services.renders import blit_complex_text


class CardsInfo:
    def __init__(self):
        self.cards = []
        self.pos = -1

    def updateDraw(self, cards: List[Card], init: int):
        self.cards = cards
        self.pos = init

    def draw(self, win: pygame.Surface):
        print(self.cards, self.pos)
        if len(self.cards) == 0:
            return
        font = loadCustomFont(24, 'nunito')
        cardImg = pygame.image.load(self.cards[self.pos].cardImg)
        cardImg = pygame.transform.scale(cardImg, (370, 400))
        pygame.draw.rect(
            win, (0, 0, 0, 0), (10, 70, 380, 800))
        win.blit(cardImg, (15, 80))
        blit_complex_text(
            win, self.cards[self.pos].card['text'], (18, 480), font, 364, (233, 233, 233))
