from engine.blobs import species_to_image
from engine.unlocks import return_available_costumes
from resources.graphics_engine.background_handler import draw_background as draw_background
from engine.unlocks import load_blob_unlocks, return_css_display_blobs, update_css_blobs, return_css_selector_blobs
import pygame as pg
from os import getcwd, getenv
cwd = getcwd()
appcwd = getenv('APPDATA')+"/BlobBall"

blob_array = return_css_display_blobs()


bic_cached = False
name_cache = []
ability_cache = []
blob_image_cache = [
]
big_image_cache = []
costume_cache = [[None, None], [None, None]] # P1: [CostumeName, Surface], P2: [CostumeName, Surface]

cursor_cached = False

font_cache = {}
token_cache = {}

def unload_css():
    global bic_cached
    global blob_image_cache
    global big_image_cache
    global font_cache
    global token_cache
    bic_cached = False
    blob_image_cache = []
    big_image_cache = []
    name_cache = []
    ability_cache = []
    font_cache = {}
    token_cache = {}

def load_blobs(blob_image_cache, big_image_cache, directory):
    global name_cache
    global ability_cache
    load_blob_unlocks(appcwd)
    update_css_blobs(appcwd)
    blob_array = return_css_display_blobs()
    #print(return_css_selector_blobs())
    for row in blob_array: #Temporary, until we make more blobs
            blob_image_cache.append([])
            big_image_cache.append([])
            name_cache.append([])
            ability_cache.append([])
            for icon in row:
                #blob_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, round(pg.image.load(directory+icon[0]).get_height()*.4636))))
                #big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (195, pg.image.load(directory+icon[0]).get_height())))
                loaded_icon = pg.image.load(directory+icon[0]).convert_alpha()
                blob_image_cache[-1].append(pg.transform.scale(loaded_icon, (2 * loaded_icon.get_width()//3, 2 * loaded_icon.get_height()//3)))
                name_cache[-1].append(font_cache['blob_name'].render(icon[1], False, (255, 255, 255)))
                ability_cache[-1].append(font_cache['blob_description'].render(icon[2], False, (255, 255, 255)))

    return blob_image_cache, big_image_cache

def force_load_blobs():
    global blob_image_cache
    global big_image_cache
    global cwd
    unload_css()
    directory = cwd + "/resources/images"
    blob_image_cache, big_image_cache = load_blobs(blob_image_cache, big_image_cache, directory)
    unload_css()

def css_blobs(game_display):
    '''
    Draws the blobs on screen, and handles "mousing over" blobs.
    '''
    global cwd
    global bic_cached
    global blob_image_cache
    global big_image_cache
    x = 0
    y = 0
    directory = cwd + "/resources/images"
    if not bic_cached:

        font_cache['blob_name'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
        font_cache['blob_description'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 15)
        font_cache['ready_confirmation'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 55)
        
        token_cache['p1_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_token.png").convert_alpha(), (51, 51))
        token_cache['p1_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_check.png").convert_alpha(), (51, 51))
        token_cache['cpu1_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu1_token.png").convert_alpha(), (51, 51))
        token_cache['cpu1_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu1_check.png").convert_alpha(), (51, 51))

        token_cache['p2_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_token.png").convert_alpha(), (51, 51))
        token_cache['p2_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_check.png").convert_alpha(), (51, 51))
        token_cache['cpu2_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu2_token.png").convert_alpha(), (51, 51))
        token_cache['cpu2_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu2_check.png").convert_alpha(), (51, 51))
        
        token_cache['p3_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p3_token.png").convert_alpha(), (51, 51))
        token_cache['p3_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p3_check.png").convert_alpha(), (51, 51))
        token_cache['cpu3_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu3_token.png").convert_alpha(), (51, 51))
        token_cache['cpu3_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu3_check.png").convert_alpha(), (51, 51))
        
        token_cache['p4_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p4_token.png").convert_alpha(), (51, 51))
        token_cache['p4_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p4_check.png").convert_alpha(), (51, 51))
        token_cache['cpu4_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu4_token.png").convert_alpha(), (51, 51))
        token_cache['cpu4_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu4_check.png").convert_alpha(), (51, 51))
        

        token_cache['p1_ghost'] = token_cache['p1_ball'].convert_alpha()
        token_cache['p1_ghost'].set_alpha(200)
        token_cache['p2_ghost'] = token_cache['p2_ball'].convert_alpha()
        token_cache['p2_ghost'].set_alpha(200)

        token_cache['cpu1_ghost'] = token_cache['cpu1_ball'].convert_alpha()
        token_cache['cpu1_ghost'].set_alpha(200)
        token_cache['cpu2_ghost'] = token_cache['cpu2_ball'].convert_alpha()
        token_cache['cpu2_ghost'].set_alpha(200)

        token_cache['p1_hand'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_hand.png").convert_alpha(), (128, 128))
        token_cache['p2_hand'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_hand.png").convert_alpha(), (128, 128))
        token_cache['p3_hand'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p3_hand.png").convert_alpha(), (128, 128))
        token_cache['p4_hand'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p4_hand.png").convert_alpha(), (128, 128))
        token_cache['p1_grab'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_grab.png").convert_alpha(), (128, 128))
        token_cache['p2_grab'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_grab.png").convert_alpha(), (128, 128))
        token_cache['p3_grab'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p3_grab.png").convert_alpha(), (128, 128))
        token_cache['p4_grab'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p4_grab.png").convert_alpha(), (128, 128))

        token_cache['cpu_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/cpu_icon.png").convert_alpha(), (80, 80))
        
        token_cache['ready_bar'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/ready_bar.png").convert_alpha(), (1366, 39))
        token_cache['p1_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p1_box.png").convert_alpha(), (217, 225))
        token_cache['p2_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p2_box.png").convert_alpha(), (217, 225))
        token_cache['p3_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p3_box.png").convert_alpha(), (217, 225))
        token_cache['p4_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p4_box.png").convert_alpha(), (217, 225))
        token_cache['pcpu_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/pcpu_box.png").convert_alpha(), (217, 225))
        token_cache['pnone_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/pnone_box.png").convert_alpha(), (217, 225))
        bic_cached = True

        blob_image_cache, big_image_cache = load_blobs(blob_image_cache, big_image_cache, directory)

        update_css_blobs(cwd)
            
    for row in blob_image_cache: #Temporary, until we make more blobs
        y += 1
        for icon in row:
            x += 1
            x_align = 1366*(x/10)-(1366*(50/1366))
            blob = blob_image_cache[y-1][x-1]
            red = x * 25
            green = y * 60
            color_tuple = (red, green, 0, 255)
            #print(color_tuple)
            #print((100+ 768*(y * (100/768)) - (768*(100/768)) - (blob.get_height() - 51)/2))
            #pg.draw.rect(game_display, color_tuple, (x_align, (100+ 768*(y * (100/768)) - (768*(130/768))), 133, 95))
            pg.draw.rect(game_display, color_tuple, (x_align - 2, (100+ (y * 100) - (130)), 137, 100))
            game_display.blit(blob, (x_align, 100+ 768*(y * (100/768)) - (768*(100/768)) - (blob.get_height() - 51)/2))
        x = 0

    game_display.blit(token_cache['ready_bar'], (0, 470))
    game_display.blit(token_cache['p1_box'], (85, 525))
    game_display.blit(token_cache['cpu_icon'], (300, 680))
    game_display.blit(token_cache['p2_box'], (412, 525))
    game_display.blit(token_cache['cpu_icon'], (627, 680))
    game_display.blit(token_cache['p3_box'], (739, 525))
    #game_display.blit(token_cache['pcpu_box'], (739, 525))
    game_display.blit(token_cache['cpu_icon'], (954, 680))
    game_display.blit(token_cache['p4_box'], (1067, 525))
    #game_display.blit(token_cache['pnone_box'], (1067, 525))
    game_display.blit(token_cache['cpu_icon'], (1282, 680))

    '''if(not p1_selector_position[4]):
        p1_selected_blob = big_image_cache[p1_selector_position[1]][p1_selector_position[0]]
    else:
        # TODO: Check costume thing
        temp_loaded = species_to_image(p1_blob, return_available_costumes()[p1_blob][p1_selector_position[4]])[0]
        if(costume_cache[0][0] != temp_loaded):
            costume_cache[0][0] = temp_loaded
            costume_cache[0][1] = pg.transform.scale(pg.image.load(temp_loaded).convert_alpha(), (195, pg.image.load(temp_loaded).get_height()))
        p1_selected_blob = costume_cache[0][1]
    p1_selected_blob = p1_selected_blob.convert_alpha()
    if(p1_selector_position[2] == 0):
        p1_selected_blob.set_alpha(200)
    else:
        p1_selected_blob.set_alpha(255)

    p1_selected_blob = pg.transform.flip(p1_selected_blob, True, False)
    if(p1_selector_position[0] == 0):
        game_display.blit(p1_selected_blob, (191, 576))
    else:
        game_display.blit(p1_selected_blob, (136, 576 - (p1_selected_blob.get_height()-110)/2))

    if(p1_selector_position[3] == 1):
        game_display.blit(token_cache['cpu_icon'], (75, 575))

    if(not p2_selector_position[4]):
        p2_selected_blob = big_image_cache[p2_selector_position[1]][p2_selector_position[0]]
    else:
        # TODO: Check costume thing
        temp_loaded = species_to_image(p2_blob, return_available_costumes()[p2_blob][p2_selector_position[4]])[0]
        if(costume_cache[1][0] != temp_loaded):
            costume_cache[1][0] = temp_loaded
            costume_cache[1][1] = pg.transform.scale(pg.image.load(temp_loaded).convert_alpha(), (195, pg.image.load(temp_loaded).get_height()))
        p2_selected_blob = costume_cache[1][1]
    p2_selected_blob = p2_selected_blob.convert_alpha()
    if(p2_selector_position[2] == 0):
        p2_selected_blob.set_alpha(200)
    else:
        p2_selected_blob.set_alpha(255)

    if(p2_selector_position[0] == 0):
        game_display.blit(p2_selected_blob, (1079, 576))
    else:
        game_display.blit(p2_selected_blob, (1024, 576 - (p2_selected_blob.get_height()-110)/2))

    if(p2_selector_position[3] == 1):
        game_display.blit(token_cache['cpu_icon'], (1225, 575))'''


    '''menu_text = font_cache['blob_name'].render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][1]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*1366//6, 11*768//12)
    game_display.blit(menu_text, text_rect)
    menu_text = font_cache['blob_name'].render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][1]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (1366//6, 11*768//12)
    game_display.blit(menu_text, text_rect)

    menu_text = font_cache['blob_description'].render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][2]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*1366//6, 24*768//25)
    game_display.blit(menu_text, text_rect)
    menu_text = font_cache['blob_description'].render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][2]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (1366//6, 24*768//25)
    game_display.blit(menu_text, text_rect)'''

def draw_css(game_display, info_getter, settings):
    global cwd

    draw_background(game_display, "css", settings)
    css_blobs(game_display)

    game_display.blit(token_cache['p1_ball'], (info_getter[0][1].token.x_pos - 25, info_getter[0][1].token.y_pos - 25))
    game_display.blit(token_cache['p2_ball'], (info_getter[0][2].token.x_pos - 25, info_getter[0][2].token.y_pos - 25))
    game_display.blit(token_cache['p3_ball'], (info_getter[0][3].token.x_pos - 25, info_getter[0][3].token.y_pos - 25))
    game_display.blit(token_cache['p4_ball'], (info_getter[0][4].token.x_pos - 25, info_getter[0][4].token.y_pos - 25))
    

    if not cursor_cached:
        assign_cursor_images(info_getter[0])
    for index in info_getter[0]:
        if(index == 0):
            break # Should this be a continue?
        player_obj = info_getter[0][index]
        game_display.blit(player_obj.cursor.current_image, (player_obj.cursor.x_pos, player_obj.cursor.y_pos))
        if(player_obj.token.current_blob):
            game_display.blit(blob_image_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x], (player_obj.menu.x_pos + 40, player_obj.menu.y_pos + 100 - (blob_image_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x].get_height() - 51)/2))
            blob_name = name_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x]
            text_rect = blob_name.get_rect()
            text_rect.center = (player_obj.menu.x_pos + 109, player_obj.menu.y_pos + 15)
            game_display.blit(blob_name, text_rect)
            blob_desc = ability_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x]
            text_rect = blob_desc.get_rect()
            text_rect.center = (player_obj.menu.x_pos + 109, player_obj.menu.y_pos + 180)
            game_display.blit(blob_desc, text_rect)

    #css_blobs(game_display, p1_selector_position, p2_selector_position, p1_blob, p2_blob)

def assign_cursor_images(cursor_dict):
    global cursor_cached
    cursor_dict[1].cursor.set_image(token_cache['p1_hand'], token_cache['p1_grab'])
    cursor_dict[2].cursor.set_image(token_cache['p2_hand'], token_cache['p2_grab'])
    cursor_dict[3].cursor.set_image(token_cache['p3_hand'], token_cache['p3_grab'])
    cursor_dict[4].cursor.set_image(token_cache['p4_hand'], token_cache['p4_grab'])

    cursor_cached = True