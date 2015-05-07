import pygame
from findPathLee import findPath
import Tile
from Character import Character
from NPC import NPC
import Extra_functions
import Render_functions
import pickle
import Buttons
import Spell


class GameProcess():
    def __init__(self, npc, character):
        self.turn = -1                      # Очередь хода (-1 - это наш персонаж)
        self.character = character          # Ссылка на игрового персонажа
        self.all_npc = npc                  # Ссылка на всех NPC
        self.all_persons = [character]      # Все персонажи
        self.all_persons.extend(npc)

    def update(self, dt):
        if self.character.stepwise_mod:
            if self.turn == -1:
                self.character.update(dt, self.all_persons)
            else:
                try:
                    self.all_npc[self.turn].update(dt, self.character, map_f, map_w, self.all_persons)
                    print(self.turn, "   Закончил -    ", self.all_npc[self.turn].finish, "  Тревога -  ", self.all_npc[self.turn].alarm, "  ОД   ", self.all_npc[self.turn].action_points)
                    if self.all_npc[self.turn].finish:
                        self.turn += 1
                except:
                    if self.all_npc[self.turn-1].finish:
                        self.turn = -1
        else:
            self.character.update(dt, self.all_persons)
            for npc in self.all_npc:
                npc.update(dt, self.character, map_f, map_w, self.all_persons)
                if npc.alarm:
                    self.on_stepwise_mod()

    def on_stepwise_mod(self):
        """
                Включить пошаговый режим для всех
        """
        self.turn = -1
        self.character.stepwise_mod = True
        try:
            for npc in self.all_npc:
                npc.stepwise_mod = True
        except:
            self.all_npc.stepwise_mod = True

    def change_mod(self):
        """
                Сменить режим с пошагового на нормальный или обратно
        """
        for npc in self.all_npc:
            if npc.alarm:
                return
        self.turn = -1
        self.character.change_mod()
        try:
            for npc in self.all_npc:
                npc.change_mod()
        except:
            self.all_npc.change_mod()

    def new_step(self):
        """
                Начать новый ход (он начинается с хода противников)
        """
        self.turn = 0
        self.character.action_points = 15
        try:
            for npc in self.all_npc:
                npc.action_points = 15
                npc.finish = False
        except:
            self.all_npc.action_points = 15
            self.all_npc.finish = False


class Interface():
    def __init__(self, char, npc, res, map_floor, map_wall):
        self.character = char
        self.npc_list = npc
        self.map_f = map_floor
        self.map_w = map_wall
        # self.map_pass = self.map_f[:]
        self.z_ind = False
        self.resolution = res
        self.path = None
        self.pathmarker = Render_functions.load_image('Pathmarker.png', alpha_cannel="True")  # Картинка выбраного пути
        self.ap = Render_functions.load_image('ActP_active.png', alpha_cannel="True")
        self.wasted_ap = Render_functions.load_image('ActP_wasted.png', alpha_cannel="True")
        self.buttons = []
        self.stepwise_buttons = []
        x = RES_X-150
        y = 100
        if type(self.character.spells) == list:
            for spell in self.character.spells:
                self.stepwise_buttons.append(Buttons.Button_Flag(Render_functions.load_text(spell.name), self.character.set_wearpon, (x, y), arg=(spell, None)))
                y += 10
        else:
            self.stepwise_buttons.append(Buttons.Button_Flag(Render_functions.load_text(self.character.spells.name), character.set_wearpon, (x, y), arg=(self.character.spells, None)))

    def events(self, e):
        if self.buttons:
            for but in self.buttons:
                if but.events(e):
                    self.z_ind = True
                else:
                    self.z_ind = False
        if self.character.stepwise_mod:
            for but in self.stepwise_buttons:
                if but.events(e):
                    self.z_ind = True
                elif self.z_ind != True:
                    self.z_ind = False
            if e.type == pygame.MOUSEMOTION:
                self.path = findPath(self.map_f, self.map_w, self.character.cor, (Extra_functions.get_click_tile(e.pos, render_coof, self.map_f)))
                if self.path == -1:
                    self.path = None
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1 and not self.z_ind:
                chosen_tile = Extra_functions.get_click_tile(e.pos, render_coof, self.map_f)
                t = True
                for npc in npc_list:
                    if chosen_tile == npc.cor:
                        self.character.set_target(npc)
                        t = False
                        break
                if t:
                    self.character.set_path(findPath(self.map_f, self.map_w, self.character.cor, chosen_tile))

    def render(self, screen, coof):
        screen.blit(Render_functions.load_text("Здоровье "+str(self.character.healf)+"|"+str(self.character.max_healf)), (RES_X-110, 5))
        screen.blit(Render_functions.load_text("Манна "+str(self.character.manna)+"|"+str(self.character.max_manna)), (RES_X-110, 25))
        if self.buttons:
            for but in self.buttons:
                    but.render(screen)
        x = self.resolution[0] - 330
        y = self.resolution[1] - 25
        for i in range(15):
            if i < self.character.action_points:
                screen.blit(self.ap, (x, y))
            else:
                screen.blit(self.wasted_ap, (x, y))
            x += 22
        x = self.resolution[0] - 375
        y = self.resolution[1] - 45
        w = self.character.gear["Wearpon"]
        if w:
            if type(w) == Spell.Spell:
                if w.type == "Attacking":
                    screen.blit(Render_functions.load_image('Fireball.png', alpha_cannel="True"), (x, y))
        else:
            screen.blit(Render_functions.load_image('Fist.png', alpha_cannel="True"), (x, y))
        if self.character.stepwise_mod:
            if self.stepwise_buttons:
                for but in self.stepwise_buttons:
                    but.render(screen)
            if self.path:
                for tile in self.path:
                    screen.blit(self.pathmarker, (coof[0]+tile[0]*100, coof[1]+tile[1]*100))
            for npc in self.npc_list:
                if npc.aggression:
                    screen.blit(Render_functions.load_text(str(npc.healf), color=(200, 0, 0)), (coof[0]+npc.cor[0]*100+10, coof[1]+npc.cor[1]*100+10))
            if self.character.dead:
                screen.blit(Render_functions.load_text("Вы мертвы", pt=200, color=(220, 0, 0)), (80, RES_Y/2-100))


