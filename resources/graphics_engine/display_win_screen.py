from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_particles import clear_particle_memory as clear_particle_memory
from engine.blobs import species_to_image
from os import getcwd
import pygame as pg
cwd = getcwd()
font_cache = {'initialized': False}
image_cache = {'initialized': False}

def unload_win_screen():
    font_cache = {'initialized': False}
    image_cache = {'initialized': False}

def draw_info_box(game_display, player, game_mode, squad_dict):
    menu_font = font_cache['info_box']
    
    text_color = (255, 255, 0)
    if(game_mode == "classic"):
        info = player.info
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
    elif(game_mode == "squadball"):
        if(player.player == 1):
            blob_count = 0
            for blob_constructor in player.menu.stored_blobs:
                game_display.blit(image_cache[f"p1_blob_{blob_count}"], (50, 380 + 100*blob_count))
                game_display.blit(image_cache["goal_ball"], (240, 390 + 100*blob_count))
                goal_text = menu_font.render('{}'.format(str(squad_dict[player.player][blob_count].info['points_from_goals'])), False, text_color)
                ko_text = menu_font.render('{}'.format(str(squad_dict[player.player][blob_count].info['points_from_kos'])), False, text_color)
                text_rect = goal_text.get_rect()
                text_rect.topleft = (275, 380 + 100*blob_count)
                game_display.blit(goal_text, text_rect)
                game_display.blit(image_cache["dead_blob"], (235, 420 + 100*blob_count))
                text_rect = ko_text.get_rect()
                text_rect.topleft = (275, 410 + 100*blob_count)
                game_display.blit(ko_text, text_rect)
                blob_count += 1
        else:
            blob_count = 0
            for blob_constructor in player.menu.stored_blobs:
                game_display.blit(image_cache[f"p2_blob_{blob_count}"], (775, 380 + 100*blob_count))
                game_display.blit(image_cache["goal_ball"], (940, 390 + 100*blob_count))
                goal_text = menu_font.render('{}'.format(str(squad_dict[player.player][blob_count].info['points_from_goals'])), False, text_color)
                ko_text = menu_font.render('{}'.format(str(squad_dict[player.player][blob_count].info['points_from_kos'])), False, text_color)
                text_rect = goal_text.get_rect()
                text_rect.topleft = (975, 380 + 100*blob_count)
                game_display.blit(goal_text, text_rect)
                game_display.blit(image_cache["dead_blob"], (935, 420 + 100*blob_count))
                text_rect = ko_text.get_rect()
                text_rect.topleft = (975, 410 + 100*blob_count)
                game_display.blit(ko_text, text_rect)
                blob_count += 1

    

def draw_ready_confirmation(game_display, player, ready, x_offset):

    token_tuple = (player.token.player, player.token.is_cpu, ready)
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
    game_stats = info_getter[3]
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
        if(game_stats[0] == "squadball"):
            # Pseudocode
            # Look at each participating player
            # Loop through each blob
            # Save an image of the blob as "p#_blob_x", where # is the player number and x is the blob number
            blob_count = 0
            for blob_constructor in game_stats[2][1].menu.stored_blobs:
                print(blob_constructor)
                blob_file = species_to_image(blob_constructor['blob'], blob_constructor['costume'])
                temp_blob = pg.image.load(blob_file[0])
                image_cache[f"p1_blob_{blob_count}"] = pg.transform.scale(temp_blob,  (2 * temp_blob.get_width()//3, 2 * temp_blob.get_height()//3))
                blob_count += 1
            blob_count = 0
            for blob_constructor in game_stats[2][2].menu.stored_blobs:
                blob_file = species_to_image(blob_constructor['blob'], blob_constructor['costume'])
                temp_blob = pg.image.load(blob_file[0])
                image_cache[f"p2_blob_{blob_count}"] = pg.transform.scale(temp_blob,  (2 * temp_blob.get_width()//3, 2 * temp_blob.get_height()//3))
                blob_count += 1
            image_cache['goal_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/balls/goal_ball.png").convert_alpha(), (30, 30))
            image_cache['dead_blob'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/blobs/quirkless_blob_-1.png").convert_alpha(), (40, 22))
    try:
        #print(*game_stats[2])
        # TODO: Move to own file?
        draw_background(game_display, "win_screen", settings)
        clear_particle_memory()
        menu_font = font_cache['big_text']
        if(game_stats[0] == 3):
            menu_text = menu_font.render("TIE", False, (0, 0, 255))
        else:
            menu_text = menu_font.render("WINNER: "+ str(game_stats[1]), False, (0, 0, 255))

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

        draw_ready_confirmation(game_display, game_stats[2][1], info_getter[0], 150)
        draw_ready_confirmation(game_display, game_stats[2][2], info_getter[1], 1100)

        draw_info_box(game_display, game_stats[2][1], game_stats[0], game_stats[6])
        draw_info_box(game_display, game_stats[2][2], game_stats[0], game_stats[6])
            
        
        #print(info_getter)


    except Exception as ex:
        print('Display Win Screen Ex:', ex)