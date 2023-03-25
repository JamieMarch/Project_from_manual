import sys
import pygame
from random import randint
from settings import Settings
from ship import Ship
from additional_quest import Mario
from bullet import Bullet
from alien import Alien
from background_stars import Stars
# from raindrop import Raindrop
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''Класс для управления ресурсами и поведением игры.'''

    def __init__(self):
        '''Инциализирует игру и создаёт игровые ресурсы'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((2560, 1440))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height, ))
        pygame.display.set_caption("Alien Invasion")
        #Создание экземпляра для хранения игровой статистики и панели результатов
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        # self.rain = pygame.sprite.Group()

        self._create_fleet()
        self.additional_quest = Mario(self)
        self._create_stars()
        # self._create_raindrop()
        '''Назначение цвета фона'''
        self.bg_color = self.settings.bg_color
        #Создание кнопки Play
        self.play_button = Button(self, "Play")



    def run_game(self):
        '''Запуск основного цикла игры'''
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            # self._update_rain()
            self._update_screen()
            #При каждом проходе кцикла перерисовывается экран
    # Отслеживание событий клавиатуры и мыши

    def _check_events(self):
            '''Обрабатывает нажатия клавиш и события мыши'''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Запускает новую игру при нажатии кнопки Play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:

            #Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #Сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            #Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            #Создадим нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            #Указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        '''Реагирует на нажатие клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        '''Реагирует на отпускание клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        '''Создание нового снаряда и включение его в группу bullets'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _update_screen(self):
            '''Обновляет изображение на экране и отображает новый экран.'''
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            self.additional_quest.bltime()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.sb.show_score()
            self.stars.draw(self.screen)
            # self.rain.draw(self.screen)
            #Кнопка Play отображается в том случае, если игра неактивна
            if not self.stats.game_active:
                self.play_button.draw_button()
    # Отображение последнего прорисованного экрана
            pygame.display.flip()
    def _create_fleet(self):
        '''Создание флота вторжения'''
        #Создание пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        '''Определяет количество рядов, помещающихсчя на экране'''
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Создание флота для вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 1.25 * alien.rect.height * row_number
        self.aliens.add(alien)
    def _check_fleet_edges(self):
        '''Реагирует на достижение пришельцем края экрана'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        '''Опускает весь флот и меняет направление флота'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _update_bullets(self):
        '''Обновляет позиции снарядов и уничтожает старые снаряды'''
        #Обновление позиций снарядов
        self.bullets.update()

        #Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        # Проверка попаданий в пришельцев
        # При обнаружении попадания удалить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
        #Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        '''Обновляет позиции всех пришельцев во флоте'''
        self._check_fleet_edges()
        self.aliens.update()
        #Проверка коллизий "пришелец-корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Проверить, добрались ли пришельцы до нижнего экрана
        self._check_aliens_bottom()
    def _ship_hit(self):
        '''Обрабатывает столкновение корабля с пришельцем'''
        if self.stats.ships_left > 0:
            #Уменьшение ships_left и обновление панели счёта
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            #Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
    def _create_stars(self):
        star = Stars(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width - int(2 * star_width)
        number_columns = available_space_x // int(2.5 * star_width)

        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - int(2 * star_height) - ship_height)
        number_rows = available_space_y // int(3 * star_height)

        for row_number in range(number_rows):
            for column_number in range(number_columns):
                self._create_star(column_number, row_number)
    def _create_star(self, column_number, row_number):
        star = Stars(self)
        star_width, star_height = star.rect.size
        star.x = star_width + 9 * star_width * column_number + randint(-1000, 1000)
        star.rect.x = star.x
        star.y = star_height + 9 * star_height * row_number + randint(-1000, 1000)
        star.rect.y = star.y
        self.stars.add(star)
    # def _create_raindrop(self):
    '''Функция для создания дождевой капли'''
    #     rain = Raindrop(self)
    #     rain_width, rain_height = rain.rect.size
    #     available_space_x = self.settings.screen_width - int(2 * rain_width)
    #     number_columns = available_space_x // int(3 * rain_width)
    #
    #     ship_height = self.ship.rect.height
    #     available_space_y = (self.settings.screen_height - int(2 * rain_height) - ship_height)
    #     number_rows = available_space_y // int(3 * rain_height)
    #     for row_number in range(number_rows):
    #         for column_number in range(number_columns):
    #             self._create_rain(column_number, row_number)
    # def _create_rain(self, column_number, row_number):
    '''Функция для создания дождя'''
    #     rain = Raindrop(self)
    #     rain_width, rain_height = rain.rect.size
    #     rain.x = rain_width + 6 * rain_width * column_number + randint(-500, 500)
    #     rain.rect.x = rain.x
    #     rain.y = rain_height + 6 * rain_height * row_number + randint(-500, 500)
    #     rain.rect.y = rain.y
    #     self.rain.add(rain)
    # def _update_rain(self):
    #     self.rain.update()

        # for raindrop in self.rain.copy():
        #     if raindrop.rect.bottom <= 0:
        #         self.rain.remove(raindrop)
        #         self._create_rain()
    def _check_aliens_bottom(self):
        '''Проверяет, добрались ли пришельцы до нижнего края'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Происходит то же, что при столкновении с кораблём
                self._ship_hit()
                break
if __name__ == '__main__':
    '''Создание экземпляра и запуск игры'''
    ai = AlienInvasion()
    ai.run_game()