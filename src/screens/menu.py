import pygame
import math
import sys
from src.components.button import ButtonDuels
from src.services.getFont import loadCustomFont
from src.components.buttonImg import ButtonImage
from src.components.card import Card
from src.interfaces.card_model import Deck
from src.interfaces.cards import cards
from src.services.saveDeck import saveDeckOnDisk

vols = {
    '1': 0.03,
    '2': 0.1,
    '3': 0.3,
    '4': 0.6,
    '5': 0.9,
}


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


class EndDuel(Menu):
    def __init__(self, game, won: bool = False):
        Menu.__init__(self, game)
        self.won = won

    def render_self(self):
        self.run_display = True
        while self.run_display:
            self.game.window.fill(self.game.BLACK)
            if self.won:
                self.game.draw_text(
                    "Vitoria !!", 80, self.mid_w, self.mid_h - 180)
                self.game.draw_text(
                    "Parabens, ao voltar ao menu você poderá buscar outras partidas", 40, self.mid_w, self.mid_h)
            else:
                self.game.draw_text(
                    "Derrota !!", 80, self.mid_w, self.mid_h - 180)
                self.game.draw_text(
                    "infelizmente você foi derrotado, jogue outras partidas para evoluir mais", 40, self.mid_w, self.mid_h)
            self.blit_screen()
            pygame.time.wait(2000)
            self.run_display = False
        self.game.goToMenuScreen()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80
        self.deckx, self.decky = self.mid_w, self.mid_h + 130
        self.helpx, self.helpy = self.mid_w, self.mid_h + 180
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 230
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
            self.game.draw_text("Help", 40, self.helpx, self.helpy)
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
                    self.helpx + self.offset, self.helpy)
                self.state = "Help"
            elif self.state == "Help":
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
                    self.helpx + self.offset, self.helpy)
                self.state = "Help"
            elif self.state == "Help":
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
            elif self.state == "Help":
                self.game.curr_screen = self.game.help_menu
            elif self.state == "Credits":
                self.game.curr_screen = self.game.credits_menu

            self.run_display = False
            self.game.curr_screen.render_self()


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.userx, self.usery = self.mid_w - 120, self.mid_h + 30
        self.volx, self.voly = self.mid_w - 120, self.mid_h + 100
        self.buttonsY = self.voly - 10
        self.buttonsx = self.volx + 70
        self.base_font = loadCustomFont(25)
        self.userText = self.game.userName
        self.volume = self.game.volume
        self.btns_vol = [ButtonDuels('1', self.buttonsx, self.buttonsY, (200, 200, 200), 'rooters', 30, 30, 10, 25, textColor=(20, 20, 20)), ButtonDuels('2', self.buttonsx + 40, self.buttonsY, (200, 200, 200), 'rooters', 30, 30, 10, 25, textColor=(20, 20, 20)),
                         ButtonDuels('3', self.buttonsx + 80, self.buttonsY, (200, 200, 200), 'rooters', 30, 30, 10, 25, textColor=(20, 20, 20)), ButtonDuels('4', self.buttonsx + 120, self.buttonsY, (200, 200, 200), 'rooters', 30, 30, 10, 25, textColor=(20, 20, 20)), ButtonDuels('5', self.buttonsx + 160, self.buttonsY, (200, 200, 200), 'rooters', 30, 30, 10, 25, textColor=(20, 20, 20))]

    def render_self(self):
        self.game.music.stop()
        self.run_display = True
        self.sound = pygame.mixer.Sound('assets/sounds/dramatic.wav')
        self.button = ButtonImage('save', 1100, 820)
        self.input_rect = pygame.Rect(
            self.userx + 74, self.usery - 20, 200, 36)
        color_active = (233, 233, 233)
        color_passive = (150, 150, 150)
        color = color_passive
        self.text_active = False
        while self.run_display:
            self.check_input()
            color = color_active if self.text_active else color_passive
            self.game.window.fill(self.game.BLACK)
            text_surface = self.base_font.render(
                self.userText, True, (255, 255, 255))

            self.game.draw_text(
                "Options", 80, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 80)
            self.game.draw_text(
                "UserName:", 25, self.userx, self.usery, font="nunito")
            self.game.draw_text("Volume: ", 30, self.volx,
                                self.voly, font="nunito")

            self.game.window.blit(
                text_surface, (self.userx + 80, self.usery - 16))
            self.button.draw(self.game.window)
            for btn in self.btns_vol:
                btn.draw(self.game.window)
            pygame.draw.rect(self.game.window,
                             color, self.input_rect, 2)
            self.blit_screen()
        self.game.goToMenuScreen()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    self.text_active = False
                    pos = pygame.mouse.get_pos()
                    if self.button.click(pos):
                        saveDeckOnDisk(self.game.playerDeck, self.userText, {
                                       'vol': self.volume})
                        self.game.userName = self.userText
                        self.game.volume = self.volume
                        self.run_display = False
                        return
                    elif self.input_rect.collidepoint(pos):
                        self.text_active = True
                    else:
                        for vol in self.btns_vol:
                            if vol.click(pos):
                                self.volume = vols[vol.text]
                                self.sound.set_volume(self.volume)
                                self.sound.play(0, 1000)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.goToMenuScreen()
                elif self.text_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.userText = self.userText[:-1]
                    else:
                        if len(self.userText) < 12:
                            self.userText += event.unicode


