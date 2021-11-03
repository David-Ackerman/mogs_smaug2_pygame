import pygame
from pygame.locals import *
from screens.menu import *
from client import Client
from services.saveDeck import loadDeckOnDisk


class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.CLICKED = False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 880
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(
            ((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        response = loadDeckOnDisk()
        self.main_menu = MainMenu(self)
        self.deck_menu = DeckMenu(self, playerDeck=response["deck"])
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        # self.player = Player(self, playerDeck=response["deck"])
        self.player = Client(self)
        self.curr_screen = self.main_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_screen.run_display = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    self.CLICKED = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.BACK_KEY, self.START_KEY, self.CLICKED = False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


g = Game()
g.curr_screen.render_self()
