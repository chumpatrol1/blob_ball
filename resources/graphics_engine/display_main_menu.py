from resources.graphics_engine.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd
from engine.debug import get_debug
cwd = getcwd()

font_cache = {'cached': False}
ball = pg.transform.scale(pg.image.load(cwd + "/resources/images/balls/soccer_ball.png"), (76, 76))
text_array = []

def draw_main_menu(game_display, info_getter, settings):
    global menu_font
    if not font_cache['cached']:
        font_cache['menu_font'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
        menu_font = font_cache['menu_font']
        text_array = [
        menu_font.render('Play!', False, (0, 0, 150)),
        menu_font.render('Online', False, (0, 0, 150)),
        menu_font.render('Almanac', False, (0, 0, 150)),
        menu_font.render('Rules', False, (0, 0, 150)),
        menu_font.render('Settings', False, (0, 0, 150)),
        menu_font.render('Medals', False, (0, 0, 150)),
        menu_font.render('Tutorial', False, (0, 0, 150)),
        menu_font.render('Quit', False, (0, 0, 150))
        ]
        if(get_debug):
            text_array[8] = menu_font.render('Debug', False, (150, 0, 0))
    menu_font = font_cache['menu_font']
    selector_position = info_getter[0]
    ruleset = info_getter[1]
    draw_background(game_display, 'main_menu', settings)

    game_display.blit(ball, (850, (76 * selector_position) + 38))

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

    # Version Number
    text_box = menu_font.render(ruleset['version'], False, (0, 0, 150))
    text_rect = text_box.get_rect()
    text_rect.bottomright = (1366, 768)
    game_display.blit(text_box, text_rect)