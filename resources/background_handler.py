import pygame as pg
import os
import ctypes
from pygame import image
pg.font.init()
cwd = os.getcwd()
user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
game_display = pg.display.set_mode((0, 0)) # The canvas

pg.init()
clock = pg.time.Clock()
#clock.tick(60)
background_cache = {"initialized": False}
previous_game_screen = "main_menu"
def load_background(game_screen, settings):
    global background_cache
    background_cache['initialized'] = True
    if(game_screen == "main_menu"):
        if(settings['hd_backgrounds']):
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\main_menu_background_hd.png").convert()
        else:
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\main_menu_background.png").convert()
    elif(game_screen == "casual_css"):
        if(settings['hd_backgrounds']):
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\css_background.png").convert()
        else:
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\green_background.png").convert()
    elif(game_screen == "casual_match"):
        if(settings['hd_backgrounds']):
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\field_alpha_hd.png").convert()
        else:
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\field_alpha.png").convert()
    elif(game_screen == "win_screen"):
        background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\green_background.png")
    elif(game_screen == "rules"):
        print("RULES")
        if(settings['hd_backgrounds']):
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\rules_background.png").convert()
        else:
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\green_background.png").convert()
    elif(game_screen == "settings"):
        if(settings['hd_backgrounds']):
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\settings_background.png").convert()
        else:
            background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\green_background.png").convert()
def draw_background(game_display, game_screen, settings):
    global cwd
    global background_cache
    global previous_game_screen
    if not (game_screen == previous_game_screen):
        background_cache['initialized'] = False
        previous_game_screen = game_screen
    if(not background_cache['initialized']):
        load_background(game_screen, settings)
    game_display.blit(background_cache['background'], (0, 0))