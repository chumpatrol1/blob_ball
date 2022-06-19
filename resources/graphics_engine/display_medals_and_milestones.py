from resources.graphics_engine.background_handler import draw_background as draw_background
from engine.unlocks import load_medal_unlocks, return_mam_display_medals, update_mam_medals
import pygame as pg
from os import getcwd
cwd = getcwd()

medal_array = return_mam_display_medals()

bic_cached = False
medal_image_cache = [
]
big_image_cache = []

font_cache = {}
token_cache = {}

def unload_mam():
    global bic_cached
    global medal_image_cache
    global big_image_cache
    global font_cache
    global token_cache
    bic_cached = False
    medal_image_cache = []
    big_image_cache = []
    font_cache = {}
    token_cache = {}

def load_medals(medal_image_cache, big_image_cache, directory):
    load_medal_unlocks(cwd)
    update_mam_medals(cwd)
    medal_array = return_mam_display_medals()
    for row in medal_array: #Temporary, until we make more medals
            medal_image_cache.append([])
            big_image_cache.append([])
            for icon in row:
                if(medal_image_cache[-1] == []):
                    try:
                        medal_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, 91)))
                        big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (100, 100)))
                    except:
                        print("Medal sprite was not found - failsafe trigger")
                        medal_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+"/medals/404.png").convert_alpha(), (91, 91)))
                        big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+"/medals/404.png").convert_alpha(), (100, 100)))
                else:
                    medal_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, 51)))
                    big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (195, 109)))
    return medal_image_cache, big_image_cache

def force_load_medals():
    global medal_image_cache
    global big_image_cache
    global cwd
    unload_mam()
    directory = cwd + "/resources/images"
    medal_image_cache, big_image_cache = load_medals(medal_image_cache, big_image_cache, directory)
    unload_mam()

def mam_medals(game_display, medal_selector):
    '''
    Draws the medals on screen, and handles "mousing over" blobs.
    '''
    global cwd
    global bic_cached
    global medal_image_cache
    global big_image_cache
    x = 0
    y = 0
    directory = cwd + "/resources/images"
    if not bic_cached:
        medal_image_cache, big_image_cache = load_medals(medal_image_cache, big_image_cache, directory)

        font_cache['medal_name'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
        font_cache['medal_description'] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
        
        token_cache['ball'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_token.png").convert_alpha(), (51, 51))
        token_cache['selected'] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_tokens/p1_check.png").convert_alpha(), (51, 51))
        
        token_cache['ghost'] = token_cache['ball'].convert_alpha()
        token_cache['ghost'].set_alpha(200)
        
        bic_cached = True
            
    for row in medal_image_cache:
        y += 1
        for icon in row:
            x += 1
            medal = medal_image_cache[y-1][x-1]
            if(x == 1):
                game_display.blit(medal, (1366*(x/10)+(1366*(20/1366)), 768*(y * (100/768)) - (768*(45/768))))
            else:
                game_display.blit(medal, (1366*(x/10)+(1366*(20/1366)), 768*(y * (100/768)) - (768*(20/768))))
        x = 0
    
    selected_medal = big_image_cache[medal_selector[1]][medal_selector[0]]
    selected_medal = selected_medal.convert_alpha()
    if(medal_selector[2] == 0):
        selected_medal.set_alpha(200)
    else:
        selected_medal.set_alpha(255)

    selected_medal = pg.transform.flip(selected_medal, True, False)
    if(medal_selector[0] == 0):
        game_display.blit(selected_medal, (191, 576))
    else:
        game_display.blit(selected_medal, (136, 576))


    menu_text = font_cache['medal_name'].render(str(medal_array[medal_selector[1]][medal_selector[0]][1]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (1366//6, 11*768//12)
    game_display.blit(menu_text, text_rect)

    menu_text = font_cache['medal_description'].render(str(medal_array[medal_selector[1]][medal_selector[0]][2]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (1366//6, 24*768//25)
    game_display.blit(menu_text, text_rect)

def draw_mam(game_display, info_getter, settings):
    global cwd
    medal_selector = info_getter[0]
    ghost_position = info_getter[1]

    draw_background(game_display, "mam", settings)
    mam_medals(game_display, medal_selector)

    ball = token_cache['ball']
    game_display.blit(ball, ((136 * (medal_selector[0] + 1) + 1366*(1/135)), 100 * (medal_selector[1] + 1) - 25))
    if(ghost_position is not None and not medal_selector[2]):
        ghost = 'ghost'
        game_display.blit(token_cache[ghost], ((136 * (ghost_position[0] + 1) + 1366*(1/135)), 100 * (ghost_position[1] + 1) - 25))