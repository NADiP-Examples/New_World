import pygame
import Render_functions
from coefficients import *
import random


class Men():
    def __init__(self, name, cor, attack=1):
    # Основные параметры персонажа
        self.name = name                        # Имя
        self.cor = cor                          # Координаты
        self.speed = 5                          # Скорость передвижения
        self.body = {                           # Изображения частей тела персонажей по умолчанию
                "head": Render_functions.load_image("Head_1.png", alpha_cannel="True"),                 # Голова
                "body": Render_functions.load_image("Body_1.png", alpha_cannel="True")                  # Тело
        }
        self.gear = {                           # Снаряжение
                "Outerwear": Render_functions.load_image("White_doc_robe.png", alpha_cannel="True"),    # Куртка\Костюм
                "Wearpon"  : None                                                                       # Оружие
        }
        self.skills = {                         # Навыки
                "magic"     :1,                                                             # Магия
                "strength"  :1,                                                             # Сила
                "shooting"  :1                                                              # Стрельба
        }
        self.coofs = {                          # Коэффициенты (стоимость движения)
            "stepwise_move": STEPWISE_MOVE,                                                 # Движение на клетку
            "stepwise_hand_to_hand": STEPWISE_HAND_TO_HAND                                  # Удар в рукопашную
        }
        self.healf = 10                         # Очки здоровья
        self.manna = self.skills["magic"]*10    # Очки манны
        self.action_points = 15                 # Очки действий

    # Технические заморочки
        self.path = ()                          # Путь, по которому идет персонаж
        self.rotate = 0                         # Угол, на который повернут персонаж
        self.move_progress = [0, 0]             # Помогает отобразить процесс перехода с одной клетки на другую
        self.anim_speed = 25                    # Скорость смены кадров в миллисекундах
        self.worktime = 0                       # Кол-во миллисекунд с последней смены кадра
        self.ren_img = None                     # Картинка, которая отображается на экране
        self.stepwise_mod = False               # Включает/Выключает пошаговый режим
        self.last_stop = None                   # Место, где персонажа в последний раз остановили методом stop
        self.attack_distance = attack           # Дальность, на которой можно атаковать (1 клетка по умолчанию)
        self.attackfield_update()               # Область атаки в виде Rect'а

    def update(self, dt):
        self.worktime += dt
        if not self.stepwise_mod:
            if self.action_points < 15:
                self.action_points += 1
        if self.worktime >= self.anim_speed:
            self.worktime -= self.anim_speed
            if self.path:
                if self.stepwise_mod:
                    if self.path[0] != self.cor:
                        if self.action_points - self.coofs['stepwise_move'] < 0:
                            self.stop()
                        else:
                            if type(self.path[0]) == int:
                                self.move(self.path)
                            else:
                                self.move(self.path[0])
                    else:
                        self.path = self.path[1:]
                        self.use_action_points(self.coofs['stepwise_move'])
                else:
                    if self.path[0] != self.cor:
                        if type(self.path[0]) == int:
                            self.move(self.path)
                        else:
                            self.move(self.path[0])
                    else:
                        self.path = self.path[1:]

        self.ren_img = self.img_designer()

    def move(self, new_cor):
        """
                Двигает персонажа с тайла на тайл и отображает процесс
        """
        if new_cor[0] > self.cor[0]:        # Вправо
            if self.rotate != 270:
                self.img_rotate(270)
            else:
                self.move_progress[0] += self.speed
                if self.move_progress[0] >= 100:
                    self.move_progress[0] = 0
                    self.cor = new_cor
        elif new_cor[0] < self.cor[0]:        # Влево
            if self.rotate != 90:
                self.img_rotate(90)
            else:
                self.move_progress[0] -= self.speed
                if self.move_progress[0] <= -100:
                    self.move_progress[0] = 0
                    self.cor = new_cor
        elif new_cor[1] > self.cor[1]:        # Вниз
            if self.rotate != 180:
                self.img_rotate(180)
            else:
                self.move_progress[1] += self.speed
                if self.move_progress[1] >= 100:
                    self.move_progress[1] = 0
                    self.cor = new_cor
        elif new_cor[1] < self.cor[1]:        # Вверх
            if self.rotate != 0:
                self.img_rotate(0)
            else:
                self.move_progress[1] -= self.speed
                if self.move_progress[1] <= -100:
                    self.move_progress[1] = 0
                    self.cor = new_cor

    def stop(self):
        """
                Остановить персонажа
        """
        if self.path != self.last_stop:
            self.last_stop = self.path[0]
            self.path = None

    def change_mod(self):
        """
                Включает/выключает пошаговый бой
        """
        self.stepwise_mod = not self.stepwise_mod

    def use_action_points(self, cost):
        """
                Отнять cost очков действий, если при этом их кол-во не станет меньше нуля
        """
        if self.action_points >= cost:
            self.action_points -= cost
            return True
        else:
            return False

    def hit(self, target):
        if self.gear["Wearpon"]:
            pass
        else:
            damage = self.skills["strength"]
            cost = self.coofs["stepwise_hand_to_hand"]
        if self.use_action_points(cost):
            target.hurt(damage)

    def hurt(self, damage):
        if random.randint(1, 100) > 10:
            self.healf -= damage

    def attackfield_update(self):
        self.attack_field = pygame.Rect(self.cor[0]-self.attack_distance, self.cor[1]-self.attack_distance, self.attack_distance*2+1, self.attack_distance*2+1)

    def set_path(self, path):
        """
                Устанавливает путь
        """
        if path != -1:
            if not self.path:
                self.path = path
            elif type(self.path[0]) == int:  # fixme! Жуткий ход. Поправить.
                print(self.path)
                self.path = path
                print(self.path)

    def img_rotate(self, value, angle=10):
        """
                Поворачивает картинку в сторону значения угла value на angle градусов. 0 градусов - вверх
        """
        value -= self.rotate
        if value >= 360:
            value -= 360
        elif value < 0:
            value += 360
        if value <= 180:
            self.rotate += angle
        else:
            self.rotate -= angle
        if self.rotate >= 360:
            self.rotate -= 360
        elif self.rotate < 0:
            self.rotate += 360

    def img_designer(self):
        """
                Собирает картинку из частей, поворачивает на нужный угол,
                вклеивает на поверхность 100х100 пикселей (размер тайла)
        """
        if self.gear["Outerwear"]:
            body = self.gear["Outerwear"]
        else:
            body = self.body["body"]
        head = self.body["head"]
        img = pygame.Surface((body.get_width(), int(head.get_height()/2+body.get_height())), pygame.SRCALPHA)
        img.blit(body, (0, img.get_height()-body.get_height()))
        img.blit(head, (img.get_width()/2-head.get_width()/2, 0))
        img = pygame.transform.rotate(img, self.rotate)
        main_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        main_img.blit(img, (main_img.get_width()/2-img.get_width()/2, main_img.get_height()/2-img.get_height()/2))
        return main_img

    def render(self, screen):
        screen.blit(self.ren_img, (self.cor[0]*100+self.move_progress[0], self.cor[1]*100+self.move_progress[1]))