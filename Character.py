from Men import Men
import pygame

class Character(Men):
    def __init__(self, name, cor, skills=(1,1,1), spelllist = (), body=("Body_1.png", "Head_1.png"), gear=(None, None)):
        super().__init__(name, cor, skills=skills, spelllist=spelllist, body=body, gear=gear)