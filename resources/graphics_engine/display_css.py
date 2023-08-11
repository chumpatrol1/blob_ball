from engine.blobs import species_to_image
from engine.unlocks import return_available_costumes
from resources.graphics_engine.background_handler import draw_background as draw_background
from engine.unlocks import load_blob_unlocks, return_css_display_blobs, update_css_blobs
import pygame as pg
from os import getcwd, getenv
cwd = getcwd()
appcwd = getenv('APPDATA')+"/BlobBall"

blob_array = return_css_display_blobs()

bic_cached = False
blob_image_cache = [
]
big_image_cache = []
costume_cache = [[None, None], [None, None]] # P1: [CostumeName, Surface], P2: [CostumeName, Surface]

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
    font_cache = {}
    token_cache = {}

def load_blobs(blob_image_cache, big_image_cache, directory):
    load_blob_unlocks(appcwd)
    update_css_blobs(appcwd)
    blob_array = return_css_display_blobs()
    for row in blob_array: #Temporary, until we make more blobs
            blob_image_cache.append([])
            big_image_cache.append([])
            for icon in row:
                if(blob_image_cache[-1] == []):
                    blob_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, 91)))
                    big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (100, 100)))
                else:
                    blob_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, round(pg.image.load(directory+icon[0]).get_height()*.4636))))
                    big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (195, pg.image.load(directory+icon[0]).get_height())))
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
        blob_image_cache, big_image_cache = load_blobs(blob_image_cache, big_image_cache, directory)

        font_cache['blob_name'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
        font_cache['blob_description'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
        font_cache['ready_confirmation'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 55)
        
        token_cache['p1_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_token.png").convert_alpha(), (51, 51))
        token_cache['p1_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_check.png").convert_alpha(), (51, 51))
        token_cache['cpu1_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu1_token.png").convert_alpha(), (51, 51))
        token_cache['cpu1_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu1_check.png").convert_alpha(), (51, 51))

        token_cache['p2_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_token.png").convert_alpha(), (51, 51))
        token_cache['p2_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p2_check.png").convert_alpha(), (51, 51))
        token_cache['cpu2_ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu2_token.png").convert_alpha(), (51, 51))
        token_cache['cpu2_selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/cpu2_check.png").convert_alpha(), (51, 51))
        
        token_cache['p1_ghost'] = token_cache['p1_ball'].convert_alpha()
        token_cache['p1_ghost'].set_alpha(200)
        token_cache['p2_ghost'] = token_cache['p2_ball'].convert_alpha()
        token_cache['p2_ghost'].set_alpha(200)

        token_cache['cpu1_ghost'] = token_cache['cpu1_ball'].convert_alpha()
        token_cache['cpu1_ghost'].set_alpha(200)
        token_cache['cpu2_ghost'] = token_cache['cpu2_ball'].convert_alpha()
        token_cache['cpu2_ghost'].set_alpha(200)

        token_cache['red_hands'] = pg.image.load(cwd + "/resources/images/css_icons/lame_cursor.png").convert_alpha()

        token_cache['cpu_icon'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/cpu_icon.png").convert_alpha(), (51, 51))
        
        bic_cached = True
            
    for row in blob_image_cache: #Temporary, until we make more blobs
        y += 1
        for icon in row:
            x += 1
            x_align = 1366*(x/10)+(1366*(20/1366))
            blob = blob_image_cache[y-1][x-1]
            if(x == 1):
                game_display.blit(blob, (x_align, 768*(y * (100/768)) - (768*(45/768))))
            else:
                game_display.blit(blob, (x_align, 768*(y * (100/768)) - (768*(20/768)) - (blob.get_height() - 51)/2))
        x = 0

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
    game_display.blit(token_cache['red_hands'], (info_getter[0][1].cursor.x_pos, info_getter[0][1].cursor.y_pos))
    #css_blobs(game_display, p1_selector_position, p2_selector_position, p1_blob, p2_blob)