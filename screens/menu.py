import pygame
import pygame_widgets
import math
from pygame_widgets.button import Button
from components.card import Card
from interfaces.card_model import Deck
from interfaces.cards import cards
from services.saveDeck import saveDeckOnDisk


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text("*", 30, self.cursor_rect.x,
                            self.cursor_rect.y, 'magic')

    def blit_screen(self, scroll=0):
        self.game.window.blit(self.game.window, (0, scroll))
        pygame.display.flip()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80
        self.deckx, self.decky = self.mid_w, self.mid_h + 130
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 180
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.window.fill(self.game.BLACK)
            self.game.draw_text(
                "main menu", 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 180)
            self.game.draw_text("Start Game", 40, self.startx, self.starty)
            self.game.draw_text("Options", 40, self.optionsx, self.optionsy)
            self.game.draw_text("Deck", 40, self.deckx, self.decky)
            self.game.draw_text("Credits", 40, self.creditsx, self.creditsy)
            self.draw_cursor(),
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (
                    self.deckx + self.offset, self.decky)
                self.state = "Deck"
            elif self.state == "Deck":
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (
                    self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (
                    self.deckx + self.offset, self.decky)
                self.state = "Deck"
            elif self.state == "Deck":
                self.cursor_rect.midtop = (
                    self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (
                    self.startx + self.offset, self.starty)
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
        self.volx, self.voly = self.mid_w, self.mid_h + 30
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.window.fill(self.game.BLACK)
            self.game.draw_text(
                "Options", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text("Volume", 20, self.volx, self.voly)
            self.game.draw_text("Controls", 20, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.goToMenuScreen()
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == "Volume":
                self.cursor_rect.midtop = (
                    self.controlsx + self.offset, self.controlsy)
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
        self.scroll = 0
        self.column = 0
        self.all_sprites_list = pygame.sprite.Group()
        self.playerCardPos = [10, 100]
        for card in cards:
            self.cards.append(
                Card(card=card, isBack=False, isDeckMenu=True,
                     isMenuDeckSelected=card in self.playerDeck)
            )

        self.all_sprites_list.add(self.cards)
        self.breaks = list(range(1, math.ceil(len(cards) / 5)))

    def updateCardsPos(self):
        for i in range(len(self.cards)):
            self.cards[i].rect.x = self.playerCardPos[0] + (self.column * 264)
            self.cards[i].rect.y = self.playerCardPos[1] + \
                ((self.row + self.scroll) * 308)
            self.column += 1
            if (i + 1) / 5 in self.breaks:
                self.row += 1
                self.column = 0

    def render_self(self):
        self.run_display = True
        self.updateCardsPos()
        self.button = Button(
            self.game.window,
            1100,
            820,
            100,
            40,
            text="Save",
            fontSize=30,
            margin=20,
            radius=8,
            onClick=lambda: saveDeckOnDisk(self.playerDeck),
        )
        clock = pygame.time.Clock()
        while self.run_display:
            self.check_input()
            events = pygame.event.get()
            self.game.window.fill(self.game.BLACK)
            self.all_sprites_list.update()
            self.all_sprites_list.draw(self.game.window)
            pygame_widgets.update(events)
            self.game.draw_text(
                "Monte seu deck clicando nas cartas que deseja", 40, self.game.DISPLAY_W / 2, 40)
            # self.game.window.scroll(0, 80)

            self.blit_screen()
            clock.tick(30)

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_screen.run_display = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [
                        s for s in self.all_sprites_list if s.rect.collidepoint(pos)]
                    if len(clicked_sprites) > 0:
                        clicked_sprites[0].setSelectedOnDeckMenu()
                        if clicked_sprites[0].menuDeckSelected:
                            self.playerDeck.append(clicked_sprites[0].card)
                        else:
                            self.playerDeck.remove(clicked_sprites[0].card)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == -1 and self.scroll > -self.breaks[-2]:
                    self.scroll -= 1
                if event.y == 1 and self.scroll < 0:
                    self.scroll += 1
                self.row = 0
                self.column = 0
                self.updateCardsPos()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    self.game.goToMenuScreen()
                if event.key == pygame.K_DOWN:
                    print(event)
                if event.key == pygame.K_UP:
                    print(event)


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.game.goToMenuScreen()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_screen = self.game.main_menu
                self.run_display = False
            self.game.window.fill(self.game.BLACK)
            self.game.draw_text(
                "Credits", 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text("Made by master of gamblers", 15,
                                self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10, 'magic')
            self.blit_screen()
