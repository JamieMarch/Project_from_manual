import pygame

class Mario():
    '''Класс для выведения изображение персонажа'''

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('C:/Users/Jamie/PycharmProjects/Alien Invasion/images/Mario.bmp')
        self.rect = self.image.get_rect()

        self.rect.center = self.screen_rect.center

    def bltime(self):

        self.screen.blit(self.image, self.rect)