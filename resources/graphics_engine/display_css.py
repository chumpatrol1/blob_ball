from engine.blobs.get_costumes import species_to_image
from engine.unlocks import return_available_costumes
from resources.graphics_engine.background_handler import draw_background as draw_background
from engine.unlocks import load_blob_unlocks, return_css_display_blobs, update_css_blobs, return_css_selector_blobs
import pygame as pg
from os import getcwd, getenv
cwd = getcwd()
appcwd = getenv('APPDATA')+"\\BlobBall"
print(cwd)
print(appcwd)
blob_array = return_css_display_blobs()


bic_cached = False
name_cache = []
ability_cache = []
blob_image_cache = [
]
ghost_image_cache = []
costume_cache = [[None, None], [None, None]] # P1: [CostumeName, Surface], P2: [CostumeName, Surface]

cursor_cached = False

font_cache = {}
token_cache = {}

def unload_css():
    global bic_cached
    global blob_image_cache
    global ghost_image_cache
    global font_cache
    global token_cache
    bic_cached = False
    blob_image_cache = []
    ghost_image_cache = []
    name_cache = []
    ability_cache = []
    font_cache = {}
    token_cache = {}

def load_blobs(blob_image_cache, ghost_image_cache):
    global name_cache
    global ability_cache
    load_blob_unlocks(appcwd)
    update_css_blobs(appcwd)
    blob_array = return_css_display_blobs()
    #print(return_css_selector_blobs())
    for row in blob_array: #Temporary, until we make more blobs
            blob_image_cache.append([])
            ghost_image_cache.append([])
            name_cache.append([])
            ability_cache.append([])
            for icon in row:
                #blob_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, round(pg.image.load(directory+icon[0]).get_height()*.4636))))
                #ghost_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (195, pg.image.load(directory+icon[0]).get_height())))
                try:
                    loaded_icon = pg.image.load(cwd + "/blobs/" + icon[3] + "/" + icon[0]).convert_alpha()
                except:
                    loaded_icon = pg.image.load(cwd + "/blobs/" + "random" + "/" + "shadow_blob.png")
                blob_image_cache[-1].append(pg.transform.scale(loaded_icon, (2 * loaded_icon.get_width()//3, 2 * loaded_icon.get_height()//3)))
                ghost_image_cache[-1].append(pg.transform.scale(loaded_icon, (2 * loaded_icon.get_width()//3, 2 * loaded_icon.get_height()//3)))
                ghost_image_cache[-1][-1].set_alpha(200)
                name_cache[-1].append(font_cache['blob_name'].render(icon[1], False, (255, 255, 255)))
                ability_cache[-1].append(font_cache['blob_description'].render(icon[2], False, (255, 255, 255)))

    return blob_image_cache, ghost_image_cache

def force_load_blobs():
    global blob_image_cache
    global ghost_image_cache
    global cwd
    #unload_css()
    blob_image_cache, ghost_image_cache = load_blobs(blob_image_cache, ghost_image_cache)
    unload_css()

def load_images_and_fonts(game_display, info_getter):
    global cwd
    global bic_cached
    global blob_image_cache
    global ghost_image_cache
    directory = cwd + "/resources/images"     
    if not bic_cached:

        font_cache['blob_name'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
        font_cache['blob_description'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 15)
        font_cache['ready_confirmation'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
        
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

        token_cache['cpu_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/cpu_icon.png").convert_alpha(), (40, 40))
        
        token_cache['ready_bar'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/ready_bar.png").convert_alpha(), (1366, 39))
        token_cache['ready_bar_glow'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/ready_bar_glow.png").convert_alpha(), (1366, 39))
        token_cache['back_button_glow'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/back_button_glow.png").convert_alpha(), (176, 79))
        token_cache['back_button_glow'].set_alpha(100)
        token_cache['rules_button_glow'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/rules_button_glow.png").convert_alpha(), (886, 79))
        token_cache['rules_button_glow'].set_alpha(100)
        token_cache['almanac_button_glow'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/almanac_button_glow.png").convert_alpha(), (145, 79))
        token_cache['almanac_button_glow'].set_alpha(100)
        token_cache['settings_button_glow'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/settings_button_glow.png").convert_alpha(), (145, 79))
        token_cache['settings_button_glow'].set_alpha(100)

        info_getter[2]['casual_match'].surfaces['idle'] = token_cache['ready_bar']
        info_getter[2]['casual_match'].surfaces['hover'] = token_cache['ready_bar_glow']
        info_getter[2]['main_menu'].surfaces['hover'] = token_cache['back_button_glow']
        info_getter[2]['rules'].surfaces['hover'] = token_cache['rules_button_glow']
        info_getter[2]['almanac'].surfaces['hover'] = token_cache['almanac_button_glow']
        info_getter[2]['settings'].surfaces['hover'] = token_cache['settings_button_glow']
        
        

        token_cache['p1_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p1_box.png").convert_alpha(), (285, 225))
        token_cache['p2_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p2_box.png").convert_alpha(), (285, 225))
        token_cache['p3_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p3_box.png").convert_alpha(), (285, 225))
        token_cache['p4_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/p4_box.png").convert_alpha(), (285, 225))
        token_cache['pcpu_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/pcpu_box.png").convert_alpha(), (285, 225))
        token_cache['pnone_box'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/pnone_box.png").convert_alpha(), (217, 225))
        bic_cached = True

        blob_image_cache, ghost_image_cache = load_blobs(blob_image_cache, ghost_image_cache)

        update_css_blobs(cwd)

def draw_css_buttons_blobs(game_display, info_getter):   
    '''
    Draws the blobs on screen, and handles "mousing over" blobs.
    '''
    global cwd
    global bic_cached
    global blob_image_cache
    global ghost_image_cache
    x = 0
    y = 0
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
            #pg.draw.rect(game_display, color_tuple, (x_align - 2, (100+ (y * 100) - (130)), 137, 100))
            game_display.blit(blob, (x_align, 100+ 768*(y * (100/768)) - (768*(100/768)) - (blob.get_height() - 51)/2))
        x = 0

    for button_key in info_getter[2]:
        button = info_getter[2][button_key]
        if(button.surfaces[button.state]):
            game_display.blit(button.surfaces[button.state], (button.left, button.top))

def draw_rules(game_display, ruleset):
    time_limit_seconds = str((ruleset['time_limit']%3600)//60)
    if(len(time_limit_seconds) == 1):
        time_limit_seconds = "0" + time_limit_seconds

    time_limit_text = " in " + f"{ruleset['time_limit']//3600}:{time_limit_seconds}"
    if(ruleset['time_limit'] == 0):
        time_limit_text = ""

    rules_text = f'Score {ruleset["goal_limit"]} Point{"s" if ruleset["goal_limit"] > 1 else ""}{time_limit_text}!'

    text_box = font_cache['ready_confirmation'].render(rules_text, False, (0, 0, 150))
    text_rect = text_box.get_rect()
    text_rect.topleft = (290, 15)
    game_display.blit(text_box, text_rect)

def draw_css(game_display, info_getter, settings):
    global cwd
    load_images_and_fonts(game_display, info_getter)
    draw_background(game_display, "css", settings)
    draw_rules(game_display, info_getter[3])
    draw_css_buttons_blobs(game_display, info_getter)
    

    if not cursor_cached:
        assign_cursor_images(info_getter[0])
    # Draw Menus
    for player_menu in info_getter[0]:
        if(player_menu == 0):
            continue
        player_menu = info_getter[0][player_menu]
        game_display.blit(player_menu.menu.image_cache[player_menu.token.player_state], (player_menu.menu.x_pos, player_menu.menu.y_pos))
        game_display.blit(token_cache["cpu_icon"], (player_menu.menu.x_pos+240, player_menu.menu.y_pos+150))
    '''game_display.blit(token_cache['p1_ball'], (info_getter[0][1].token.x_pos - 25, info_getter[0][1].token.y_pos - 25))
    game_display.blit(token_cache['p2_ball'], (info_getter[0][2].token.x_pos - 25, info_getter[0][2].token.y_pos - 25))
    game_display.blit(token_cache['p3_ball'], (info_getter[0][3].token.x_pos - 25, info_getter[0][3].token.y_pos - 25))
    game_display.blit(token_cache['p4_ball'], (info_getter[0][4].token.x_pos - 25, info_getter[0][4].token.y_pos - 25))
    '''
    # Draw Cursors
    for index in info_getter[0]:
        if(index == 0):
            break # Should this be a continue?
        player_obj = info_getter[0][index]
        if(player_obj.token.current_blob and player_obj.token.attached_to and not player_obj.token.player_state == 'none'):
            game_display.blit(ghost_image_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x], (player_obj.menu.x_pos + 73, player_obj.menu.y_pos + 100 - (blob_image_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x].get_height() - 51)/2))
            blob_name = name_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x]
            text_rect = blob_name.get_rect()
            text_rect.center = (player_obj.menu.x_pos + 142, player_obj.menu.y_pos + 15)
            game_display.blit(blob_name, text_rect)
            blob_desc = ability_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x]
            text_rect = blob_desc.get_rect()
            text_rect.center = (player_obj.menu.x_pos + 142, player_obj.menu.y_pos + 180)
            game_display.blit(blob_desc, text_rect)
        elif(player_obj.token.current_blob and not player_obj.token.attached_to and not player_obj.token.player_state == 'none'):
            if(player_obj.token.current_costume == 0):
                game_display.blit(blob_image_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x], (player_obj.menu.x_pos + 73, player_obj.menu.y_pos + 100 - (blob_image_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x].get_height() - 51)/2))
            else:
                #print(player_obj.token.current_costume)
                temp_loaded = f"blobs/{player_obj.token.current_blob}/" + species_to_image(player_obj.token.current_blob, player_obj.token.current_costume)["alive"]
                #print(player_obj.token.current_costume)
                #print(temp_loaded)
                if(costume_cache[0][0] != temp_loaded):
                    costume_cache[0][0] = temp_loaded
                    costume_cache[0][1] = pg.image.load(temp_loaded).convert_alpha()
                blob_to_draw = costume_cache[0][1]
                blob_to_draw = pg.transform.scale(blob_to_draw, (2 * blob_to_draw.get_width()//3, 2 * blob_to_draw.get_height()//3))
                game_display.blit(blob_to_draw, (player_obj.menu.x_pos + 73, player_obj.menu.y_pos + 100 - (blob_image_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x].get_height() - 51)/2))
            blob_name = name_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x]
            text_rect = blob_name.get_rect()
            text_rect.center = (player_obj.menu.x_pos + 142, player_obj.menu.y_pos + 15)
            game_display.blit(blob_name, text_rect)
            blob_desc = ability_cache[player_obj.token.current_blob_y][player_obj.token.current_blob_x]
            text_rect = blob_desc.get_rect()
            text_rect.center = (player_obj.menu.x_pos + 142, player_obj.menu.y_pos + 180)
            game_display.blit(blob_desc, text_rect)
    
    # Draw Tokens
    for player_menu in info_getter[0]:
        player_menu = info_getter[0][player_menu]
        token = player_menu.token
        if(token.image_cache[token.player_state]):
            if(token.current_blob and not token.attached_to):
                game_display.blit(token.image_cache[token.player_state + "_select"], (token.x_pos - 25, token.y_pos - 25))
            else:
                game_display.blit(token.image_cache[token.player_state], (token.x_pos - 25, token.y_pos - 25))
    
    #Draw the cursor on top of everything!
    for index in info_getter[0]:
        if(index == 0):
            break # Should this be a continue?
        player_obj = info_getter[0][index]
        game_display.blit(player_obj.cursor.current_image, (player_obj.cursor.x_pos, player_obj.cursor.y_pos))
        

    #css_blobs(game_display, p1_selector_position, p2_selector_position, p1_blob, p2_blob)

def assign_cursor_images(cursor_dict):
    global cursor_cached
    cursor_dict[1].cursor.set_image(token_cache['p1_hand'], token_cache['p1_grab'])
    cursor_dict[2].cursor.set_image(token_cache['p2_hand'], token_cache['p2_grab'])
    #cursor_dict[3].cursor.set_image(token_cache['p3_hand'], token_cache['p3_grab'])
    #cursor_dict[4].cursor.set_image(token_cache['p4_hand'], token_cache['p4_grab'])
    cursor_dict[1].menu.set_image({'human': token_cache['p1_box'], 'cpu': token_cache['pcpu_box'], 'none': token_cache['pnone_box']})
    cursor_dict[2].menu.set_image({'human': token_cache['p2_box'], 'cpu': token_cache['pcpu_box'], 'none': token_cache['pnone_box']})
    #cursor_dict[3].menu.set_image({'human': token_cache['p3_box'], 'cpu': token_cache['pcpu_box'], 'none': token_cache['pnone_box']})
    #cursor_dict[4].menu.set_image({'human': token_cache['p4_box'], 'cpu': token_cache['pcpu_box'], 'none': token_cache['pnone_box']})
    cursor_dict[1].token.set_image({'human': token_cache['p1_ball'], 'human_select': token_cache['p1_selected'], 'cpu': token_cache['cpu1_ball'], 'cpu_select': token_cache['cpu1_selected'], 'none': None})
    cursor_dict[2].token.set_image({'human': token_cache['p2_ball'], 'human_select': token_cache['p2_selected'], 'cpu': token_cache['cpu2_ball'], 'cpu_select': token_cache['cpu2_selected'], 'none': None})
    #cursor_dict[3].token.set_image({'human': token_cache['p3_ball'], 'human_select': token_cache['p3_selected'], 'cpu': token_cache['cpu3_ball'], 'cpu_select': token_cache['cpu3_selected'], 'none': None})
    #cursor_dict[4].token.set_image({'human': token_cache['p4_ball'], 'human_select': token_cache['p4_selected'], 'cpu': token_cache['cpu4_ball'], 'cpu_select': token_cache['cpu4_selected'], 'none': None})
    cursor_cached = True
