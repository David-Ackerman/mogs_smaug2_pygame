import pygame
import pygame_widgets
from pygame_widgets.button import Button
from components.card import Card
from interfaces.card_model import Deck
from interfaces.cards import cards
from services.saveDeck import saveDeckOnDisk

breaks = [1, 2, 3, 4, 5]


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 60
        self.deckx, self.decky = self.mid_w, self.mid_h + 90
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 80)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Deck", 20, self.deckx, self.decky)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor(),
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.deckx + self.offset, self.decky)
                self.state = "Deck"
            elif self.state == "Deck":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.deckx + self.offset, self.decky)
                self.state = "Deck"
            elif self.state == "Deck":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.curr_screen = self.game.player
            elif self.state == "Options":
                self.game.curr_screen = self.game.options_menu
            elif self.state == "Deck":
                self.game.curr_screen = self.game.deck_menu
            elif self.state == "Credits":
                self.game.curr_screen = self.game.credits_menu

            self.run_display = False
            self.game.curr_screen.render_self()


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Options", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text("Volume", 20, self.volx, self.voly)
            self.game.draw_text("Controls", 20, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_screen = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == "Volume":
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = "Controls"
            elif self.state == "Controls":
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = "Volume"
        elif self.game.START_KEY:
            # TO-DO: Adicionar menu de volume e de controles
            pass


class DeckMenu(Menu):
    def __init__(self, game, playerDeck: list[Deck]):
        Menu.__init__(self, game)
        self.playerDeck: list[Deck] = playerDeck[:]
        self.cards: list[Deck] = []
        self.row = 0
        self.column = 0
        self.all_sprites_list = pygame.sprite.Group()
        self.playerCardpos = [10, 100]
        for card in cards:
            self.cards.append(
                Card(card=card, isBack=False, isDeckMenu=True, isMenuDeckSelected=card in self.playerDeck)
            )
        for i in range(len(self.cards)):
            self.cards[i].rect.x = self.playerCardpos[0] + (self.column * 128)
            self.cards[i].rect.y = self.playerCardpos[1] + (self.row * 160)
            self.column += 1
            if (i + 1) / 10 in breaks:
                self.row += 1
                self.column = 0
        self.button = Button(
            self.game.display,
            1100,
            650,
            100,
            40,
            text="Save",
            fontSize=30,
            margin=20,
            radius=8,
            onClick=lambda: saveDeckOnDisk(self.playerDeck),
        )
        self.all_sprites_list.add(self.cards)
        self.clock = pygame.time.Clock()

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            events = pygame.event.get()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Monte seu deck clicando nas cartas que deseja", 40, self.game.DISPLAY_W / 2, 40)
            self.all_sprites_list.update()
            self.all_sprites_list.draw(self.game.display)
            pygame_widgets.update(events)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_screen = self.game.main_menu
            self.run_display = False
        elif self.game.CLICKED:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [s for s in self.all_sprites_list if s.rect.collidepoint(pos)]
            if len(clicked_sprites) > 0:
                clicked_sprites[0].setSelectedOnDeckMenu()
                if clicked_sprites[0].menuDeckSelected:
                    self.playerDeck.append(clicked_sprites[0].card)
                else:
                    self.playerDeck.remove(clicked_sprites[0].card)
        elif self.game.START_KEY:
            # TO-DO: Adicionar menu de volume e de controles
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_screen = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Credits", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text("Made by master of gamblers", 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.blit_screen()
