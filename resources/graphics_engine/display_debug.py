import pygame as pg
from os import getcwd
from engine.handle_input import handle_mouse
from resources.graphics_engine.handle_screen_size import return_mouse_wh
cwd = getcwd()

debug_dict = {
    'initialized': False,
}

def draw_debug(game_display):
    if not debug_dict['initialized']:
        debug_dict['initialized'] = True
        debug_dict['menu_font'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    pos, clicked, moved = handle_mouse()
    wnh = return_mouse_wh()
    menu_font = debug_dict['menu_font']
    text_box = menu_font.render(f"X: {pos[0]}, Y: {pos[1]}, L: {clicked[0]}, R: {clicked[2]}, W: {wnh[0]}, H: {wnh[1]}", False, (0, 0, 150))
    text_rect = text_box.get_rect()
    text_rect.topleft = (0, 0)
    game_display.blit(text_box, text_rect)