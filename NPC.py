from Men import Men
import pygame
from findPathLee import findPath


class NPC(Men):
    def __init__(self, name, cor, aggression=True, vision=3, skills=(1, 1, 1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=("White_doc_robe.png", None)):
        super().__init__(name, cor, skills=skills, spelllist=spelllist, body=body, gear=gear)
        self.aggression = aggression
        self.search = False
        self.search_point = None
        self.alarm = False
        self.vision = vision
        self.visionfield_update()
        self.finish = False

    def update(self, dt, char, map_f, map_w, map_w_phisic, all_persons):
        if self.dead:
            self.finish = True
        else:
            self.visionfield_update()
            self.attackfield_update()
            self.AI(char, map_f, map_w, map_w_phisic)
            super().update(dt, all_persons)
            if self.stepwise_mod and self.action_points - self.coofs['stepwise_move'] < 0 and not self.anim_play:
                self.finish = True

    def AI(self, char, map_f, map_w, map_w_phisic):
        """
                Интеллект NPC. Он уже может:
                    1.
        """
        if self.search:
            if self.alarm:
                self.search = False
            else:
                if self.cor == self.search_point:
                    self.search = False
                    self.search_point = None
                else:
                    if not self.search_point:
                        self.search_point = char.cor
                    self.aggression = True
                    self.set_path(findPath(map_f, map_w, self.cor, self.search_point)[:-1])
                    if type(self.path) == list:
                        self.search_point = self.path[-1]
        if self.aggression:
            if self.attack_field.collidepoint(char.cor[0], char.cor[1]):
                self.path = None
                if self.alarm:
                    self.set_target(char)
            else:
                if self.vision_field.collidepoint(char.cor[0], char.cor[1]) and self.check_for_visibility(map_w_phisic, ((self.cor[0]+0.5,self.cor[1]+0.5),(char.cor[0]+0.5,char.cor[1]+0.5))): #
                    self.alarm = True
                    if not self.path:
                        self.set_path(findPath(map_f, map_w, self.cor, char.cor))
                        if self.path != -1:
                            self.path = self.path[:-1]
                else:
                    self.alarm = False
                    if not self.path:
                        self.finish = True
        else:
            self.finish = True
        if not self.alarm and not self.search and not self.path:
            self.finish = True

    def hurt(self, damage):
        super().hurt(damage)
        self.search = True

    def kill_men(self):
        super().kill_men()
        self.finish = True
        self.alarm = False
        self.search = False

    def use_action_points(self, cost):
        """
                Отнять cost очков действий, если при этом их кол-во не станет меньше нуля
        """
        if self.action_points >= cost:
            self.action_points -= cost
            return True
        else:
            self.finish = True
            return False

    def visionfield_update(self):
        self.vision_field = pygame.Rect(self.cor[0]-self.vision, self.cor[1]-self.vision, self.vision*2+1, self.vision*2+1)