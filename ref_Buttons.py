__author__ = 'booblegum'
import pygame
from Render_functions import load_image


class ButtonImg():
    """ Исправленный класс Кнопки (не проверен)"""
    def __init__(self, images, pos, action):
        """Картинки могут быть переданы как в виде путей к файлам, так и ввиде Surface' ов"""
        self.images = {}
        if all(isinstance(img, pygame.Surface) for img in images):
            self.images = {'out': images[0], 'in': images[1], 'down': images[2]}
        else:
            for key, img in zip(['out', 'in', 'down'], images):
                self.images[key] = load_image(img, alpha_cannel="True")

        self.pos = pos
        self.mod = "out"
        self.action = action
        self.rect = self.images['out'].get_rect()
        self.rect.move_ip(pos)

    def events(self, e):
        if e.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(e.pos):
                self.mod = "in"
        elif e.type == pygame.MOUSEBUTTONDOWN and self.mod == 'in':
            self.mod = "down"
        elif e.type == pygame.MOUSEBUTTONUP and self.mod == 'down':
            self.action()
            self.mod = 'in'
        else:
            self.mod = "out"

    def render(self, screen):
        screen.blit(self.images[self.mod], self.pos)