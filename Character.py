from Men import Men
import pygame

class Character(Men):
    def __init__(self, name, cor, skills=(1,1,1), spelllist = ()):
        super().__init__(name, cor, skills=skills, spelllist=spelllist)