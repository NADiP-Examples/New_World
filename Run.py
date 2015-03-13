import pygame
from findPathLee import findPath
import Tile
from Character import Character
import Extra_functions


def set_scene(scene_value):
    """
    Уникальная нанофункция, сменяющая сцену. Благодаря моим глубочайшим познаниям в архитектуре языка выглядит так уродливо
    """
    scene_value[0][0] = scene_value[1]

# Globals
FPS = 60      # ФПС программы
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
pygame.init()                                       # PyGame начинает работу
screen = pygame.display.set_mode((RES_X,RES_Y))     # Создаем окно программы
clock = pygame.time.Clock()                         #Создаем таймер
menu = ["game"]                                     # Меню, которое в данный момент на экране
mainloop = True                                     # Двигатель главного цикла
world_img = pygame.Surface((RES_X, RES_Y))
render_coof = [0, 0]
ch = False
character = Character("Test Character", (0, 0))
B_tile = Tile.Floor((0, 0), "B_Tile.png", 1)
B_wall = Tile.Wall((0, 0), "Wall_1.png", 1)

while mainloop:
    screen.fill((0, 0, 0))
    world_img.fill((0, 0, 0))
    if menu[0] == "game":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                    mainloop = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    pass
                if e.button == 2:
                    ch = True
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    character.set_path(findPath(map_f,map_w,character.cor,(Extra_functions.get_click_tile(e.pos,render_coof,map_f))))
                if e.button == 2:
                    ch = False
            if e.type == pygame.MOUSEMOTION:
                if ch:
                    render_coof[0] += e.rel[0]
                    render_coof[1] += e.rel[1]
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
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
    pygame.display.set_caption("FPS: " + str(clock.get_fps()))
    clock.tick(FPS) # Управление ФПС

    pygame.display.flip() # Обновляем дисплей