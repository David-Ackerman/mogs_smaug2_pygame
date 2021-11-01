import pygame
from pygame.locals import *
import random
from components.card import Card
from sys import exit
from interfaces.card_model import Deck


class Player:
    def __init__(self, game, playerDeck: list[Deck]):
        self.step = 0
        self.playerDeck = playerDeck[:]
        self.handCards = []
        myCards = []
        for i in range(4):
            drawnedCard = random.choices(playerDeck, k=1)[0]
            myCards.append(drawnedCard)
            playerDeck.remove(drawnedCard)
        self.all_sprites_list = pygame.sprite.Group()
        self.playerCardpos = [410, 720 - 150]
        for i in myCards:
            self.handCards.append(Card(i, False, False))
        for i in range(len(self.handCards)):
            self.handCards[i].rect.x = self.playerCardpos[0] + (i * 120)
            self.handCards[i].rect.y = self.playerCardpos[1]
        self.all_sprites_list.add(self.handCards)
        self.clock = pygame.time.Clock()
        self.game = game
        self.BOARD_BG = pygame.image.load("assets/duelBoard.png")
        self.CARD_HAND = pygame.image.load("assets/cardHand.png")
        self.SIDE_DETAILS = pygame.image.load("assets/sideDetails.png")
        # self.BOARD_BG = pygame.transform.scale(self.BOARD_BG, (self.game.DISPLAY_W, self.game.DISPLAY_H))

    def blit_screen(self, game, player):
        if not (game.connected()):
            font = pygame.font.SysFont("comicsans", 70)
            text = font.render("Waiting for Player...", True, (255, 0, 0))
            self.game.window.blit(
                text, (self.game.DISPLAY_W / 2 - text.get_width() / 2,
                       self.game.DISPLAY_H / 2 - text.get_height() / 2)
            )
        else:
            self.game.window.blit(self.SIDE_DETAILS, (0, 0))
            self.game.window.blit(
                self.CARD_HAND, (400, self.game.DISPLAY_H - 160))
            self.game.window.blit(self.BOARD_BG, (400, 0))
        pygame.display.update()
        self.game.reset_keys()

    def render_self(self):
        self.run_display = True

        while self.run_display:
            self.clock.tick(30)
            self.blit_screen(self.duel)
            self.game.check_events()
            if self.game.START_KEY:
                self.run_display = False
            self.all_sprites_list.update()
            self.all_sprites_list.draw(self.game.window)
            pygame.display.flip()

            # Number of frames per secong e.g. 60
