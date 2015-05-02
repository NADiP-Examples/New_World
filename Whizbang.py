import math
import pygame
import Render_functions

class Whizbang:
    def __init__(self, start, finish, img, speed=10):
        self.start = start
        self.finish = finish
        self.img = self.create_img(img)
        self.speed = speed
        self.progress = 0

    def update(self):
        pass

    def create_img(self, img):
        """
                Рассчитывает угол поворота персонажа, чтобы он смотрел на определенный тайл
        """
        img = Render_functions.load_image(img, alpha_cannel="True")
        x1 = self.finish[0]-self.start[0]
        y1 = self.finish[1]-self.start[1]
        x2 = 0
        y2 = -1
        a = int(math.acos((x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2)))*180/3.14)
        if self.finish[0]-self.start[0] > 0:
            a = -a + 360
        print(img, a)
        return pygame.transform.rotate(img, a)

    def render(self, screen):
        screen.blit(self.img, (self.start[0]*100+50, self.start[1]*100+50))