class DeckMenu(Menu):
    def __init__(self, game, playerDeck: list[Deck]):
        Menu.__init__(self, game)
        self.playerDeck: list[Deck] = playerDeck[:]
        self.cards: list[Deck] = []
        self.row = 0
        self.scroll = 0
        self.column = 0
        self.all_sprites_list = pygame.sprite.Group()
        self.playerCardPos = [20, 100]
        for card in cards:
            self.cards.append(
                Card(card=card, isBack=False, isDeckMenu=True,
                     isSelected=card in self.playerDeck)
            )

        self.all_sprites_list.add(self.cards)
        self.brakValue = math.floor(self.game.WIDTH / 240)
        self.breaks = list(range(1, math.ceil(len(cards) / self.brakValue)))

    def updateCardsPos(self):
        for i in range(len(self.cards)):
            self.cards[i].rect.x = self.playerCardPos[0] + (self.column * 240)
            self.cards[i].rect.y = self.playerCardPos[1] + \
                ((self.row + self.scroll) * 308)
            self.column += 1
            if (i + 1) / self.brakValue in self.breaks:
                self.row += 1
                self.column = 0

    def render_self(self):
        self.run_display = True
        self.updateCardsPos()
        self.button = ButtonImage(
            'save', self.game.WIDTH - 160, self.game.HEIGHT - 80)

        clock = pygame.time.Clock()
        while self.run_display:
            self.check_input()
            self.game.window.fill(self.game.BLACK)
            self.all_sprites_list.update()
            self.all_sprites_list.draw(self.game.window)
            self.button.draw(self.game.window)
            pygame.draw.rect(
                self.game.window, (self.game.BLACK), (0, 0, self.game.WIDTH, 80))
            self.game.draw_text(
                "Monte seu deck clicando nas cartas que deseja", 40, self.game.WIDTH / 2, 40)

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
                    if self.button.click(pos):
                        saveDeckOnDisk(self.playerDeck, self.game.userName, {
                                       'vol': self.game.volume})
                        return
                    clicked_sprites = [
                        s for s in self.all_sprites_list if s.rect.collidepoint(pos)]
                    if len(clicked_sprites) > 0:
                        clicked_sprites[0].setSelectedOnDeckMenu()
                        if clicked_sprites[0].isSelected:
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


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def render_self(self):
        self.run_display = True
        credits = pygame.image.load('assets/creditos.png')
        credits = pygame.transform.scale(credits, (self.game.DISPLAY_W, 500))
        scroll = 0
        clock = pygame.time.Clock()
        while self.run_display:
            clock.tick(30)
            self.game.check_events()
            self.check_input()
            self.game.window.fill(self.game.BLACK)
            self.game.window.blit(
                credits, (0, self.game.DISPLAY_H / 2 - scroll))
            scroll += 2
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.goToMenuScreen()
        elif self.game.START_KEY:
            pass


class HelpMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def render_self(self):
        self.run_display = True
        help = pygame.image.load('assets/help.png')
        help = pygame.transform.scale(
            help, (self.game.DISPLAY_W, self.game.DISPLAY_H))
        clock = pygame.time.Clock()
        while self.run_display:
            clock.tick(30)
            self.game.check_events()
            self.check_input()
            self.game.window.fill(self.game.BLACK)
            self.game.window.blit(
                help, (0, 0))

            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.run_display = False
            self.game.goToMenuScreen()
        elif self.game.START_KEY:
            pass
