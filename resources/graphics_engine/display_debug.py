import pygame as pg
from os import getcwd
from engine.handle_input import handle_mouse
cwd = getcwd()

def draw_debug(game_display):
    pos, clicked = handle_mouse()
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    text_box = menu_font.render(f"X: {pos[0]}, Y: {pos[1]}, L: {clicked[0]}, R: {clicked[2]}", False, (0, 0, 150))
    text_rect = text_box.get_rect()
    text_rect.topleft = (0, 0)
    game_display.blit(text_box, text_rect)