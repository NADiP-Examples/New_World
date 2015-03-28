import os
import pygame

# from Old_F.Game_text import *


def load_image(name,path = "Images", alpha_cannel = ""):
    fullname = os.path.join(path, name) # Указываем путь к папке с картинками

    try:
        image = pygame.image.load(fullname) # Загружаем картинку и сохраняем поверхность (Surface)
    except (pygame.error): # Если картинки нет на месте
        print("Cannot load image:", name)
        return 0
    if(alpha_cannel):
        image = image.convert_alpha()
    else:
        image = image.convert()

    return image

def load_text(text, color=(255, 255, 255), font=None, pt=20):
    return pygame.font.Font(font, pt).render(text, True, color)

def tiled_background(img, res_x, res_y):
    x = 0
    y = 0
    img = load_image(img, alpha_cannel="True")
    surface = pygame.Surface((res_x, res_y))
    size = img.get_rect()[3]
    while True:
        surface.blit(img, (x, y))
        x += size
        if x >= res_x:
            if y >= res_y:
                return surface
            x = 0
            y += size

def scene_render(map_f, map_w, objects, sur, size):
    y = 0
    for line in map_f:
        x = 0
        for tile in line:
            if tile:
                objects["Floor"][tile].set_coords((x, y))
                objects["Floor"][tile].render(sur)
            x += 1
        y += 1
    y = 0
    for line in map_w:
        x = 0
        for tile in line:
            z = 0
            for dir in tile:
                if dir == 1:
                    if z == 0:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("D")
                        objects["Wall"][dir].render(sur)
                    elif z == 1:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("L")
                        objects["Wall"][dir].render(sur)
                    elif z == 2:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("U")
                        objects["Wall"][dir].render(sur)
                    elif z == 3:
                        objects["Wall"][dir].set_coords((x, y))
                        objects["Wall"][dir].set_rotate("R")
                        objects["Wall"][dir].render(sur)
                z += 1
            x += 1
        y += 1
    size = (50, 50)
    sur = pygame.transform.scale(sur, size)
    return sur

def massdata_render(screen, mod, char):
    y = 15
    screen.blit(load_text("Навыки:", pt=25, color=(255,152,0)), (30,y))
    y += 60
    if mod[0] == "b":
        for thing in ("ranged","pistols","high_rate","shotguns","rifles","launchers","radiants","powers","sprayer","thrown","non-lethal","close-in", "short","long","spear","axes","strike",
                      "blocking", "fight_skills", "dogfight","tactic","armorer","equipment","light_armor","medium_armor","heavy_armor","suits"):
            if thing in ("ranged","close-in","fight_skills","equipment"):
                screen.blit(load_text(phrase[thing], pt=26), (50,y+15))
                y+=20
            else:
                screen.blit(load_text(phrase[thing], pt=22), (40,y))
                screen.blit(load_text(str(char.skills[thing]), pt=26), (245,y))
                screen.blit(load_image("sel_but_1.png",alpha_cannel="True"), (220,y))
            y += 20
    if mod[0] == "m":
        for thing in ("elements","fire","water","air","dirt","energy","life","necromancy","psionicist", "psychokinesis","mind_control","telepathy","multipurpose","protector","healer"):
            if thing in ("elements","psionicist","multipurpose"):
                screen.blit(load_text(phrase[thing], pt=26), (50,y+15))
                y+=20
            else:
                screen.blit(load_text(phrase[thing], pt=22), (40,y))
                screen.blit(load_text(str(char.skills[thing]), pt=26), (245,y))
            y += 20
    if mod[0] == "s":
        for thing in ("comm","threat","suasion","leadership","being", "games_of_chance","trade"):
            if thing in ("comm","being"):
                screen.blit(load_text(phrase[thing], pt=26), (50,y+15))
                y+=20
            else:
                screen.blit(load_text(phrase[thing], pt=22), (40,y))
                screen.blit(load_text(str(char.skills[thing]), pt=26), (245,y))
            y += 20
    if mod[0] == "c":
        for thing in ("natural","stamina","strength","agility","reaction","swiming","running","knowlege", "med","explosive","hack_locks","electrical_eng",
                      "survival","crimes", "stealth","pickpocketing","traps"):
            if thing in ("natural","knowlege","crimes"):
                screen.blit(load_text(phrase[thing], pt=26), (50,y+15))
                y+=20
            else:
                screen.blit(load_text(phrase[thing], pt=22), (40,y))
                screen.blit(load_text(str(char.skills[thing]), pt=26), (245,y))
            y += 20
        # if phrase[thing]:
        #     screen.blit(load_text(phrase[thing], pt=22), (40,y))
        # else:
        #     screen.blit(load_text("---", pt=25), (40,y))
# "pistols","high_rate","shotguns","rifles","launchers","radiants","powers","sprayer","thrown","non-lethal", "short","long","spear","axes","strike","blocking", "dogfight",
#                       "tactic","armorer","light_armor","medium_armor","heavy_armor","suits",   "fire","water","air","dirt","energy","life","necromancy", "psychokinesis","mind_control","telepathy",
#                       "protector","healer",   "charisma","threat","suasion","leadership","deception", "games_of_chance","trade","driving","aviating","ships","specesips","mech","riding",   "stamina",
#                       "strength","agility","reaction","quickness","climbing","swiming","running", "first-aid","surgery","explosive","hack_locks","electrical_eng","survival", "stealth",
#                       "pickpocketing","traps"