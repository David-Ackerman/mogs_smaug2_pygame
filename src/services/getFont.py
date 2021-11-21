import os  # Remember to import it in order to use os.path.join().
import pygame

fonts = {
    'nunito': 'NunitoSans-Regular.ttf',
    'nunito-bold': 'NunitoSans-Bold.ttf',
    'nunito-italic': 'NunitoSans-Italic.ttf',
    'nunito-l': 'NunitoSans-Light.ttf',
    'nunito-l-italic': 'NunitoSans-LightItalic.ttf',
    'magic': 'MagicSparkle.ttf'
}


def loadCustomFont(size: int, fontType: str = 'nunito'):
    """
    A function to load a custom font from a file.
    """
    fullname = os.path.join('assets', 'fonts', fonts[fontType])
    f = pygame.font.Font(fullname, size)
    return f