def set_scene(scene_value):
    """
    Уникальная нанофункция, сменяющая сцену. Благодаря моим глубочайшим познаниям в архитектуре языка выглядит так уродливо
    """
    scene_value[0][0] = scene_value[1]


# Globals
FPS = 60                                            # ФПС программы
RES_X = 900                                         # Разрешение по длине
RES_Y = 700                                         # Разрешение по ширине
TILE_SIZE = 100                                     # Размер тайла (НЕ РАБОТАЕТ!!!!!)


# Main Actions
file = open('d', 'rb')                              # Открыть файл с картами
maps = pickle.load(file)                            # Загрузить карты
map_f, map_w, map_d = maps                          # Загрузить карты в собственные переменные
file.close()                                        # Закрыть файл с картами

pygame.init()                                       # PyGame начинает работу
screen = pygame.display.set_mode((RES_X, RES_Y))    # Создаем окно программы
clock = pygame.time.Clock()                         # Создаем таймер
menu = ["game"]                                     # Меню, которое в данный момент на экране
mainloop = True                                     # Двигатель главного цикла
world_img = pygame.Surface((RES_X, RES_Y))          # Поверхность, на которой отображается весь игровой мир
render_coof = [0, 0]
ch = False
npc_list = [NPC("Test_Enemy", (1, 4), gear=(None, None)), NPC("Test_Enemy_2", (4, 2), gear=(None, None))]
npc_list[0].attack_distance = 2
character = Character("Test Character", (0, 0), skills=(1, 3, 1), spelllist=(Spell.fireball))
game_process = GameProcess(npc_list, character)
interface = Interface(character, npc_list, (RES_X, RES_Y), map_f, map_w)
interface.buttons.append(Buttons.Button("Пошагово/Реальное время", (0, RES_Y-20), game_process.change_mod))
interface.stepwise_buttons.append(Buttons.Button("Конец хода", (300, RES_Y-20), game_process.new_step))


objects = {     # Все доступные объекты
    "Floor": {
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

        game_process.update(clock.get_time())
        world_img = Render_functions.scene_render(map_f, map_w, objects, world_img, TILE_SIZE)
        character.render(world_img)
        for npc in npc_list:
            npc.render(world_img)
        screen.blit(world_img, render_coof)
        interface.render(screen, render_coof)
    pygame.display.set_caption("FPS: " + str(clock.get_fps()))
    clock.tick(FPS)         # Управление ФПС
    pygame.display.flip()   # Обновляем дисплей