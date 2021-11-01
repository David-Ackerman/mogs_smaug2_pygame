from typing import Tuple
import pygame
from duel import Duel
from network import Network
pygame.font.init()

width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Client')


class Button:
    def __init__(self, text: str, x: int, y: int, color: tuple[int, int, int]):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 160
        self.height = 100

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))
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


btns = [Button("Rock", 50, 500, (0, 0, 0)), Button(
        "Scissors", 255, 500, (255, 0, 0)), Button("Paper", 460, 500, (0, 255, 0))]


class Client():
    def __init__(self):
        self.a = 1

    def redrawWindow(self, win: pygame.Surface, game: Duel, p):
        win.fill((128, 128, 128))

        if not(game.connected()):
            font = pygame.font.SysFont("comicsans", 70)
            text = font.render("Waiting for Player...", True, (255, 0, 0))
            win.blit(text, (width/2 - text.get_width() /
                            2, height/2 - text.get_height()/2))
        else:
            font = pygame.font.SysFont("comicsans", 50)
            text = font.render("Your Move", 1, (0, 255, 255))
            win.blit(text, (80, 200))

            text = font.render("Opponents", 1, (0, 255, 255))
            win.blit(text, (380, 200))

            move1 = game.get_player_move(0)
            move2 = game.get_player_move(1)

            if game.bothWent():
                text1 = font.render(move1, 1, (0, 0, 0))
                text2 = font.render(move2, 1, (0, 0, 0))
            else:
                if game.p1Went and p == 0:
                    text1 = font.render(move1, 1, (0, 0, 0))
                elif game.p1Went:
                    text1 = font.render("Locked In", 1, (0, 0, 0))
                else:
                    text1 = font.render("Waiting...", 1, (0, 0, 0))

                if game.p2Went and p == 1:
                    text2 = font.render(move2, 1, (0, 0, 0))
                elif game.p2Went:
                    text2 = font.render("Locked In", 1, (0, 0, 0))
                else:
                    text2 = font.render("Waiting...", 1, (0, 0, 0))

            if p == 1:
                win.blit(text2, (100, 350))
                win.blit(text1, (400, 350))
            else:
                win.blit(text1, (100, 350))
                win.blit(text2, (400, 350))

            for btn in btns:
                btn.draw(win)
        pygame.display.update()

    def main(self):
        run = True
        clock = pygame.time.Clock()
        n = Network()
        player = int(n.getP())
        print("You are player", player)

        while run:
            clock.tick(30)
            try:
                game: Duel = n.send("get")
            except:
                run = False
                print("Couldn't get game")
                break

            if game.bothWent():
                self.redrawWindow(win, game, player)
                pygame.time.delay(500)
                try:
                    game = n.send('reset')
                except:
                    run = False
                    print("Couldn't get game")
                    break

                font = pygame.font.SysFont("comicsans", 80)
                if game.winner() == -1:
                    text = font.render("Tie Game!", 1, (255, 0, 0))
                elif game.winner() == player:
                    text = font.render("You Won!", 1, (255, 0, 0))
                else:
                    text = font.render("You Lost...", 1, (255, 0, 0))

                win.blit(text, (width/2 - text.get_width() /
                                2, height/2 - text.get_height()/2))
                pygame.display.update()
                pygame.time.delay(2000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if btn.click(pos) and game.connected():
                            if player == 0:
                                if not game.p1Went:
                                    n.send(btn.text)
                            else:
                                if not game.p2Went:
                                    n.send(btn.text)
            self.redrawWindow(win, game, player)

    def render_self(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(30)
            win.fill((128, 128, 128))
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Click to Play!", 1, (255, 0, 0))
            win.blit(text, (100, 200))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        self.main()
