from engine.blobs import blob
from resources.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd
cwd = getcwd()

def draw_almanac_main(game_display, selector_position, settings):
    draw_background(game_display, 'almanac', settings)
    menu_font = pg.font.Font(cwd + "\\resources\\fonts\\TX_Jello2.ttf", 50)
    text_array = [
        menu_font.render('Blobs and Info', False, (0, 0, 150)),
        menu_font.render('Medals', False, (0, 0, 150)),
        menu_font.render('Game Statistics', False, (0, 0, 150)),
        menu_font.render('Art', False, (0, 0, 150)),
        menu_font.render('Credits', False, (0, 0, 150)),
        menu_font.render('Back', False, (0, 0, 150))
    ]


    ball = pg.image.load(cwd + "\\resources\\images\\soccer_ball.png")
    ball = pg.transform.scale(ball, (76, 76))
    game_display.blit(ball, (875, ((76 * selector_position) + (0.5 * 76))))

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

def draw_almanac_credits(game_display, settings):
    draw_background(game_display, 'credits', settings)
    menu_font = pg.font.Font(cwd + "\\resources\\fonts\\TX_Jello2.ttf", 40)
    text_array = [
        menu_font.render('Game Developers', False, (0, 0, 150)),
        menu_font.render('Elijah "Chumpatrol1" McLaughlin (Lead Programmer, Lead Designer)', False, (0, 0, 150)),
        menu_font.render('Ellexium (Lead Artist, Programmer)', False, (0, 0, 150)),
        menu_font.render('Zion "Chumpatrol2" McLaughlin (Game Balancer, Bug Hunter)', False, (0, 0, 150)),
        menu_font.render('Yael "Chumpatrol3" McLaughlin (Concept Artist)', False, (0, 0, 150)),
        menu_font.render('NeoPhyte_TPK (Font Contributor, Bug Hunter)', False, (0, 0, 150)),
    ]

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76

def draw_almanac_art(game_display, selector_position, settings):
    draw_background(game_display, 'almanac', settings)
    menu_font = pg.font.Font(cwd + "\\resources\\fonts\\TX_Jello2.ttf", 50)
    text_array = [
        menu_font.render('Backgrounds', False, (0, 0, 150)),
        menu_font.render('Blobs and Icons', False, (0, 0, 150)),
        menu_font.render('Fan Creations', False, (0, 0, 150)),
        menu_font.render('Sound Test', False, (0, 0, 150)),
        menu_font.render('Music Test', False, (0, 0, 150)),
        menu_font.render('Back', False, (0, 0, 150)),
        menu_font.render('Navigate Art Menus with Left and Right', False, (0, 0, 150)),
        menu_font.render('Go back with "Ability" or "Kick"', False, (0, 0, 150)),
        menu_font.render('Sound Menus Unavailable', False, (0, 0, 150)),
    ]


    ball = pg.image.load(cwd + "\\resources\\images\\soccer_ball.png")
    ball = pg.transform.scale(ball, (76, 76))
    game_display.blit(ball, (875, ((76 * selector_position) + (0.5 * 76))))

    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 76
    return

def draw_almanac_backgrounds(game_display, selector_position):
    print(selector_position)
    if(selector_position == 0):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'green_background', settings)
    elif(selector_position == 1):
        settings = {'hd_backgrounds': False,}
        draw_background(game_display, 'casual_match', settings)
    elif(selector_position == 2):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'css', settings)
    elif(selector_position == 3):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'casual_match', settings)
    elif(selector_position == 4):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'rules', settings)
    elif(selector_position == 5):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'settings', settings)
    elif(selector_position == 6):
        settings = {'hd_backgrounds': True,}
        draw_background(game_display, 'almanac', settings)

blob_cached = False
blob_cache = []
def draw_almanac_blobs(game_display, selector_position):
    global blob_cached
    global blob_cache
    if not blob_cached:
        from resources.display_css import load_blobs
        blob_cache = load_blobs(blob_cache, cwd + "\\resources\\images")
        temp_cache = []
        for row in blob_cache:
            temp_cache = temp_cache + row[1:]
        for row in blob_cache:
            temp_cache = temp_cache + [row[0]]
        blob_cache = temp_cache
        blob_cached = True
        
    settings = {'hd_backgrounds': False,}
    draw_background(game_display, 'green_background', settings)
    game_display.blit(blob_cache[selector_position], (200, 200))