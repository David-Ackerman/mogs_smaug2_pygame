from threading import Timer
from typing import Tuple
import pygame
from src.interfaces.card_model import Fonts

from src.services.getFont import loadCustomFont

pygame.font.init()


class ButtonDuels:
    def __init__(self, text: str, x: int, y: int,  color, font: Fonts = 'nunito-bold', width: int = 160, height: int = 100, radius: int = -1, textSize: int = 35, textColor=(255, 255, 255)):
        self.text = text
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.width = width
        self.clickColor = (self.color[0] - 80,
                           self.color[0] - 80, self.color[0] - 80)
        self.height = height
        self.clicked = False
        self.textSize = textSize
        self.textColor = textColor
        self.font = font

    def despress(self):
        self.clicked = False

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(
            win, self.clickColor if self.clicked else self.color, (self.x, self.y, self.width, self.height), border_radius=self.radius)
        font = loadCustomFont(self.textSize, self.font)
        text = font.render(self.text, True, self.textColor)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                 self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            self.clicked = True
            t = Timer(0.25, self.despress)
            t.start()
            return True
        else:
            return False
