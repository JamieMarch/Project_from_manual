import pygame
from pygame.sprite import Sprite
class Stars(Sprite):
    '''Класс для выведения изображения звёзд на background'''

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        self.image = pygame.image.load('C:/Users/Jamie/PycharmProjects/Alien Invasion/images/stars.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
