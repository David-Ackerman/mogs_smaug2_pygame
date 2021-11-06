from typing import Tuple
import pygame

from interfaces.card_model import Deck


CARD_WIDTH = {'default': 100, 'deckMenu': 104}
CARD_HEIGHT = {'default': 140, 'deckMenu': 144}
CARD_COMPOSE_COORD = {
    'default': {
        'template': (0, 0),
        'cardIcon': (4, 9),
        'power': (55, CARD_HEIGHT['default'] - 12)
    },
    'deckMenu': {
        'template': (2, 2),
        'cardIcon': (6, 11),
        'power': (57, CARD_HEIGHT['deckMenu'] - 14)
    }
}


class Card(pygame.sprite.Sprite):
    def __init__(self, card: Deck, isBack: bool, isDeckMenu: bool, isMenuDeckSelected: bool = False, id: str = 0):
        super().__init__()
        self.card = card
        self.cardOnDuelId = id
        self.isDeckMenu = isDeckMenu
        self.selection = 'default'
        if(self.isDeckMenu):
            self.selection = 'deckMenu'
        self.coords = CARD_COMPOSE_COORD[self.selection]
        self.myfont = pygame.font.Font(pygame.font.get_default_font(), 12)
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
        if x <= x1 <= x + CARD_WIDTH['default'] and y <= y1 <= y + CARD_HEIGHT['default']:
            return True
        else:
            return False

    def build_card(self):
        if self.isBack:
            self.surf.blit(pygame.image.load('assets/card.png'), (0, 0))
        else:
            if(self.isDeckMenu):
                if(self.menuDeckSelected):
                    self.surf.fill((20, 200, 40))
                else:
                    self.surf.fill((20, 20, 20))
            self.surf.blit(pygame.image.load(
                'assets/cardFront.png'), self.coords['template'])
            self.surf.blit(pygame.image.load(self.cardImg),
                           self.coords['cardIcon'])
            self.surf.blit(self.myfont.render(str(self.power),
                           True, (0, 0, 0)),  self.coords['power'])

    def setSelectedOnDeckMenu(self):
        self.menuDeckSelected = not self.menuDeckSelected
        self.build_card()
