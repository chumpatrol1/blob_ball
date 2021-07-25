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
def load_background(game_screen):
    global background_cache
    background_cache['initialized'] = True
    if(game_screen == "main_menu"):
        background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\green_background.png")
    elif(game_screen == "casual_css"):
        background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\green_background.png")
    elif(game_screen == "casual_match"):
        background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\field_alpha.png").convert()
    elif(game_screen == "win_screen"):
        background_cache['background'] = pg.image.load(cwd + "\\resources\\images\\green_background.png")

def draw_background(game_display, game_screen):
    global cwd
    global background_cache
    global previous_game_screen
    if not (game_screen == previous_game_screen):
        background_cache['initialized'] = False
    if(not background_cache['initialized']):
        load_background(game_screen)
    game_display.blit(background_cache['background'], (0, 0))