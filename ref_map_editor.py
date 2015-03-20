__author__ = 'booblegum'
import pygame
from Render_functions import load_image
import copy
ON = 1
OUT = 0


class EditableField():
    def __init__(self, width, height, pos=(0, 0)):
        # Карты тайлов и стен
        self.map_floor = []
        self.map_wall = []
        self._create_empty_maps(width, height)
        self.pos = pos
        self.cell_size = (40, 40)
        self.image = pygame.Surface((width*self.cell_size[0], height*self.cell_size[1]), pygame.SRCALPHA)
        self.image.fill((0, 50, 0))
        self.rect = self.image.get_rect()
        self.rect.move_ip(pos)
        self.draw_field()
        self.drag = False
        self.mod = OUT

    def _create_empty_maps(self, width, height):
        """Создаем пустые карты: Тайлов и Стен"""
        self.map_floor = []
        for h in range(height):
            line_floor = []
            line_wall = []
            for w in range(width):
                line_floor.append(0)
                line_wall.append([0, 0, 0, 0])
            self.map_floor.append(line_floor)
            self.map_wall.append(line_wall)

    def add_row(self):
        """Добавляет новую линию снизу"""
        self.map_floor.append([0 for _ in range(len(self.map_floor[0]))])
        self.map_floor.append([[0, 0, 0, 0] for _ in range(len(self.map_floor[0]))])

    def del_row(self):
        """Удаляет нижнюю линию"""
        if len(self.map_floor) > 1:
            self.map_floor.pop()
            self.map_wall.pop()

    def add_column(self):
        """Добавляет новую колонну справа"""
        for line in self.map_floor:
            line.append(0)
        for line in self.map_wall:
            line.append([0, 0, 0, 0])

    def del_column(self):
        """Удаляет колонну справа"""
        for line in self.map_floor:
            line.pop()
        for line in self.map_wall:
            line.pop()

    def draw_field(self):
        x = 0
        y = 0
        for line in self.map_floor:
            pygame.draw.line(self.image, (200, 200, 00), (0, y), (self.rect.w, y))
            y += self.cell_size[1]
            for el in line:
                pygame.draw.line(self.image, (200, 200, 00), (x, 0), (x, self.rect.h))
                x += self.cell_size[0]

    def events(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.mod = ON
            else:
                self.mod = OUT
            if self.drag:
                self.rect = self.rect.move(event.rel)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.mod == ON:
            self.drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag = False

    def render(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Tile:
    def __init__(self, image, pos, id):
        self.image = load_image(image, alpha_cannel="True")
        self.rect = self.image.get_rect()
        # Подсветка при наведении
        self.backlight = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.backlight.fill((0, 0, 20, 150))
        self.id = id

        self.rect.move_ip(pos)
        self.over = False  # Курсор над Тайлом
        self.pressed = False  # Кнопка мыши была надажа над Тайлом

    def resize(self, new_size):
        self.image = pygame.transform.scale(self.image, new_size)
        self.rect = self.image.get_rect()
        self.backlight = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.backlight.fill((0, 0, 20, 150))

    def move_to(self, new_pos):
        self.rect.move_ip(new_pos)

    def events(self, e):
        if e.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(e.pos):
                self.over = True
            else:
                self.over = False
        elif e.type == pygame.MOUSEBUTTONDOWN and self.over:
            self.pressed = True
        elif e.type == pygame.MOUSEBUTTONUP and self.over and self.pressed:
            self.pressed = False
            return self.id  # FIXME: bad idea, тут нужно генерить свое событие click

    def render(self, screen):
        screen.blit(self.image, self.rect.topleft)
        if self.over:
            screen.blit(self.backlight, self.rect.topleft)


# Палитра
class Palette:
    def __init__(self, pos=(0, 0), paints=[]):
        self.paints = paints
        self.paints_size = (40, 40)
        self.screen = pygame.Surface((self.paints_size[0]*len(self.paints), self.paints_size[1]))
        self.rect = self.screen.get_rect()
        self.rect.move_ip(pos)
        self.screen.fill((0, 0, 100))
        self._paints_to_place()

    def _paints_to_place(self):
        x, y = 0, 0
        for paint in self.paints:
            paint.resize(self.paints_size)
            paint.move_to((x, y))
            x += self.paints_size[0]
            # y += self.paints_size[1]

    def events(self, event):
        # Немного магия, но зато очень удобно пользовать -)
        # переводим глобальные координаты в локальные и отдаем дочерним элементам
        # Т.е. создаем копию событий, и уже в копии меняем .pos для доч.элементов
        new_event = pygame.event.Event(event.type, event.dict.copy())
        try:
            new_event.pos = (event.pos[0]-self.rect.x, event.pos[1]-self.rect.y)
        except AttributeError:
            pass
        for paint in self.paints:
            paint.events(new_event)

    def render(self, screen):
        for paint in self.paints:
            paint.render(self.screen)
        screen.blit(self.screen, self.rect.topleft)


# Перетаскиваемая палитра
class DnDPalette(Palette):
    def __init__(self, pos=(0, 0), paints=[]):
        Palette.__init__(self, pos=pos, paints=paints)
        self.drag = False
        self.mod = OUT

    def events(self, event):
        # Обрабатываем события самой панелью
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.mod = ON
            else:
                self.mod = OUT
            if self.drag:
                self.rect = self.rect.move(event.rel)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.mod == ON:
            self.drag = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.drag = False

        Palette.events(self, event)


class Editor:
    def __init__(self):
        self.palettes = []
        self.field = None

    def events(self, event):
        pass

    def render(self, screen):
        pass

if __name__ == '__main__':
    # Globals
    FPS = 60
    RES_X = 500
    RES_Y = 500

    pygame.init()
    screen = pygame.display.set_mode((RES_X, RES_Y))
    # tile = Tile('B_Tile.png', (50, 50), 1)
    palette = DnDPalette(paints=[Tile('B_Tile.png', (50, 50), 1),
                                 Tile('B_Tile.png', (50, 50), 2),
                                 Tile('Tile-2.png', (50, 50), 4),
                                 Tile('B_Tile.png', (50, 50), 5)])

    palette2 = DnDPalette(pos=(20, 20), paints=[Tile('B_Tile.png', (50, 50), 1),
                                 Tile('B_Tile.png', (50, 50), 2),
                                 Tile('Tile-2.png', (50, 50), 4),
                                 Tile('B_Tile.png', (50, 50), 5)])
    ef = EditableField(5, 4)
    mainloop = True
    while mainloop:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                    mainloop = False
            palette.events(e)
            palette2.events(e)
            ef.events(e)

        screen.fill((0, 0, 0))
        ef.render(screen)
        palette.render(screen)
        palette2.render(screen)
        pygame.display.flip()