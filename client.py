import pygame
from duel import Duel
from network import Network
from screens.s_duel import DuelGame
from services.getFont import loadCustomFont

width = 1280
height = 880


class Client():
    def __init__(self, game):
        self.game = game

    def redrawWindow(self, win: pygame.Surface):
        win.fill((128, 128, 128))
        font = loadCustomFont(70, 'nunito-bold')
        text = font.render("Waiting for Player...", True, (255, 0, 0))
        win.blit(text, (width/2 - text.get_width() /
                        2, height/2 - text.get_height()/2))
        pygame.display.update()

    def main(self):
        self.run_display = True
        clock = pygame.time.Clock()
        n = Network()
        player = int(n.getP()['player'])
        while self.run_display:
            clock.tick(30)
            try:
                duel: Duel = n.send({'action': 'standby'})
            except Exception as e:
                self.run_display = False
                print("Couldn't get game", e)
                self.game.goToMenuScreen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if(duel.connected()):
                self.run_display = False
            self.redrawWindow(self.game.window)
        self.game.duelGame = DuelGame(self.game, n, player, duel)
        self.game.curr_screen = self.game.duelGame
        self.game.curr_screen.render_self()

    def render_self(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.goToMenuScreen()
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

            self.game.window.fill((128, 128, 128))
            font = loadCustomFont(60, 'nunito-bold')
            text = font.render("Click to search a duel!", 1, (255, 40, 67))
            self.game.window.blit(text, (width/2 - text.get_width() /
                                         2, height/2 - text.get_height()/2))
            pygame.display.update()
        self.main()
