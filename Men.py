import pygame
import Render_functions
from coefficients import *
import random
import Spell
import math


class Men():
    def __init__(self, name, cor, attack=1, skills=(1, 1, 1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=(None, None)):# "White_doc_robe.png"
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
            "Wearpon":   Render_functions.load_image(gear[1], alpha_cannel="True")    # Оружие
        }
        self.skills = {                         # Навыки
            "magic":    skills[0],                                                     # Магия
            "strength": skills[1],                                                     # Сила
            "shooting": skills[2]                                                      # Стрельба
        }
        self.animations = {}
        self.animations_update(body, gear)
        self.spells = spelllist                         # Заклинания
        self.effects = []                               # Эффекты, наложеные на персонажа
        self.max_healf = self.skills["strength"]*10     # Максимальные очки здоровья
        self.healf = self.skills["strength"]*10         # Текущие очки здоровья
        self.max_manna = self.skills["magic"]*10        # Максимальные очки манны
        self.manna = self.skills["magic"]*10            # Текущие очки манны
        self.armor = 0                                  # Показатель брони
        self.__update_armor
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
        self.anim_play = False
        self.anim_stage = 0
        self.worktime = 0                       # Кол-во миллисекунд с последней смены кадра
        self.ren_img = None                     # Картинка, которая отображается на экране
        self.ren_img = self.img_designer()
        self.stepwise_mod = False               # Включает/Выключает пошаговый режим
        self.last_stop = None                   # Место, где персонажа в последний раз остановили методом stop
        self.attack_distance = attack           # Дальность, на которой можно атаковать (1 клетка по умолчанию)
        self.attackfield_update()               # Область атаки в виде Rect'а
        self.target = None                      # Цель атаки
        self.whizbangs = []
        self.angle = 0

    def update(self, dt, all_persons):
        if self.dead:
            return
        self.worktime += dt
        if not self.worktime >= self.anim_speed:
            return
        self.worktime -= self.anim_speed
        if not self.stepwise_mod and self.action_points < 15:
            self.action_points += 1
        if self.path:
            for per in all_persons:
                if not per.dead:
                    if self.path[0] == per.cor and self != per:
                        self.stop()
                    elif self.path == per.cor and self != per:
                        self.stop()
        if self.path:
            if self.path[0] != self.cor:
                if self.stepwise_mod and self.action_points - self.coofs['stepwise_move'] < 0:
                    self.stop()
                else:
                    if type(self.path[0]) == int:
                        self.move(self.path)
                    else:
                        self.move(self.path[0])
            else:
                self.path = self.path[1:]
                if self.stepwise_mod:
                    self.use_action_points(self.coofs['stepwise_move'])
        elif self.target:
            self.attackfield_update()
            self.hit()
        self.ren_img = self.img_designer()
        for w in self.whizbangs:
            w.update()
            if w.end:
                self.whizbangs.remove(w)

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
        if not self.attack_field.collidepoint(self.target.cor[0], self.target.cor[1]):
            return
        if not self.look_direction(self.target.cor):
            return
        if self.anim_play == "b_punch":
            return
        if self.gear["Wearpon"]:
            if type(self.gear["Wearpon"]) == Spell.Spell:
                if self.target == self and self.gear["Wearpon"].type != "Defence":
                    self.target = None
                    return
                if self.use_action_points(self.gear["Wearpon"].action_points):
                    self.gear["Wearpon"].apply(self, self.target, self.cor, self.whizbangs)
        else:
            if self.target == self:
                self.target = None
                return
            damage = self.skills["strength"]
            cost = self.coofs["stepwise_hand_to_hand"]
            if self.use_action_points(cost):
                self.target.hurt(damage)
                self.anim_play = "b_punch"
        self.target = None

    def set_wearpon(self, weapon):
        """
                Смена оружия на новое (или приготовить кулаки, если его нет)
        """
        self.gear["Wearpon"] = weapon
        if weapon:
            self.attack_distance = weapon.distance
        else:
            self.attack_distance = 1
        self.attackfield_update()

    def set_target(self, target):
        self.target = target

    def hurt(self, damage):
        """
                Получение урона
        """
        if random.randint(1, 10) > 1:
            damage -= self.armor
            if damage < 0:
                damage = 0
            self.healf -= damage
        if self.healf <= 0:
            self.healf = 0
            self.kill_men()

    def kill_men(self):
        self.dead = True

    def __update_armor(self):
        self.armor = 0

    def check_for_visibility(self, phisic_wallmap, v_segment):
        print(v_segment)
        try:
            k1 = (v_segment[0][1]-v_segment[1][1])/(v_segment[0][0]-v_segment[1][0])
        except:
            k1 = 0
        b1 = v_segment[0][1]-k1*v_segment[0][0]
        for segment in phisic_wallmap:
            print(segment)
            try:
                k2 = (segment[0][1]-segment[1][1])/(segment[0][0]-segment[1][0])
            except:
                k2 = 0
            if k2 != k1:
                b2 = segment[0][1]-k2*segment[0][0]
                try:
                    x = (b2-b1)/(k1-k2)
                except:
                    x = 0
                y = k2*x+b2
                print(x, y)
                if y == k1*x+b1:
                    if not (((x <= v_segment[0][0] and x >= v_segment[1][0]) or (x >= v_segment[0][0] and x <= v_segment[1][0])) and ((y <= v_segment[0][1] and y >= v_segment[1][1]) or (y >= v_segment[0][1] and y <= v_segment[1][1]))):
                        print("000000000000000000000000000000000000")
                        return True

    def attackfield_update(self):
        """
                Обновляет область, по которой персонаж может бить
        """
        self.attack_field = pygame.Rect(self.cor[0]-self.attack_distance, self.cor[1]-self.attack_distance, self.attack_distance*2+1, self.attack_distance*2+1)

    def set_path(self, path):
        """
                Устанавливает путь
        """
        if path == -1:
            return
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
        try:
            a = int(math.acos((x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2)))*180/3.14)
            self.angle = a
        except:
            a = self.angle
        if cor[0]-self.cor[0] > 0:
            a = -a + 360
        if self.rotate != a:
            self.img_rotate(a)
        else:
            return True

    def animations_update(self, body, gear):
        if gear[0]:
            pass
        else:
            foundation = body[0][:-4]
        self.animations = {
            "b_punch" : (Render_functions.load_image(foundation+"_a_punch1.png", alpha_cannel="True"),
                       Render_functions.load_image(foundation+"_a_punch2.png", alpha_cannel="True"),
                       Render_functions.load_image(foundation+"_a_punch3.png", alpha_cannel="True"),
                       Render_functions.load_image(foundation+"_a_punch4.png", alpha_cannel="True"),
                       Render_functions.load_image(foundation+"_a_punch5.png", alpha_cannel="True"))
        }

    def get_anim_frame(self):
        a = self.animations[self.anim_play]
        if self.anim_stage < len(a):
            self.anim_stage += 1
            return a[self.anim_stage-1]
        else:
            self.anim_play = False
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
        body = None
        head = None
        if self.anim_play:
            if "b" in self.anim_play:
                body = self.get_anim_frame()
        if not body:
            if self.gear["Outerwear"]:
                body = self.gear["Outerwear"]
            else:
                body = self.body["body"]
        head = self.body["head"]
        img = pygame.Surface((body.get_width(), int(head.get_height()/2+body.get_height())), pygame.SRCALPHA)
        img.blit(body, (0, img.get_height()-body.get_height()))
        img.blit(head, (img.get_width()/2-head.get_width()/2, img.get_height()/2-head.get_height()/2))
        img = pygame.transform.rotate(img, self.rotate)
        main_img = pygame.Surface((100, 100), pygame.SRCALPHA)
        main_img.blit(img, (main_img.get_width()/2-img.get_width()/2, main_img.get_height()/2-img.get_height()/2))
        return main_img

    def get_coords_on_map(self):
        return self.cor[0]*100+self.move_progress[0], self.cor[1]*100+self.move_progress[1]

    def render(self, screen):
        screen.blit(self.ren_img, self.get_coords_on_map())
        for w in self.whizbangs:
            w.render(screen)