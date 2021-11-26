import pygame
from src.server.duel import Duel
from network import Network
from src.screens.s_duel import DuelGame
from src.services.getFont import loadCustomFont
from subprocess import Popen

images = [
    pygame.image.load('assets/waiting/waiting1.png'),
    pygame.image.load('assets/waiting/waiting2.png'),
    pygame.image.load('assets/waiting/waiting3.png'),
    pygame.image.load('assets/waiting/waiting4.png'),
    pygame.image.load('assets/waiting/waiting5.png'),
    pygame.image.load('assets/waiting/waiting6.png'),
    pygame.image.load('assets/waiting/waiting7.png'),
    pygame.image.load('assets/waiting/waiting8.png'),
    pygame.image.load('assets/waiting/waiting9.png'),
    pygame.image.load('assets/waiting/waiting10.png'),
    pygame.image.load('assets/waiting/waiting11.png'),
    pygame.image.load('assets/waiting/waiting12.png')
]


class Client():
    def __init__(self, game):
        self.game = game
        self.index = 0

    def redrawWindow(self, win: pygame.Surface):
        win.blit(self.image, (0, 0))
        self.animateBackground()
        pygame.display.update()

    def animateBackground(self):
        self.index += 1
        if self.index >= len(images):
            self.index = 0
        self.image = pygame.transform.scale(
            images[self.index], (self.game.WIDTH, self.game.HEIGHT))
        pygame.time.delay(60)

    def getConnection(self):
        n = Network(self.game.userName)
        player = int(n.getP()['player'])
        gameUser = self.game.userName + str(player)
        return (n, player, gameUser)

    def main(self):
        self.index = 0
        self.image = pygame.transform.scale(
            images[self.index], (self.game.WIDTH, self.game.HEIGHT))
        self.run_display = True
        clock = pygame.time.Clock()
        try:
            n, player, gameUser = self.getConnection()
        except Exception as e:
            self.game.server = Popen('python server.py')
            try:
                n, player, gameUser = self.getConnection()
            except:
                self.run_display = False
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
        self.game.duelGame = DuelGame(self.game, n, player, gameUser, duel)
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
            self.game.window.blit(text, (self.game.WIDTH/2 - text.get_width() /
                                         2, self.game.HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
        self.main()
