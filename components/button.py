from typing import Tuple
import pygame

pygame.font.init()


class ButtonDuels:
    def __init__(self, text: str, x: int, y: int,  color, width: int = 160, height: int = 100, radius: int = -1):
        self.text = text
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.width = width
        self.height = height

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height), border_radius=self.radius)
        font = pygame.font.SysFont("comicsans", 35)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                 self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos: Tuple[int, int]):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
