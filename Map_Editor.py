import pygame
import Extra_functions
import Tile
import Buttons


class EditableField():
    def __init__(self, width, height):
        self.map_f, self.map_w = self.matrix_creator(width, height)  # Карты тайлов и стен

    def matrix_creator(self, width, height):
        '''
                Получает ширину и высоту (в тайлах) и возвращает пустой шаблон карты (тайлов и стен - именно в этом порядке)
        '''
        matrix_f = []
        matrix_w = []
        line = []
        i = 0
        while i < width:
            line.append(0)
            i += 1
        i = 0
        while i < height:
            matrix_f.append(line[:])
            i += 1
        i = 0
        line = []
        while i < width:
            line.append([0, 0, 0, 0])
            i += 1
        i = 0
        while i < height:
            matrix_w.append(line[:])
            i += 1
        return matrix_f,matrix_w

    def matrix_new_line(self):
        '''
                Добавляет новую линию снизу
        '''
        line = []
        i = 0
        while i < len(self.map_f[0]):
            line.append(0)
            i += 1
        self.map_f.append(line)
        i = 0
        line = []
        while i < len(self.map_w[0]):
            line.append([0, 0, 0, 0])
            i += 1
        self.map_w.append(line)

    def matrix_del_last_line(self):
        '''
                Удаляет нижнюю линию
        '''
        if len(self.map_f) > 1:
            self.map_f = self.map_f[0:-1]
            self.map_w = self.map_w[0:-1]

    def matrix_new_column(self):
        """
                Добавляет новую колонну справа
        """
        for line in self.map_f:
            line.append(0)
        for line in self.map_w:
            line.append([0, 0, 0, 0])

    def matrix_del_last_column(self):
        """
                Удаляет колонну справа
        """
        if len(self.map_f[0]) > 1:
            i = 0
            while i < len(self.map_f):
                self.map_f[i] = self.map_f[i][:-1]
                i += 1
            i = 0
            while i < len(self.map_w):
                self.map_w[i] = self.map_w[i][:-1]
                i += 1


class Interface():
    def __init__(self, map, buttons, buttons_wall, map_size_buttons):
        self.brush = 0                              # ID тайла, которым мы будем рисовать!
        self.buttons = buttons                      # Кнопки, которыми меняются кисть тайлов
        self.buttons_wall = buttons_wall            # Кнопки, которыми меняются кисть стен
        self.map_size_buttons = map_size_buttons    # Кнопки, которыми меняется размер поля
        self.switch_buttons = []                    # Кнопки, переключающие меню
        self.section = "Floor"                      # Меню, которое находится в данный момент на экране
        self.grid = self.grid_creator(map)          # Сетка, которая накладывается на поле с тайлами

    def events(self, e, map):
        for but in self.switch_buttons:
            if but.events(e):
                self.buttons_up(but, self.switch_buttons)
                self.set_brush(0)
        if self.section == "Floor":
            for but in self.buttons:
                if but.events(e):
                    self.buttons_up(but, self.buttons)
        if self.section == "Wall":
            for but in self.buttons_wall:
                if but.events(e):
                    self.buttons_up(but, self.buttons_wall)
        for but in self.map_size_buttons:
            if but.events(e):
                self.grid = self.grid_creator(map)

    def buttons_up(self, but, lst):
        """
                Получает кнопку, на которую нажали и список с кнопками "отжимает" остальные кнопки
        """
        for button in lst:
            if button != but:
                button.stat = False

    def set_brush(self, new_brush):
        """
                Меняет кисть на новую
        """
        self.brush = new_brush

    def set_section(self, new_section):
        """
                Меняет секцию с объектами на новую
        """
        self.section = new_section

    def append_buttons(self, buttons):
        '''
                Добавляет кнопку/кнопки разных тайов в общий список
        '''
        try:
            for but in buttons:
                self.buttons.append(but)
        except:
            self.buttons.append(buttons)

    def grid_creator(self, map):
        '''
                Получает карту, возвращает секу, которая визуально будет отделять один тайл от другого
        '''
        width = 0
        height = 0
        i = 0
        while i < len(map):
            height += 100
            i += 1
        i = 0
        while i < len(map[0]):
            width += 100
            i += 1
        sur = pygame.Surface((width+1, height+1), pygame.SRCALPHA)
        x = 0
        y = 0
        i = 0
        while i <= len(map):
            pygame.draw.line(sur, (200, 200, 00), (0, y), (width, y))
            y += 100
            i += 1
        i = 0
        while i <= len(map[0]):
            pygame.draw.line(sur, (200, 200, 00), (x, 0), (x, height))
            x += 100
            i += 1
        return sur

    def render(self, screen, render_coof):
        screen.blit(self.grid, render_coof)
        for but in self.switch_buttons:
                but.render(screen)
        if self.section == "Floor":
            for but in self.buttons:
                but.render(screen)
        if self.section == "Wall":
            for but in self.buttons_wall:
                but.render(screen)
        for but in self.map_size_buttons:
            but.render(screen)


