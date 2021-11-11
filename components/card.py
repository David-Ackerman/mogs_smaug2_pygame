from typing import Tuple
import pygame
from pygame import surface

from interfaces.card_model import Deck
from services.getFont import loadCustomFont


CARD_WIDTH = {'default': 100, 'deckMenu': 200}
CARD_HEIGHT = {'default': 140, 'deckMenu': 280}


CARD_COMPOSE_COORD = {
    'default': {
        'template': (0, 0),
        'cardIcon': (8, 12),
        'power': (55, CARD_HEIGHT['default'] - 16),
    },
    'deckMenu': {
        'template': (2, 2),
        'cardIcon': (10, 13),
        'power': (57, CARD_HEIGHT['deckMenu'] - 16),
    }
}


class Card(pygame.sprite.Sprite):
    def __init__(self, card: Deck, isBack: bool, isDeckMenu: bool, isMenuDeckSelected: bool = False, id: str = '0', flip=False):
        super().__init__()
        self.card, self.flipped, self.cardOnDuelId, self.isDeckMenu = card, flip, id, isDeckMenu
        self.selection = 'deckMenu' if self.isDeckMenu else 'default'
        self.coords = CARD_COMPOSE_COORD[self.selection]
        self.myfont = loadCustomFont(14, 'nunito-bold')
        self.surf = pygame.Surface(
            (CARD_WIDTH[self.selection], CARD_HEIGHT[self.selection]))
        self.menuDeckSelected = isMenuDeckSelected
        self.isBack = isBack
        self.build_card()
        self.image = self.surf
        self.rect = self.image.get_rect()

    def click(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]
        y = self.rect.y
        x = self.rect.x
        if x <= x1 <= x + CARD_WIDTH[self.selection] and y <= y1 <= y + CARD_HEIGHT[self.selection]:
            return True
        else:
            return False

    def build_card(self):
        cardType = self.card['card_element']
        if self.isBack:
            img = pygame.image.load('assets/cardTemplates/cardBack.png')
            if self.flipped:
                img = pygame.transform.flip(img, False, True)
            img = pygame.transform.scale(img, (100, 140))

            self.surf.blit(img, (0, 0))
        else:
            if(self.isDeckMenu):
                if(self.menuDeckSelected):
                    self.surf.fill((20, 200, 40))
                else:
                    self.surf.fill((20, 20, 20))
            cardPath = 'assets/cardTemplates/cardFront-' + \
                ('normal' if cardType == 'knight' or cardType ==
                 None else cardType) + '.png'
            # print(cardPath)
            bgImg = pygame.image.load(cardPath)
            bgImg = pygame.transform.scale(bgImg, (100, 140))
            cardImg = pygame.image.load(self.card['card_image'])
            cardImg = pygame.transform.scale(cardImg, (82, 102))
            # textSurf = self.myfont.render(str(self.power),
            #                               True, (50, 50, 50))
            self.surf.blit(bgImg, self.coords['template'])
            self.surf.blit(cardImg, self.coords['cardIcon'])
            # self.surf.blit(textSurf,  self.coords['power'])
            if self.flipped:
                self.surf = pygame.transform.flip(self.surf, False, True)

    def setSelectedOnDeckMenu(self):
        self.menuDeckSelected = not self.menuDeckSelected
        self.build_card()
