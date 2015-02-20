from pygame import *
from findPathLee import findPath
from Tile import *
from Character import *
from Extra_functions import *

def set_scene(scene_value):
    """
    Уникальная нанофункция, сменяющая сцену. Благодаря моим глубочайшим познаниям в архитектуре языка выглядит так уродливо
    """
    scene_value[0][0] = scene_value[1]

# Globals
FPS = 60      #  ФПС программы
RES_X = 900   # Разрешение по длине
RES_Y = 700   # Разрешение по ширине

map_f = (
    (1,1,1,0,0,1,1),
    (1,1,1,1,0,1,1),
    (1,1,1,1,1,1,1),
    (1,1,1,1,1,1,1),
    (0,0,1,1,1,1,1),
    (0,1,1,1,1,1,1)
)
map_w = (
    ((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)),
    ((0,0,0,0),(0,0,0,0),(0,0,1,1),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)),
    ((0,0,1,0),(1,1,1,1),(0,0,0,1),(0,0,0,0),(0,0,0,1),(0,0,0,0),(0,0,0,0)),
    ((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,1),(0,0,0,0),(0,0,0,0),(0,0,0,0)),
    ((0,0,0,0),(0,0,0,0),(1,0,0,1),(0,0,1,1),(0,0,0,1),(0,0,1,0),(0,0,1,0)),
    ((0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0))
)




        # Main Actions
init()                                      # PyGame начинает работу
screen = display.set_mode((RES_X,RES_Y))    # Создаем окно программы
clock = time.Clock()                        #Создаем таймер
menu = ["game"]                             # Меню, которое в данный момент на экране
mainloop = True                             # Двигатель главного цикла
world_img = Surface((RES_X,RES_Y))
render_coof = [0,0]
ch = False
character = Character("Test Character",(0,0))
B_tile = Floor((0,0),"B_Tile.png")
B_wall = Wall((0,0),"Wall_1.png")

while mainloop:
    screen.fill((0,0,0))
    world_img.fill((0,0,0))
    if menu[0] == "game":
        for e in event.get():
            if e.type == QUIT:
                    mainloop = False
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    pass
                if e.button == 2:
                    ch = True
            if e.type == MOUSEBUTTONUP:
                if e.button == 1:
                    character.set_path(findPath(map_f,map_w,character.cor,(get_click_tile(e.pos,render_coof,map_f))))
                if e.button == 2:
                    ch = False
            if e.type == MOUSEMOTION:
                if ch:
                    render_coof[0] += e.rel[0]
                    render_coof[1] += e.rel[1]
            elif e.type == KEYDOWN or e.type == KEYUP:
                pass
        y = 0
        for line in map_f:
            x = 0
            for tile in line:
                if tile == 1:
                    B_tile.set_coords((x,y))
                    B_tile.render(world_img,render_coof)
                x+=1
            y+=1
        y = 0
        for line in map_w:
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

        character.update(clock.get_time())

        character.render(world_img,render_coof)
        screen.blit(world_img,(0,0))

    # print(clock.get_time())
    display.set_caption("FPS: " + str(clock.get_fps()))
    clock.tick(FPS) # Управление ФПС

    display.flip() # Обновляем дисплей