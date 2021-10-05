from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_particles import clear_particle_memory as clear_particle_memory
from os import getcwd
import pygame as pg
cwd = getcwd()
font_cache = {'initialized': False}
image_cache = {'initialized': False}


def draw_info_box(game_display, player):
    menu_font = font_cache['info_box']
    info = player.info
    text_color = (255, 255, 0)
    text_array = [
        menu_font.render('Points from Goals: {}'.format(str(info['points_from_goals'])), False, text_color),
        menu_font.render('Points from KO\'s: {}'.format(str(info['points_from_kos'])), False, text_color),
        menu_font.render('Kick Count: {}'.format(str(info['kick_count'])), False, text_color),
        menu_font.render('Block Count: {}'.format(str(info['block_count'])), False, text_color),
        menu_font.render('Boost Count: {}'.format(str(info['boost_count'])), False, text_color),
        menu_font.render('Parries: {}'.format(str(info['parries'])), False, text_color),
        menu_font.render('Jumps: {}'.format(str(info['jumps'])), False, text_color),
    ]

    text_y = 380
    text_x = 50
    if(player.player == 2):
        text_x = 775
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (text_x, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 50

def draw_ready_confirmation(game_display, player, ready, x_offset):

    token_tuple = (player.player, player.is_cpu, ready)
    token_dict = {
        (1, False, False): 'p1_ball',
        (1, False, True): 'p1_selected',
        (1, True, False): 'cpu1_ball',
        (1, True, True): 'cpu1_selected',
        (2, False, False): 'p2_ball',
        (2, False, True): 'p2_selected',
        (2, True, False): 'cpu2_ball',
        (2, True, True): 'cpu2_selected',
    }
    used_token = token_dict[token_tuple]
    game_display.blit(image_cache[used_token], (x_offset, 250))

def draw_win_screen(game_display, info_getter, settings):
    if(not font_cache['initialized']):
        font_cache['initialized'] = True
        font_cache['info_box'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 38)
        font_cache['big_text'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 50)
    if(not image_cache['initialized']):
        image_cache['initialized'] = True
        token_size = (100, 100)
        image_cache['p1_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_token.png").convert_alpha(), (100, 100))
        image_cache['p1_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_check.png").convert_alpha(), (100, 100))
        image_cache['cpu1_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu1_token.png").convert_alpha(), (100, 100))
        image_cache['cpu1_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu1_check.png").convert_alpha(), (100, 100))

        image_cache['p2_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_token.png").convert_alpha(), (100, 100))
        image_cache['p2_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_check.png").convert_alpha(), (100, 100))
        image_cache['cpu2_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu2_token.png").convert_alpha(), (100, 100))
        image_cache['cpu2_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu2_check.png").convert_alpha(), (100, 100))

    try:
        game_stats = info_getter[3]
        # TODO: Move to own file?
        draw_background(game_display, "win_screen", settings)
        clear_particle_memory()
        menu_font = font_cache['big_text']
        if(game_stats[0] == 3):
            menu_text = menu_font.render("TIE", False, (0, 0, 255))
        else:
            menu_text = menu_font.render("WINNER: "+ str(game_stats[0]), False, (0, 0, 255))

        text_rect = menu_text.get_rect()
        text_rect.center = (683, 60)
        game_display.blit(menu_text, text_rect)

        menu_text = menu_font.render("TIME TAKEN: "+ str(game_stats[5]), False, (0, 0, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (683, 110)
        game_display.blit(menu_text, text_rect)

        menu_text = menu_font.render(f"SCORE: {game_stats[4][0]}-{game_stats[4][1]}", False, (0, 0, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (683, 170)
        game_display.blit(menu_text, text_rect)

        if(info_getter[2] > 45):
            menu_text = menu_font.render("PRESS ABILITY/ENTER", False, (0, 0, 255))
            text_rect = menu_text.get_rect()
            text_rect.center = (683, 290)
            game_display.blit(menu_text, text_rect)
        
        draw_ready_confirmation(game_display, game_stats[1], info_getter[0], 150)
        draw_ready_confirmation(game_display, game_stats[2], info_getter[1], 1100)

        draw_info_box(game_display, game_stats[1])
        draw_info_box(game_display, game_stats[2])
        
        #print(info_getter)


    except Exception as ex:
        print('Display Win Screen Ex:', ex)