from Men import Men
import pygame
from findPathLee import findPath


class NPC(Men):
    def __init__(self, name, cor, aggression=True, vision=2):
        super().__init__(name, cor)
        self.aggression = aggression
        self.vision = vision
        self.visionfield_update()

    def update(self, dt, char_cor, map_f, map_w):
        self.visionfield_update()
        self.AI(char_cor, map_f, map_w)
        super().update(dt)

    def AI(self, char_cor, map_f, map_w):
        if self.aggression:
            if self.vision_field.collidepoint(char_cor[0], char_cor[1]):
                self.set_path(findPath(map_f, map_w, self.cor, char_cor))


    def visionfield_update(self):
        self.vision_field = pygame.Rect(self.cor[0]-self.vision, self.cor[1]-self.vision, self.vision*2+1, self.vision*2+1)