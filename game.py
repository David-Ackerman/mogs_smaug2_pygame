from src.services.saveDeck import loadDeckOnDisk
from src.services.getFont import loadCustomFont
from src.screens.s_duel import DuelGame
from src.screens.menu import *
from client import Client
from subprocess import Popen
import pygame
from pygame.locals import *
from src.services.compressImg import compressAssets, decompressAssets


class Game:
    def __init__(self):
        decompressAssets()
        pygame.init()
        infos = pygame.display.Info()
        self.WIDTH, self.HEIGHT = infos.current_w, infos.current_h - 80
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        gameIcon = pygame.image.load('assets\images\gameIcon.jpg')
        self.running, self.playing = True, False
        self.server = None
        self.lastEvent = None
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.CLICKED = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = self.WIDTH, self.HEIGHT
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(
            'Masters of Gamblers')
        pygame.display.set_icon(gameIcon)
        response = loadDeckOnDisk()
        self.playerDeck = response["deck"] if response['hasDeck'] else []
        self.userName = response['userName'] if response['hasDeck'] else ''
        self.volume = response['options']['vol'] if response['hasDeck'] else 0.1
        self.music = pygame.mixer.music
        self.music.set_volume(self.volume)

        self.main_menu = MainMenu(self)
        self.help_menu = HelpMenu(self)
        self.deck_menu = DeckMenu(self, self.playerDeck)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.player = Client(self)
        self.curr_screen = self.main_menu

    def finish(self):
        compressAssets()
        self.running, self.playing = False, False
        self.curr_screen.run_display = False
        if self.server:
            Popen.kill(self.server)
        pygame.quit()
        sys.exit()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finish()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    self.CLICKED = True
            elif event.type == pygame.KEYDOWN:
                self.lastEvent = event
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY, self.CLICKED = False, False, False, False, False

    def draw_text(self, text, size, x, y, color=(255, 255, 255), font='magic'):
        font = loadCustomFont(size, font)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.window.blit(text_surface, text_rect)

    def goToMenuScreen(self):
        self.BACK_KEY = True
        self.curr_screen = ""
        self.player = ''
        self.player = Client(self)
        self.main_menu = MainMenu(self)
        self.curr_screen = self.main_menu
        self.reset_keys()
        self.curr_screen.render_self()


def initGame():
    g = Game()
    g.curr_screen.render_self()


initGame()
