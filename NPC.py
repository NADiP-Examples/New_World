from Men import Men
import pygame
from findPathLee import findPath


class NPC(Men):
    def __init__(self, name, cor, aggression=True, vision=2):
        super().__init__(name, cor)
        self.aggression = aggression
        self.vision = vision
        self.visionfield_update()

    def update(self, dt, char, map_f, map_w):
        self.visionfield_update()
        self.attackfield_update()
        if self.AI(char, map_f, map_w):
            super().update(dt)
            return True
        else:
            super().update(dt)

    def AI(self, char, map_f, map_w):
        """
                Интеллект NPC
        """
        if self.aggression:
            if self.attack_field.collidepoint(char.cor[0], char.cor[1]):
                self.hit(char)
                return True
            else:
                if self.vision_field.collidepoint(char.cor[0], char.cor[1]):
                    if not self.path:
                        self.set_path(findPath(map_f, map_w, self.cor, char.cor))
                        if self.path != -1:
                            self.path = self.path[:-1]
                        return True

    def visionfield_update(self):
        self.vision_field = pygame.Rect(self.cor[0]-self.vision, self.cor[1]-self.vision, self.vision*2+1, self.vision*2+1)