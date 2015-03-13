import Render_functions
import pygame


class Tile():
    def __init__(self, coords, state, ID):
        self.cor = coords       # Положение блока на тайловой сетке
        self.state = state      # Статус блока: "passable" - проходимый, "impassable" - непроходимый
        self.ID = ID

    def set_coords(self, cor):
        self.cor = cor


class Floor(Tile):
    def __init__(self,coords, img, ID, state="passable"):
        Tile.__init__(self,coords, state,ID)
        self.image = Render_functions.load_image(img,alpha_cannel=True)

    def render(self,screen, coof):
        screen.blit(self.image, (self.cor[0]*100+coof[0],self.cor[1]*100+coof[1]))

class Wall(Tile):
    def __init__(self,coords,img, ID, state="impassable",rotate = "D"):
        Tile.__init__(self,coords, state, ID)
        self.image = Render_functions.load_image(img,alpha_cannel=True)
        self.render_image = self.image
        self.rotate = rotate
        self.set_rotate(self.rotate)

    def set_rotate(self,rotate):
        self.rotate = rotate
        if rotate == "R":
            self.render_image = pygame.transform.rotate(self.image,90)
        elif rotate == "L":
            self.render_image = pygame.transform.rotate(self.image,-90)
        elif rotate == "U":
            self.render_image = pygame.transform.rotate(self.image,180)
        elif rotate == "D":
            self.render_image = self.image

    def render(self,screen,coof):
        screen.blit(self.render_image, (self.cor[0]*100+coof[0],self.cor[1]*100+coof[1]))