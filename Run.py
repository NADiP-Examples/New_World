import pygame
from findPathLee import findPath
import Tile
from Character import Character
from NPC import NPC
import Extra_functions
import Render_functions
import pickle
import Buttons


class Interface():
    def __init__(self, char, npc, res):
        self.buttons = []
        self.stepwise_buttons = []
        self.character = char
        self.npc_list = npc
        self.z_ind = False
        self.resolution = res
        self.path = None

    def events(self, e):
        if self.buttons:
            for but in self.buttons:
                if but.events(e):
                    self.z_ind = True
                else:
                    self.z_ind = False
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1 and not self.z_ind:
                chosen_tile = Extra_functions.get_click_tile(e.pos, render_coof, map_f)
                for npc in npc_list:
                    if chosen_tile == npc.cor:
                        character.hit(npc)
                        print("NPC HEALTH HERE!!! - ", npc.healf)
                    else:
                        character.set_path(findPath(map_f, map_w, character.cor, chosen_tile))
        if character.stepwise_mod:
            for but in self.stepwise_buttons:
                if but.events(e):
                    self.z_ind = True
                else:
                    self.z_ind = False
            if e.type == pygame.MOUSEMOTION:
                self.path = findPath(map_f, map_w, character.cor, (Extra_functions.get_click_tile(e.pos, render_coof, map_f)))
                if self.path == -1:
                    self.path = None

    def new_step(self):
        character.action_points = 15
        if self.npc_list:
            for npc in self.npc_list:
                npc.action_points = 15

    def change_mod(self):
        character.change_mod()
        for npc in self.npc_list:
            npc.change_mod()

    def render(self, screen, coof):
        if self.buttons:
            for but in self.buttons:
                    but.render(screen)
        x = self.resolution[0] - 330
        y = self.resolution[1] - 25
        for i in range(15):
            if i < character.action_points:
                screen.blit(Render_functions.load_image('ActP_active.png', alpha_cannel="True"), (x, y))
            else:
                screen.blit(Render_functions.load_image('ActP_wasted.png', alpha_cannel="True"), (x, y))
            x += 22
        if character.stepwise_mod:
            if self.stepwise_buttons:
                for but in self.stepwise_buttons:
                    but.render(screen)
            if self.path:
                for tile in self.path:
                    screen.blit(Render_functions.load_image('Tile-Button-down.png', alpha_cannel="True"), (coof[0]+tile[0]*100, coof[1]+tile[1]*100))



def set_scene(scene_value):
    """
    Уникальная нанофункция, сменяющая сцену. Благодаря моим глубочайшим познаниям в архитектуре языка выглядит так уродливо
    """
    scene_value[0][0] = scene_value[1]

# Globals
FPS = 60      # ФПС программы
RES_X = 900   # Разрешение по длине
RES_Y = 700   # Разрешение по ширине
TILE_SIZE = 100

def npc_step(npc_list):
    for npc in npc_list:
        pass



        # Main Actions
file = open('d', 'rb')
maps = pickle.load(file)
map_f, map_w, map_d = maps
file.close()

pygame.init()                                       # PyGame начинает работу
screen = pygame.display.set_mode((RES_X, RES_Y))    # Создаем окно программы
clock = pygame.time.Clock()                         # Создаем таймер
menu = ["game"]                                     # Меню, которое в данный момент на экране
mainloop = True                                     # Двигатель главного цикла
world_img = pygame.Surface((RES_X, RES_Y))
render_coof = [0, 0]
ch = False
npc_list = [NPC("Test_Enemy", (1, 4))]
character = Character("Test Character", (0, 0))
interface = Interface(character, npc_list, (RES_X, RES_Y))
interface.buttons.append(Buttons.Button("Пошагово/Реальное время", (0, RES_Y-20), interface.change_mod))
interface.stepwise_buttons.append(Buttons.Button("Конец хода", (300, RES_Y-20), interface.new_step))
# npc_list[0].set_path(findPath(map_f, map_w, npc_list[0].cor, character.cor))

objects = {
        # Все доступные объекты
    "Floor" : {
        1: Tile.Floor((0, 0), "B_Tile.png", 1),
        2: Tile.Floor((0, 0), "Tile-2.png", 2)
    },
    "Wall": {
        1: Tile.Wall((0, 0), "Wall_1.png", 1)
    }
}

while mainloop:
    screen.fill((0, 0, 0))
    world_img.fill((0, 0, 0))
    if menu[0] == "game":
        for e in pygame.event.get():
            if e.type == pygame.MOUSEMOTION or e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP:
                interface.events(e)
            if e.type == pygame.QUIT:
                    mainloop = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    pass
                if e.button == 2:
                    ch = True
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 2:
                    ch = False
            if e.type == pygame.MOUSEMOTION:
                if ch:
                    render_coof[0] += e.rel[0]
                    render_coof[1] += e.rel[1]
            elif e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                pass

        character.update(clock.get_time())
        for npc in npc_list:
            if npc.update(clock.get_time(), character, map_f, map_w):
                character.stepwise_mod = True
                for npc in npc_list:
                    npc.stepwise_mod = True
        world_img = Render_functions.scene_render(map_f, map_w, objects, world_img, TILE_SIZE)
        character.render(world_img)
        for npc in npc_list:
            npc.render(world_img)
        screen.blit(world_img, render_coof)
        interface.render(screen, render_coof)
    print(character.healf)
    pygame.display.set_caption("FPS: " + str(clock.get_fps()))
    clock.tick(FPS)         # Управление ФПС
    pygame.display.flip()   # Обновляем дисплей