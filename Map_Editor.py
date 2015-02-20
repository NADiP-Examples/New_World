from pygame import *
from Extra_functions import *
from Tile import *

class Editable_Field():
    def __init__(self,width,height):
        self.map_f, self.map_w = self.matrix_creator(width,height)

    def matrix_creator(self,width,height):
        matrix_f = []
        matrix_w = []
        line = []
        i = 0
        while i < width:
            line.append(1)
            i+=1
        i = 0
        while i < height:
            matrix_f.append(line)
            i+=1
        i = 0
        line = []
        while i < width:
            line.append([0,0,0,0])
            i+=1
        i = 0
        while i < height:
            matrix_w.append(line)
            i+=1
        return matrix_f,matrix_w

class Interface():
    def __init__(self):
        self.brush = 0

# Globals
FPS = 60      #  ФПС программы
RES_X = 900   # Разрешение по длине
RES_Y = 700   # Разрешение по ширине

        # Main Actions
init()                                      # PyGame начинает работу
screen = display.set_mode((RES_X,RES_Y))    # Создаем окно программы
# menu = ["game"]                             # Меню, которое в данный момент на экране
mainloop = True                             # Двигатель главного цикла

field = Editable_Field(5,5)
interface = Interface()
render_coof = [200,200]
ch = False
world_img = Surface((RES_X,RES_Y))

B_tile = Floor((0,0),"B_Tile.png")
B_wall = Wall((0,0),"Wall_1.png")

while mainloop:
    screen.fill((0,0,0))
    world_img.fill((0,0,0))
    for e in event.get():
        if e.type == QUIT:
                mainloop = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 2:
                ch = True
        if e.type == MOUSEBUTTONUP:
            if e.button == 1:
                pass
                # field.map_f[get_click_tile(e.pos,render_coof,field.map_f)[]] #fixme! ДОДЕЛАТЬ!
            if e.button == 2:
                ch = False
        if e.type == MOUSEMOTION:
            if ch:
                render_coof[0] += e.rel[0]
                render_coof[1] += e.rel[1]
    y = 0
    for line in field.map_f:
        x = 0
        for tile in line:
            if tile == 1:
                B_tile.set_coords((x,y))
                B_tile.render(world_img,render_coof)
            x+=1
        y+=1
    y = 0
    for line in field.map_w:
        x = 0
        for tile in line:
            z = 0
            for dir in tile:
                if dir == 1:
                    if z == 0:
                        B_wall.set_coords((x,y))
                        B_wall.set_rotate("D")
                        B_wall.render(world_img,render_coof)
                    elif z == 1:
                        B_wall.set_coords((x,y))
                        B_wall.set_rotate("L")
                        B_wall.render(world_img,render_coof)
                    elif z == 2:
                        B_wall.set_coords((x,y))
                        B_wall.set_rotate("U")
                        B_wall.render(world_img,render_coof)
                    elif z == 3:
                        B_wall.set_coords((x,y))
                        B_wall.set_rotate("R")
                        B_wall.render(world_img,render_coof)
                z +=1
            x+=1
        y+=1
    screen.blit(world_img,(0,0))
    display.flip()