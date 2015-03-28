import pygame
import Render_functions


pygame.init() # Из-за какого-то космического недоразумения, которое и породило pygame, без этой строки класс не может при инициализации прочесть звук.
class Button:
    def __init__(self, text, cor, action, arg = False, sin= False, st=pygame.mixer.Sound('Sounds/2.ogg'), color=(255,152,0), font=None, pt=27): # Текст кнопки, координаты, функция, звук при наведении, звук при переходе
        self.out = Render_functions.load_text(text,pt=pt)
        self.into = Render_functions.load_text(text,pt=pt,color=color)
        self.rect = Render_functions.load_text(text,pt=pt).get_rect()
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
            if e.type == pygame.MOUSEBUTTONDOWN:
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
    def __init__(self, image, action, pos, arg=False, sin=False, st=pygame.mixer.Sound('Sounds/2.ogg'), size=False):
        self.img = image
        if size:
            self.img = pygame.transform.scale(self.img, size)
        self.rect = self.img.get_rect()
        self.rect.move_ip(pos)
        self.cor = pos
        self.sub_imgs = (Render_functions.load_image("Tile-Button-in.png", alpha_cannel="True"),Render_functions.load_image("Tile-Button-down.png", alpha_cannel="True"))
        self.s_in = sin
        self.s_tar = st
        self.action = action
        self.arguments = arg        # Кортеж из двух значений, первое - аргументы, передаваемые при нажатии кнопки, вторые - при отжатии
        self.mod = "out"
        self.stat = False           # Показывает, нажата кнопка или нет
        try:
            self.render_img = pygame.Surface((size))
        except:
            self.render_img = pygame.Surface((100,100))

    def events(self, e): # Действие, список в который кнопка кидает изменения, доп. цель с возвращением значения.
        if self.rect.collidepoint(e.pos):
            if self.s_in:
                    self.s_in.play()
            self.mod = "in"
            if e.type == pygame.MOUSEBUTTONUP:
                if self.s_tar:
                    self.s_tar.play()
                self.stat = not self.stat
                if self.stat:
                    self.action(self.arguments[0])
                else:
                    self.action(self.arguments[1])
                return True
        else:
            self.mod = "out"

    def render(self, screen):
        self.render_img.blit(self.img, (0,0))
        if self.mod == "in":
            self.render_img.blit(self.sub_imgs[0], (0,0))
        if self.stat:
            self.render_img.blit(self.sub_imgs[1], (0,0))
        screen.blit(self.render_img, self.cor)



class Button_Img():
    def __init__(self, imgs, cor, action, arg = False, sin= False, st=pygame.mixer.Sound('Sounds/2.ogg')): # Картинки кнопки, координаты, функция, звук при наведении, звук при переходе
        self.imgs = []
        if type(imgs[1]) != pygame.Surface:
            print("1")
            for img in imgs:
                self.imgs.append(Render_functions.load_image(img, alpha_cannel="True"))
        else:
            self.imgs = imgs
        self.cor = cor
        self.mod = "out"
        self.action = action
        self.arguments = arg
        self.s_in = sin
        self.s_tar = st
        print(self.imgs)
        self.rect = self.imgs[0].get_rect()
        self.rect.move_ip(cor)

    def events(self, e): # Действие, список в который кнопка кидает изменения, доп. цель с возвращением значения.
        if self.rect.collidepoint(e.pos):
            if self.s_in:
                    self.s_in.play()
            self.mod = "in"
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.mod = "down"
            if e.type == pygame.MOUSEBUTTONUP:
                if self.s_tar:
                    self.s_tar.play()
                if self.arguments:
                    self.action(self.arguments)
                else:
                    self.action()
                return True
        else:
            self.mod = "out"

    def render(self, screen):
        if self.mod == "out":
            screen.blit(self.imgs[0], self.cor)
        elif self.mod == "in":
             screen.blit(self.imgs[1], self.cor)
        elif self.mod == "down":
             screen.blit(self.imgs[2], self.cor)