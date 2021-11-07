from typing import Tuple
import pygame
from pygame import surface

from interfaces.card_model import Deck
from services.getFont import loadCustomFont


CARD_WIDTH = {'default': 100, 'deckMenu': 104}
CARD_HEIGHT = {'default': 140, 'deckMenu': 144}
CARD_COMPOSE_COORD = {
    'default': {
        'template': {'default': (0, 0), 'flipped': (0, 0)},
        'cardIcon': {'default': (4, 9), 'flipped': (4, CARD_HEIGHT['default'] - 122)},
        'power': {'default': (55, CARD_HEIGHT['default'] - 14), 'flipped': (55, 1)}
    },
    'deckMenu': {
        'template': {'default': (2, 2)},
        'cardIcon': {'default': (6, 11)},
        'power': {'default': (57, CARD_HEIGHT['deckMenu'] - 14)}
    }
}


class Card(pygame.sprite.Sprite):
    def __init__(self, card: Deck, isBack: bool, isDeckMenu: bool, isMenuDeckSelected: bool = False, id: str = '0', flip=False):
        super().__init__()
        self.card, self.flipped, self.cardOnDuelId, self.isDeckMenu = card, flip, id, isDeckMenu
        self.selection = 'deckMenu' if self.isDeckMenu else 'default'
        self.textPos = 'flipped' if self.flipped else 'default'
        self.coords = CARD_COMPOSE_COORD[self.selection]
        self.myfont = loadCustomFont(14, 'nunito-bold')
        self.surf = pygame.Surface(
            (CARD_WIDTH[self.selection], CARD_HEIGHT[self.selection]))
        self.cardImg = card['imageName']
        self.menuDeckSelected = isMenuDeckSelected
        self.type = card['card_type']
        self.power = card['card_power']
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
        if self.isBack:
            img = pygame.image.load('assets/card.png')
            if self.flipped:
                img = pygame.transform.flip(img, False, True)
            self.surf.blit(img, (0, 0))
        else:
            if(self.isDeckMenu):
                if(self.menuDeckSelected):
                    self.surf.fill((20, 200, 40))
                else:
                    self.surf.fill((20, 20, 20))
            bgImg = pygame.image.load('assets/cardFront.png')
            cardImg = pygame.image.load(self.cardImg)
            textSurf = self.myfont.render(str(self.power),
                                          True, (50, 50, 50))
            if self.flipped:
                bgImg = pygame.transform.flip(bgImg, False, True)
                cardImg = pygame.transform.flip(cardImg, False, True)
                textSurf = pygame.transform.flip(textSurf, False, True)
            self.surf.blit(bgImg, self.coords['template'][self.textPos])
            self.surf.blit(cardImg, self.coords['cardIcon'][self.textPos])
            self.surf.blit(textSurf,  self.coords['power'][self.textPos])

    def setSelectedOnDeckMenu(self):
        self.menuDeckSelected = not self.menuDeckSelected
        self.build_card()
