import typing
import pygame
import random

musics = typing.Literal['click', 'select',
                        'viewCardInfo', 'endGame', 'simpleClick']

SONGS = ["assets/sounds/Bourree-JoelCummins.mp3",
         "assets/sounds/NorthOaklandExtasy-SquaddaB.mp3",
         "assets/sounds/Bourree-JoelCummins.mp3",
         "assets/sounds/YonderHillandDale-AaronKenny.mp3",
         "assets/sounds/StellarWind-UnicornHeads.mp3",
         ]


class Sound():
    def __init__(self, vol: float):
        self.sounds = pygame.mixer.Channel(0)
        self.music = pygame.mixer.Channel(1)
        self.vol = vol
        self.songNumber = 0
        self.sounds.set_volume(self.vol)
        self.music.set_volume(self.vol/5)
        self.soundsFx = {
            'click': (pygame.mixer.Sound('assets/sounds/select-click.wav'), 1),
            'select': (pygame.mixer.Sound('assets/sounds/quick-positive-video-game-notification-interface.wav'), 1),
            'viewCardInfo': (pygame.mixer.Sound('assets/sounds/retro-arcade-casino-notification.wav'), 1),
            'endGame': (pygame.mixer.Sound('assets/sounds/quick-win-video-game-notification.wav'), 1),
            'simpleClick': (pygame.mixer.Sound('assets/sounds/game-click.wav'), 1),
        }
        random.shuffle(SONGS)

    def updateVol(self, vol: float):
        self.vol = vol
        self.sounds.set_volume(self.vol)
        self.music.set_volume(self.vol/5)

    def playSound(self, music: musics):
        self.sounds.play(self.soundsFx[music][0], 0)

    def playSongs(self):
        sound = pygame.mixer.Sound(SONGS[self.songNumber])
        self.music.play(sound, 0, fade_ms=20)

    def continueSongs(self):
        if not (self.music.get_busy()):
            self.songNumber += 1
            if self.songNumber > len(SONGS):
                self.songNumber = 0
            sound = pygame.mixer.Sound(SONGS[self.songNumber])
            self.music.play(sound, 0, fade_ms=20)
