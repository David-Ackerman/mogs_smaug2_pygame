from typing import Tuple
import pygame

from src.interfaces.card_model import Deck
from src.services.getFont import loadCustomFont


CARD_WIDTH = {'default': 104, 'deckMenu': 204}
CARD_HEIGHT = {'default': 144, 'deckMenu': 284}

IMG_WH = {
    'default': (82, 102),
    'deckMenu': (166, 204)
}

CARD_COMPOSE_COORD = {
    'default': {
        'card': (2, 2),
        'image': (10, 14),
        'name': (6, 115),
        'attack': (55, CARD_HEIGHT['default'] - 16),
        'defense': (55, CARD_HEIGHT['default'] - 16),
        'cust': (55, CARD_HEIGHT['default'] - 16),
    },
    'deckMenu': {
        'card': (2, 2),
        'image': (18, 24),
        'name': (12, 230),
        'attack': (55, CARD_HEIGHT['deckMenu'] - 16),
        'defense': (55, CARD_HEIGHT['deckMenu'] - 16),
        'cust': (55, CARD_HEIGHT['deckMenu'] - 16),
    }
}


class Card(pygame.sprite.Sprite):
    def __init__(self, card: Deck, isBack: bool, isDeckMenu: bool, isSelected: bool = False, selectionColor=(20, 200, 40, 255), flip=False):
        super().__init__()
        self.card, self.flipped, self.cardOnDuelId = card, flip, card['onGameId']
        self.selection = 'deckMenu' if isDeckMenu else 'default'
        self.isSelected = isSelected
        self.selectionColor = selectionColor
        self.coords = CARD_COMPOSE_COORD[self.selection]

        self.myfont = loadCustomFont(14 if isDeckMenu else 8, 'nunito-bold')
        self.surf = pygame.Surface(
            (CARD_WIDTH[self.selection], CARD_HEIGHT[self.selection]), pygame.SRCALPHA)
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

    def selectCard(self, color=(20, 200, 40, 255)):
        self.isSelected = True
        self.selectionColor = color
        self.build_card(True)

    def deselectCard(self):
        self.isSelected = False
        self.build_card()

    def flipCard(self):
        self.isBack = not self.isBack
        self.build_card()

    def build_card(self, notFlip=False):

        cardType = self.card['card_element']
        if self.isBack:
            img = pygame.image.load('assets/cardTemplates/cardBack.png')
            self.surf.fill((0, 0, 0, 0))
            if self.flipped:
                img = pygame.transform.flip(img, False, True)
            img = pygame.transform.scale(img, (102, 142))
            self.surf.blit(img, (0, 0))
        else:
            if self.isSelected:
                self.surf.fill(self.selectionColor)
            else:
                self.surf.fill((0, 0, 0, 0))
            cardPath = 'assets/cardTemplates/cardFront-' + \
                ('normal' if cardType == 'knight' or cardType ==
                 None else cardType) + '.png'
            bgImg = pygame.image.load(cardPath)
            cardImg = pygame.image.load(self.card['card_image'])
            cardName = self.myfont.render(
                self.card['card_name'], True, (20, 20, 20))
            cardCust = self.myfont.render(
                str(self.card['card_cust']), True, (20, 20, 20))
            cardAttack = self.myfont.render(
                str(self.card['card_attack']), True, (20, 20, 20))
            cardDef = self.myfont.render(
                str(self.card['card_def']), True, (20, 20, 20))
            if self.selection == 'default':
                bgImg = pygame.transform.scale(bgImg, (100, 140))
            cardImg = pygame.transform.scale(cardImg, IMG_WH[self.selection])

            self.surf.blit(bgImg, self.coords['card'])
            self.surf.blit(cardImg, self.coords['image'])
            self.surf.blit(cardName, self.coords['name'])
            if self.flipped and not(notFlip):
                self.surf = pygame.transform.rotate(self.surf, 180)

    def setSelectedOnDeckMenu(self):
        self.isSelected = not self.isSelected
        self.build_card()
