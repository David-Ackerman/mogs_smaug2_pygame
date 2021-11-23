import pygame
from pygame.locals import *
from client import Client
from src.screens.menu import *
from src.screens.s_duel import DuelGame
from src.services.getFont import loadCustomFont
from src.services.saveDeck import loadDeckOnDisk


class Game:
    def __init__(self):
        pygame.init()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        gameIcon = pygame.image.load('assets/gameIcon.jpg')
        self.running, self.playing = True, False
        self.lastEvent = None
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.CLICKED = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 980
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption(
            'Masters of Gamblers')
        pygame.display.set_icon(gameIcon)
        response = loadDeckOnDisk()
        self.playerDeck = response["deck"] if response['hasDeck'] else []
        self.userName = response['userName'] if response['hasDeck'] else ''
        self.volume = response['options']['vol'] if response['hasDeck'] else 0.1
        self.music = pygame.mixer.music
        self.music.load("assets/sounds/dramatic.wav")
        self.music.play()
        self.music.set_volume(self.volume)
        self.main_menu = MainMenu(self)
        self.deck_menu = DeckMenu(self, self.playerDeck)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.player = Client(self)
        self.curr_screen = self.main_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_screen.run_display = False

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

    def draw_text(self, text, size, x, y, font='magic'):
        font = loadCustomFont(size, font)
        text_surface = font.render(text, True, self.WHITE)
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
