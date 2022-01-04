from resources.graphics_engine.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd
cwd = getcwd()

menu_asset_cache = {
'ball': pg.transform.scale(pg.image.load(cwd + "/resources/images/balls/soccer_ball.png"), (76, 76)),
'initialized': False,
}

def draw_main_menu(game_display, info_getter, settings):    
    if not menu_asset_cache['initialized']:
        menu_asset_cache['font'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
        menu_asset_cache['initialized'] = True


    menu_font = menu_asset_cache['font']
    text_array = [
        menu_font.render('Play!', False, (0, 0, 150)),
        menu_font.render('Online', False, (0, 0, 150)),
        menu_font.render('Almanac', False, (0, 0, 150)),
        menu_font.render('Rules', False, (0, 0, 150)),
        menu_font.render('Settings', False, (0, 0, 150)),
        menu_font.render('Quit', False, (0, 0, 150))
    ]

    selector_position = info_getter[0]
    ruleset = info_getter[1]
    draw_background(game_display, 'main_menu', settings)

    ball = menu_asset_cache['ball']
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

