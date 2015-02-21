import pygame
from pygame import *

from Old_F.Render_functions import *


pygame.init() # Из-за какого-то космического недоразумения, которое и породило pygame, без этой строки класс не может при инициализации прочесть звук.
class Button:
    def __init__(self, text, cor, action, arg = False, sin= False, st=pygame.mixer.Sound('Sounds/2.ogg'), color=(255,152,0), font=None, pt=27): # Текст кнопки, координаты, функция, звук при наведении, звук при переходе
        self.out = load_text(text,pt=pt)
        self.into = load_text(text,pt=pt,color=color)
        self.rect = load_text(text,pt=pt).get_rect()
        self.cor = tuple(cor)
        self.mod = "out"
        self.action = action
        self.arguments = arg
        self.s_in = sin
        self.s_tar = st
        self.rect = self.out.get_rect()
        self.rect.move_ip(cor)

    def events(self, e): # Действие, список в который кнопка кидает изменения, доп. цель с возвращением значения.
        if self.rect.collidepoint(e.pos):
            if self.s_in:
                    self.s_in.play()
            self.mod = "in"
            if e.type == MOUSEBUTTONDOWN:
                if self.s_tar:
                    self.s_tar.play()
                if self.arguments:
                    self.action(self.arguments)
                else:
                    self.action()
        else:
            self.mod = "out"

    def render(self, screen):
        if self.mod == "out":
            screen.blit(self.out, self.cor)
        elif self.mod == "in":
             screen.blit(self.into, self.cor)



class Button_Flag():
    def __init__(self, images, action, pos, arg = False, sin= False, st=pygame.mixer.Sound('Sounds/2.ogg'), size = False):
        self.imgs = images
        if size:
            for img in self.imgs:
                img = pygame.transform.scale(img,size)
        self.rect = self.imgs[0].get_rect()
        self.rect.move_ip(pos)
        self.s_in = sin
        self.s_tar = st
        self.action = action
        self.arguments = arg        # Кортеж из двух значений, первое - аргументы, передаваемые при нажатии кнопки, вторые - при отжатии
        self.mod = "out"
        self.stat = False           # Показывает, нажата кнопка или нет

    def events(self, e): # Действие, список в который кнопка кидает изменения, доп. цель с возвращением значения.
        if self.rect.collidepoint(e.pos):
            if self.s_in:
                    self.s_in.play()
            self.mod = "in"
            if e.type == MOUSEBUTTONUP:
                if self.s_tar:
                    self.s_tar.play()
                self.stat = not self.stat
                if self.stat:
                    self.action(self.arguments[0])
                else:
                    self.action(self.arguments[1])
        else:
            self.mod = "out"

    def render(self, screen):
        if self.stat:
            screen.blit(self.imgs[0], (0,0))
        else:
             screen.blit(self.imgs[0], (0,0))

# class Checkbox():
#     def __init__(self):