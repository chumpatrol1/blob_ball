from resources.graphics_engine.background_handler import draw_background as draw_background
from engine.handle_input import return_mapkey_names
import pygame as pg
from os import getcwd
cwd = getcwd()

def draw_splash_screen(game_display, info_getter, settings):
    draw_background(game_display, 'green_background', settings)
    input_keys = return_mapkey_names()

    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
    text_color = (0, 0, 255)
    if(info_getter[0] > 30):
        menu_text = menu_font.render('Press SELECT', False, text_color)
        menu_rect = menu_text.get_rect()
        menu_rect.center = (683, 50)
        game_display.blit(menu_text, menu_rect)

    text_color = (255, 0, 0)
    menu_text = menu_font.render('P1 Controls', False, text_color)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (400, 100)
    game_display.blit(menu_text, menu_rect)

    text_color = (0, 0, 255)
    menu_text = menu_font.render('P2 Controls', False, text_color)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (1000, 100)
    game_display.blit(menu_text, menu_rect)


    text_array = [
        menu_font.render("Up:", False, text_color),
        menu_font.render("Down:", False, text_color),
        menu_font.render("Left:", False, text_color),
        menu_font.render("Right:", False, text_color),
        menu_font.render("Ability/SELECT:", False, text_color),
        menu_font.render("Kick/DESELECT:", False, text_color),
        menu_font.render("Block:", False, text_color),
        menu_font.render("Boost:", False, text_color),
    ]

    text_y = 125
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (60, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 80
    text_color = (255, 0, 0)
    text_array = [
        menu_font.render(input_keys['p1_up'], False, text_color),
        menu_font.render(input_keys['p1_down'], False, text_color),
        menu_font.render(input_keys['p1_left'], False, text_color),
        menu_font.render(input_keys['p1_right'], False, text_color),
        menu_font.render(input_keys['p1_ability'], False, text_color),
        menu_font.render(input_keys['p1_kick'], False, text_color),
        menu_font.render(input_keys['p1_block'], False, text_color),
        menu_font.render(input_keys['p1_boost'], False, text_color),
    ]

    text_y = 125
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (350, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 80
    text_color = (0, 0, 255)
    text_array = [
        menu_font.render(input_keys['p2_up'], False, text_color),
        menu_font.render(input_keys['p2_down'], False, text_color),
        menu_font.render(input_keys['p2_left'], False, text_color),
        menu_font.render(input_keys['p2_right'], False, text_color),
        menu_font.render(input_keys['p2_ability'], False, text_color),
        menu_font.render(input_keys['p2_kick'], False, text_color),
        menu_font.render(input_keys['p2_block'], False, text_color),
        menu_font.render(input_keys['p2_boost'], False, text_color),
    ]

    text_y = 125
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (950, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 80

    '''
    #Information on the buttons
    text_color = (0, 124, 0)
    text_array = [
        menu_font.render("Used for menu navigation and jumping", False, text_color),
        menu_font.render("Used for menu navigation, fast falling, and energy focusing", False, text_color),
        menu_font.render("Used for menu navigation and player movement", False, text_color),
        menu_font.render("Used for menu navigation and player movement", False, text_color),
        menu_font.render("Press to use blob ability, also used as SELECT on menus.", False, text_color),
        menu_font.render("Press to kick, also used as DESELECT on menus", False, text_color),
        menu_font.render("Press to block, stopping the ball and protecting the user", False, text_color),
        menu_font.render("Press to boost, increasing a blob's speed and power", False, text_color),
    ]

    text_y = 110
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (60, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 80

    text_color = (255, 0, 255)
    text_array = [
        menu_font.render("ENTER can be used to SELECT on some menus.", False, text_color),
        menu_font.render("CTRL Toggles Fullscreen mode", False, text_color),
        menu_font.render("ESC Closes the game", False, text_color),
    ]

    text_y = 710
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (60, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 80
    '''