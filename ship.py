import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Класс для управления кораблём'''
    def __init__(self, ai_game):
        '''Инициирует корабль и задаёт его первоначальную позицию'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('C:/Users/Jamie/PycharmProjects/Alien Invasion/images/ship.bmp')
        self.rect = self.image.get_rect()
        #Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.bottom = self.screen_rect.bottom
        #Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Флаг перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    def update(self):
        '''Обновляет позицию корабля с учётом флагов'''
        #Обновляется атрибут x, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
            self.rect.x += 1
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            self.rect.x -= 1
        if self.moving_up and self.rect.y > 0:
            self.y -= self.settings.ship_speed
            self.rect.y -= 1
        if self.moving_down and self.rect.y < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
            self.rect.y += 1
    def blitme(self):
        '''Рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)