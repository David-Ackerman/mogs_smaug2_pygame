import os
import pygame

from src.interfaces.card_model import Fonts

fonts = {
    'nunito': 'NunitoSans-Regular.ttf',
    'nunito-bold': 'NunitoSans-Bold.ttf',
    'nunito-italic': 'NunitoSans-Italic.ttf',
    'nunito-l': 'NunitoSans-Light.ttf',
    'nunito-l-italic': 'NunitoSans-LightItalic.ttf',
    'magic': 'MagicSparkle.ttf',
    'rooters': 'Rooters.ttf',
    'rooters-italic': 'Rooters-Italic.ttf'
}


def loadCustomFont(size: int, fontType: Fonts = 'nunito'):
    """
    A function to load a custom font from a file.
    """
    fullname = os.path.join('assets', 'fonts', fonts[fontType])
    f = pygame.font.Font(fullname, size)
    return f