# Globals
FPS = 60      # ФПС программы
RES_X = 900   # Разрешение по длине
RES_Y = 700   # Разрешение по ширине

# Main Actions
pygame.init()                                       # PyGame начинает работу
screen = pygame.display.set_mode((RES_X, RES_Y))    # Создаем окно программы
mainloop = True                                     # Двигатель главного цикла
field = EditableField(5, 5)                         # Создаем шаблон поля тайлов
interface = Interface(field.map_f,[],[],            # Создаем интерфейс (сетка, кнопки)
    (Buttons.Button_Img(("sel_but_3.png", "sel_but_3.png", "sel_but_3.png"), (0, 200), field.matrix_new_line),
     Buttons.Button_Img(("sel_but_2.png", "sel_but_2.png", "sel_but_2.png"), (0, 178), field.matrix_del_last_line),
     Buttons.Button_Img(("sel_but_1.png", "sel_but_1.png", "sel_but_1.png"), (22, 150), field.matrix_new_column),
     Buttons.Button_Img(("sel_but_4.png", "sel_but_4.png", "sel_but_4.png"), (0, 150), field.matrix_del_last_column)))
render_coof = [200, 200]
ch = False
world_img = pygame.Surface((RES_X,RES_Y))

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

interface.append_buttons((Buttons.Button_Flag(objects["Floor"][1].image, interface.set_brush, (0, 50),arg=(1, 0)),Buttons.Button_Flag(objects["Floor"][2].image,interface.set_brush,(100,50),arg=(2,0))))
interface.switch_buttons.append(Buttons.Button_Flag(objects["Floor"][1].image,interface.set_section,(0,0),arg=("Floor","Floor"),size=(25,25)))
interface.switch_buttons.append(Buttons.Button_Flag(objects["Wall"][1].image,interface.set_section,(25,0),arg=("Wall","Wall"),size=(25,25)))
interface.buttons_wall.append(Buttons.Button_Flag(objects["Wall"][1].image,interface.set_brush,(0,50),arg=(1,0)))

while mainloop:
    screen.fill((0, 0, 0))
    world_img.fill((0, 0, 0))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
                mainloop = False
        if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.MOUSEBUTTONUP or e.type == pygame.MOUSEMOTION:
            interface.events(e, field.map_f)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 2:
                    ch = True
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    if interface.section == "Floor":
                        if Extra_functions.get_click_tile(e.pos, render_coof, field.map_f) != -1:
                            field.map_f[Extra_functions.get_click_tile(e.pos, render_coof, field.map_f)[1]][Extra_functions.get_click_tile(e.pos, render_coof, field.map_f)[0]] = interface.brush
                    elif interface.section == "Wall":
                        if Extra_functions.get_click_tile(e.pos, render_coof, field.map_f) != -1:
                            cor = Extra_functions.get_pixel_in_tile(e.pos, render_coof, field.map_f)
                            if cor[1] >=90:
                                field.map_w[Extra_functions.get_click_tile(e.pos, render_coof, field.map_f)[1]][Extra_functions.get_click_tile(e.pos, render_coof, field.map_f)[0]][0] = interface.brush
                if e.button == 2:
                    ch = False
            if e.type == pygame.MOUSEMOTION:
                if ch:
                    render_coof[0] += e.rel[0]
                    render_coof[1] += e.rel[1]
    # Начало скрипта определения и отрисовки тайлов!
    y = 0
    for line in field.map_f:
        x = 0
        for tile in line:
            if tile:
                objects["Floor"][tile].set_coords((x, y))
                objects["Floor"][tile].render(world_img, render_coof)
            x += 1
        y += 1
    y = 0
    for line in field.map_w:
        x = 0
        for tile in line:
            z = 0
            for dir in tile:
                if dir == 1:
                    if z == 0:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("D")
                        objects["Wall"][dir].render(world_img, render_coof)
                    elif z == 1:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("L")
                        objects["Wall"][dir].render(world_img, render_coof)
                    elif z == 2:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("U")
                        objects["Wall"][dir].render(world_img, render_coof)
                    elif z == 3:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("R")
                        objects["Wall"][dir].render(world_img, render_coof)
                z += 1
            x += 1
        y += 1
    # Конец скрипта определения и отрисовки тайлов!
    screen.blit(world_img, (0, 0))              # Клеим поле
    interface.render(screen, render_coof)       # Клеим интерфейс
    pygame.display.flip()                       # Обновляем экран