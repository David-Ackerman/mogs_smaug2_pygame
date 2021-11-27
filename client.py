import pygame
from network import Network
from src.components.button import ButtonDuels
from src.screens.s_duel import DuelGame
from src.server.duel import Duel
from src.services.getFont import loadCustomFont
from subprocess import Popen


class Client():
    def __init__(self, game):
        self.game = game
        self.index = 0
        self.base_font = loadCustomFont(25)
        self.ip = ""
        self.ipPos = (self.game.WIDTH/2 - 140, self.game.HEIGHT/2 - 80)
        self.ipPos = (self.game.WIDTH/2 - 140, self.game.HEIGHT/2 - 80)
        self.volume = self.game.volume
        self.input_rect = pygame.Rect(
            self.ipPos[0] + 20, self.ipPos[1], 200, 36)
        self.searchButton = ButtonDuels(
            'Procurar', self.ipPos[0] + 180, self.ipPos[1], (200, 200, 200), 'rooters', 30, 30, 10, 25, textColor=(20, 20, 20))
        self.hostButton = ButtonDuels('Hospedar', self.game.WIDTH/2 - 40, self.game.HEIGHT /
                                      2 - 20, (200, 200, 200), 'rooters', 30, 30, 10, 25, textColor=(20, 20, 20))
        self.images = [
            pygame.image.load('assets/images/waiting/waiting1.png'),
            pygame.image.load('assets/images/waiting/waiting2.png'),
            pygame.image.load('assets/images/waiting/waiting3.png'),
            pygame.image.load('assets/images/waiting/waiting4.png'),
            pygame.image.load('assets/images/waiting/waiting5.png'),
            pygame.image.load('assets/images/waiting/waiting6.png'),
            pygame.image.load('assets/images/waiting/waiting7.png'),
            pygame.image.load('assets/images/waiting/waiting8.png'),
            pygame.image.load('assets/images/waiting/waiting9.png'),
            pygame.image.load('assets/images/waiting/waiting10.png'),
            pygame.image.load('assets/images/waiting/waiting11.png'),
            pygame.image.load('assets/images/waiting/waiting12.png')
        ]

    def redrawWindow(self, win: pygame.Surface):
        win.blit(self.image, (0, 0))
        self.animateBackground()
        pygame.display.update()

    def animateBackground(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = pygame.transform.scale(
            self.images[self.index], (self.game.WIDTH, self.game.HEIGHT))
        pygame.time.delay(60)

    def getConnection(self):
        n = Network(self.game.userName, self.ip)
        player = int(n.getP()['player'])
        gameUser = self.game.userName + str(player)
        return (n, player, gameUser)

    def main(self):
        self.index = 0
        self.image = pygame.transform.scale(
            self.images[self.index], (self.game.WIDTH, self.game.HEIGHT))
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
        self.game.music.stop()
        clock = pygame.time.Clock()
        run = True

        color_active = (233, 233, 233)
        color_passive = (150, 150, 150)
        color = color_passive
        self.text_active = False
        while run:
            clock.tick(30)
            self.check_input()
            color = color_active if self.text_active else color_passive
            self.game.window.fill(self.game.BLACK)
            text_surface = self.base_font.render(
                self.ip, True, (255, 255, 255))

            self.game.draw_text(
                "Busque uma partida(Se o campo ip estiver vazio usara o ip da sua maquina) ou inicie um servidor", 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 80)
            self.game.draw_text(
                "ip:", 25, self.ipPos[0], self.ipPos[1], font="nunito")

            self.game.window.blit(
                text_surface, (self.ipPos[0] + 22, self.ipPos[1]))
            self.searchButton.draw(self.game.window)
            self.hostButton.draw(self.game.window)
            pygame.draw.rect(self.game.window,
                             color, self.input_rect, 2)
            self.game.window.blit(self.game.window, (0, 0))
            pygame.display.flip()

        self.main()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.finish
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    self.text_active = False
                    pos = pygame.mouse.get_pos()
                    if self.serchButton.click(pos):
                        print('search')
                        return
                    elif self.input_rect.collidepoint(pos):
                        self.text_active = True
                        return
                    elif self.hostButton.click(pos):
                        print('host')
                        return
                    else:
                        self.text_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.goToMenuScreen()
                elif self.text_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.ip = self.ip[:-1]
                    else:
                        if len(self.ip) < 12:
                            self.ip += event.unicode
