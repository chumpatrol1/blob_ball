from resources.graphics_engine.background_handler import draw_background as draw_background
from engine.handle_input import return_mapkey_names
import pygame as pg
from os import getcwd
cwd = getcwd()
blob_cwd = cwd + "/resources/images/blobs/"

old_pop_up = None
pop_up_image = None
pop_up_timer = 0

def draw_pop_up(game_display, info_getter, settings):
    draw_background(game_display, 'green_background', settings)
    global old_pop_up
    global pop_up_image
    global pop_up_timer
    if(pop_up_timer):
        pop_up_timer -= 1

    if not(old_pop_up == info_getter):
        old_pop_up = info_getter
        pop_up_timer = 2
    
    if(pop_up_timer == 1):
        pop_up_image = pg.image.load(blob_cwd+info_getter[0]).convert_alpha()

    if(pop_up_image is not None):
        game_display.blit(pop_up_image, (683 - pop_up_image.get_width()//2, 250 - pop_up_image.get_height()//2))

    big_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 80)
    text_color = (0, 0, 255)
    menu_text = "" 
    if(info_getter is not None):
        temp_dict = {
            0: "Blob Unlocked!",
        }
        menu_text = temp_dict[info_getter[3]]

    menu_text = big_font.render(menu_text, False, text_color)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (683, 100)
    game_display.blit(menu_text, menu_rect)

    menu_text = ""
    if(info_getter is not None):
        menu_text = info_getter[1]
    menu_text = big_font.render(menu_text, False, text_color)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (683, 450)
    game_display.blit(menu_text, menu_rect)

    small_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
    text_array = []
    try:
        for i in info_getter[2].split("/"):
            text_array.append(small_font.render(i, False, text_color))
    except:
        pass

    text_y = 525
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 50