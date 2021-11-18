from typing import Tuple
import typing
import pygame
from threading import Timer

pygame.font.init()

buttons = {
    'activate': 'assets/buttons/btn_activate',
    'attack': 'assets/buttons/btn_attack',
    'attackPhase': 'assets/buttons/btn_attackPhase',
    'endPhase': 'assets/buttons/btn_endPhase',
    'left': 'assets/buttons/btn_left',
    'right': 'assets/buttons/btn_right',
    'save': 'assets/buttons/btn_save',
    'summon': 'assets/buttons/btn_summon',
}


class ButtonImage:
    def __init__(self, img: typing.Literal['activate', 'attack', 'attackPhase', 'endPhase', 'left', 'right', 'save', 'summon'], x: int, y: int):
        self.x = x
        self.y = y
        self.imgPath = buttons[img]
        self.image = pygame.image.load(self.imgPath + '.png')

    def draw(self, win: pygame.Surface):
        win.blit(self.image, (self.x, self.y))

    def despress(self):
        self.image = pygame.image.load(self.imgPath + '.png')

    def click(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.image.get_width() and self.y <= y1 <= self.y + self.image.get_height():
            self.image = pygame.image.load(self.imgPath + '_press.png')
            t = Timer(0.2, self.despress)
            t.start()
            return True
        else:
            return False
