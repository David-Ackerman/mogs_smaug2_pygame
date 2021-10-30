from typing import Tuple
import pygame
from network import Network
from player import Player

width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')


class Button:
    def __init__(self, text: str, x: int, y: int, color: tuple[int, int, int]):
        self.text, self.x, self.y, self.color = text, x, y, color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self, height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                 self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))
    pass


btns = [Button("Rock", 50, 500, (255, 0, 0)), Button(
    "Scissors", 250, 500, (255, 0, 0)), Button("Paper", 450, 500, (0, 255, 0))]


def main():
    pass


main()
