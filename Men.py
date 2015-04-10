import pygame
import Render_functions


class Men():
    def __init__(self, name, cor):
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
                    }
        self.skills = {                         # Навыки
                "magic"     :1,                                                        # Магия
                "strength"  :1,                                                        # Сила
                "shooting"  :1                                                         # Стрельба
                    }
        self.healf = 100                        # Очки здоровья
        self.manna = self.skills["magic"]*10    # Очки манны
        self.action_points = 15                 # Очки действий
        self.stepwise_mod = False

    # Технические заморочки
        self.path = ()                          # Путь, по которому идет персонаж
        self.rotate = 0                         # Угол, на который повернут персонаж
        self.move_progress = [0, 0]              # Помогает отобразить процесс перехода с одной клетки на другую
        self.anim_speed = 25                    # Скорость смены кадров в миллисекундах
        self.worktime = 0                       # Кол-во миллисекунд с последней смены кадра
        self.ren_img = None                     # Картинка, которая отображается на экране

    def update(self, dt):
        self.worktime += dt
        if self.worktime >= self.anim_speed:
            self.worktime -= self.anim_speed
            if self.path:
                if self.path[0] != self.cor:
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

    def set_path(self, path):
        """
                Устанавливает путь
        """
        if not self.path and path != -1:
            self.path = path

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

    def change_mod(self):
        """
                Включает/выключает пошаговый бой
        """
        self.stepwise_mod = not self.stepwise_mod

    def render(self, screen):
        screen.blit(self.ren_img, (self.cor[0]*100+self.move_progress[0], self.cor[1]*100+self.move_progress[1]))