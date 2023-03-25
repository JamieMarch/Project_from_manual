import pygame
from pygame.sprite import Sprite

class Raindrop(Sprite):
    '''Класс для создания метеорита на заднем плане'''

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('C:/Users/Jamie/PycharmProjects/Alien Invasion/images/raindrop.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.rect.midbottom = ai_game.ship.rect.midbottom
    def update(self):
        '''Перемещение капель вниз'''
        self.y += self.settings.rain_speed
        self.rect.y = self.y
