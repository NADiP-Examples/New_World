import math
import pygame
import Render_functions

class Whizbang:
    def __init__(self, start, finish, img, speed=10):
        self.start = start
        self.finish = finish
        self.pos = [self.start[0]*100+50, self.start[1]*100+50]
        self.pre_x = self.pos[0]
        self.angle = self.find_angle()
        self.img = self.create_img(img)
        self.speed = self.set_speed_vector(speed)
        self.end = False

    def update(self):
        self.pre_x = self.pos[0]
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if (self.finish[0]*100 >= self.pre_x and self.finish[0]*100 <= self.pos[0]) or (self.finish[0]*100 <= self.pre_x and self.finish[0]*100 >= self.pos[0]):
            self.end = True

    def create_img(self, img):
        """
                Рассчитывает угол поворота персонажа, чтобы он смотрел на определенный тайл
        """
        img = Render_functions.load_image(img, alpha_cannel="True")
        return pygame.transform.rotate(img, self.angle)

    def find_angle(self):
        x1 = self.finish[0]-self.start[0]
        y1 = self.finish[1]-self.start[1]
        x2 = 0
        y2 = -1
        a = int(math.acos((x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2)))*180/3.14)
        if self.finish[0]-self.start[0] > 0:
            a = -a + 360
        return a

    def set_speed_vector(self, speed):
        x = 0
        y = -speed
        angle = math.radians(-self.angle)
        x = x * math.cos(angle) - y * math.sin(angle)
        y = x * math.sin(angle) + y * math.cos(angle)
        self.x, self.y = x, y
        return (x,y)

    def render(self, screen):
        screen.blit(self.img, self.pos)