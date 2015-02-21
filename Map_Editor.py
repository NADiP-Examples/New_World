from pygame import *
from Extra_functions import *
from Tile import *
from Buttons import *

class Editable_Field():
    def __init__(self,width,height):
        self.map_f, self.map_w = self.matrix_creator(width,height)

    def matrix_creator(self,width,height):
        matrix_f = []
        matrix_w = []
        line = []
        i = 0
        while i < width:
            line.append(0)
            i+=1
        i = 0
        while i < height:
            matrix_f.append(line[:])
            i+=1
        i = 0
        line = []
        while i < width:
            line.append([0,0,0,0])
            i+=1
        i = 0
        while i < height:
            matrix_w.append(line[:])
            i+=1
        return matrix_f,matrix_w

class Interface():
    def __init__(self,map):
        self.brush = 0
        self.grid = self.grid_creator(map)

    def set_brush(self, new_brush):
        self.brush = new_brush

    def grid_creator(self,map):
        width = 0
        height = 0
        i = 0
        while i < len(map):
            height += 100
            i+=1
        i = 0
        while i < len(map[0]):
            width += 100
            i+=1
        sur = Surface((width+1,height+1),SRCALPHA)
        # sur.set_alpha(10)
        x = 0
        y = 0
        i = 0
        while i <= len(map):
            print(len(map))
            draw.line(sur,(200,200,00),(0,y),(width,y))
            y+=100
            i+=1
        i = 0
        while i <= len(map[0]):
            print(len(map[0]))
            draw.line(sur,(200,200,00),(x,0),(x,height))
            x+=100
            i+=1
        return sur

    def render(self,screen,render_coof):
        screen.blit(self.grid,render_coof)



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
interface = Interface(field.map_f)
render_coof = [200,200]
ch = False
world_img = Surface((RES_X,RES_Y))

B_tile = Floor((0,0),"Tile-2.png")
B_wall = Wall((0,0),"Wall_1.png")

button = Button_Flag((B_tile.image,B_tile.image),interface.set_brush,(0,0),arg=(1,0))

while mainloop:
    screen.fill((0,0,0))
    world_img.fill((0,0,0))
    for e in event.get():
        if e.type == QUIT:
                mainloop = False
        if e.type == MOUSEBUTTONDOWN or e.type == MOUSEBUTTONUP or e.type == MOUSEMOTION:
            button.events(e)
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 2:
                    ch = True
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    if get_click_tile(e.pos,render_coof,field.map_f) != -1:
                        field.map_f[get_click_tile(e.pos,render_coof,field.map_f)[1]][get_click_tile(e.pos,render_coof,field.map_f)[0]] = interface.brush
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
    interface.render(screen,render_coof)
    button.render(screen)
    display.flip()