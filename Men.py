import pygame
import Render_functions
from coefficients import *
import random
import Spell
import math


class Men():
    def __init__(self, name, cor, attack=1, skills=(1, 1, 1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=(None, None)): # "White_doc_robe.png"
    # Основные параметры персонажа
        self.name = name                        # Имя
        self.cor = cor                          # Координаты
        self.speed = 5                          # Скорость передвижения
        self.body = {                           # Изображения частей тела персонажей по умолчанию
                "head": Render_functions.load_image(body[1], alpha_cannel="True"),                  # Голова
                "body": Render_functions.load_image(body[0], alpha_cannel="True"),                  # Тело
        }
        self.gear = {                           # Снаряжение
                "Outerwear": Render_functions.load_image(gear[0], alpha_cannel="True"),    # Куртка\Костюм
                "Wearpon"  : Render_functions.load_image(gear[1], alpha_cannel="True")    # Оружие
        }
        self.skills = {                         # Навыки
                "magic"     :skills[0],                                                     # Магия
                "strength"  :skills[1],                                                     # Сила
                "shooting"  :skills[2]                                                      # Стрельба
        }
        self.animations = ()
        self.animations_update(body, gear)
        self.spells = spelllist                         # Заклинания
        self.max_healf = self.skills["strength"]*10     # Максимальные очки здоровья
        self.healf = self.skills["strength"]*10         # Текущие очки здоровья
        self.max_manna = self.skills["magic"]*10        # Максимальные очки манны
        self.manna = self.skills["magic"]*10            # Текущие очки манны
        self.action_points = 15                         # Очки действий
        self.dead = False                               # Мертв ли персонаж

    # Технические заморочки
        self.coofs = {                          # Коэффициенты (стоимость движения)
            "stepwise_move": STEPWISE_MOVE,                                                 # Движение на клетку
            "stepwise_hand_to_hand": STEPWISE_HAND_TO_HAND                                  # Удар в рукопашную
        }
        self.path = ()                          # Путь, по которому идет персонаж
        self.rotate = 0                         # Угол, на который повернут персонаж
        self.move_progress = [0, 0]             # Помогает отобразить процесс перехода с одной клетки на другую
        self.anim_speed = 25                    # Скорость смены кадров в миллисекундах
        self.anim_part = None
        self.anim_num = None
        self.anim_stage = 0
        self.anim_start= False
        self.worktime = 0                       # Кол-во миллисекунд с последней смены кадра
        self.ren_img = None                     # Картинка, которая отображается на экране
        self.ren_img = self.img_designer()
        self.stepwise_mod = False               # Включает/Выключает пошаговый режим
        self.last_stop = None                   # Место, где персонажа в последний раз остановили методом stop
        self.attack_distance = attack           # Дальность, на которой можно атаковать (1 клетка по умолчанию)
        self.attackfield_update()               # Область атаки в виде Rect'а
        self.target = None                      # Цель атаки
        self.whizbangs = []

    def update(self, dt, all_persons):
        if not self.dead:
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
                            for per in all_persons:
                                if self.path:
                                    if self.path[0] == per.cor:
                                        print("KKKKKKKKKKKKKKKKKKKKKKKKK")
                                        self.stop()
                    else:
                        if self.path[0] != self.cor:
                            if type(self.path[0]) == int:
                                self.move(self.path)
                            else:
                                self.move(self.path[0])
                        else:
                            self.path = self.path[1:]
                            for per in all_persons:
                                if self.path:
                                    if self.path[0] == per.cor:
                                        print("KKKKKKKKKKKKKKKKKKKKKKKKK")
                                        self.stop()
                elif self.target:
                    self.attackfield_update()
                    self.hit()
                self.ren_img = self.img_designer()
                for w in self.whizbangs:
                    w.update()

    def move(self, new_cor):
        """
                Двигает персонажа с тайла на тайл и отображает процесс
        """
        if new_cor[0] > self.cor[0]:        # Вправо
            if self.look_direction(new_cor):
                self.move_progress[0] += self.speed
                if self.move_progress[0] >= 100:
                    self.move_progress[0] = 0
                    self.cor = new_cor
        elif new_cor[0] < self.cor[0]:        # Влево
            if self.look_direction(new_cor):
                self.move_progress[0] -= self.speed
                if self.move_progress[0] <= -100:
                    self.move_progress[0] = 0
                    self.cor = new_cor
        elif new_cor[1] > self.cor[1]:        # Вниз
            if self.look_direction(new_cor):
                self.move_progress[1] += self.speed
                if self.move_progress[1] >= 100:
                    self.move_progress[1] = 0
                    self.cor = new_cor
        elif new_cor[1] < self.cor[1]:        # Вверх
            if self.look_direction(new_cor):
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

    def hit(self):
        """
                Поворачивает персонажа в сторону цели и бьёт её
        """
        if self.attack_field.collidepoint(self.target.cor[0], self.target.cor[1]):
            if self.look_direction(self.target.cor):
                if self.gear["Wearpon"]:
                    if type(self.gear["Wearpon"]) == Spell.Spell:
                        if self.use_action_points(self.gear["Wearpon"].action_points):
                            self.gear["Wearpon"].apply(self.target, self.cor, self.whizbangs)
                else:
                    damage = self.skills["strength"]
                    cost = self.coofs["stepwise_hand_to_hand"]
                    if self.use_action_points(cost):
                        self.target.hurt(damage)
                        self.anim_part = 0
                        self.anim_num = 0
                        self.anim_start = True
                self.target = None

    def set_wearpon(self, w):
        """
                Смена оружия на новое (или приготовить кулаки, если его нет)
        """
        self.gear["Wearpon"] = w
        if w:
            self.attack_distance = w.distance
        else:
            self.attack_distance = 1
        self.attackfield_update()

    def set_target(self, target):
        self.target = target

    def hurt(self, damage):
        """
                Получение урона
        """
        if random.randint(1, 100) > 10:
            self.healf -= damage
        if self.healf <= 0:
            self.healf = 0
            self.dead = True

    def attackfield_update(self):
        """
                Обновляет область, по которой персонаж может бить
        """
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

    def look_direction(self, cor):
        """
                Рассчитывает угол поворота персонажа, чтобы он смотрел на определенный тайл
        """
        x1 = cor[0]-self.cor[0]
        y1 = cor[1]-self.cor[1]
        x2 = 0
        y2 = -1
        a = int(math.acos((x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2)))*180/3.14)
        if cor[0]-self.cor[0] > 0:
            a = -a + 360
        if self.rotate != a:
            self.img_rotate(a)
        else:
            return True

    def animations_update(self, body, gear):
        self.animations = [[[]],
                           [[]]
                            ]
        if gear[0]:
            pass
        else:
            self.animations[0][0] =  Render_functions.load_image(body[0][:-4]+"_a_punch1.png", alpha_cannel="True")

    def play_anim(self):
        a = self.animations[self.anim_part][self.anim_num]
        if type(a) == list:
            pass
        elif self.anim_stage < 1:
            if type(a) == list:
                pass
            else:
                return a
            self.anim_stage += 1
        else:
            self.anim_start = False
            self.anim_stage = 0

    def img_rotate(self, value, angle=10):
        """
                Поворачивает картинку в сторону значения угла value на angle градусов. 0 градусов - вверх
        """
        a = value
        value -= self.rotate
        if value >= 360:
            value -= 360
        elif value < 0:
            value += 360
        if value <= 180:
            if value < 10:
                self.rotate = a
            else:
                self.rotate += angle
        else:
            if value < 10:
                self.rotate = a
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
        print(self.rotate)
        if self.anim_start:
            self.play_anim()
        main_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        main_img.blit(img, (main_img.get_width()/2-img.get_width()/2, main_img.get_height()/2-img.get_height()/2))
        return main_img

    def render(self, screen):
        screen.blit(self.ren_img, (self.cor[0]*100+self.move_progress[0], self.cor[1]*100+self.move_progress[1]))
        for w in self.whizbangs:
            w.render(screen)