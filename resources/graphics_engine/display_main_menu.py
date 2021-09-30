from resources.graphics_engine.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd
cwd = getcwd()

def draw_main_menu(screen_size, game_display, selector_position, settings):
    draw_background(game_display, 'main_menu', settings)
    menu_font = pg.font.Font(cwd + "\\resources\\fonts\\neuropol-x-free.regular.ttf", 40)
    text_array = [
        menu_font.render('Play!', False, (0, 0, 150)),
        menu_font.render('Online', False, (0, 0, 150)),
        menu_font.render('Almanac', False, (0, 0, 150)),
        menu_font.render('Rules', False, (0, 0, 150)),
        menu_font.render('Settings', False, (0, 0, 150)),
        menu_font.render('Quit', False, (0, 0, 150))
    ]


    ball = pg.image.load(cwd + "\\resources\\images\\balls\\soccer_ball.png")
    ball = pg.transform.scale(ball, (screen_size[1]//10, screen_size[1]//10))
    game_display.blit(ball, (850, ((screen_size[1]//10) * selector_position) + (0.5 * screen_size[1]//10)))

    text_y = screen_size[1]//10
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (screen_size[0]//2, text_y)
        game_display.blit(text_box, text_rect)
        text_y += screen_size[1]//10