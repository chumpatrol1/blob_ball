from resources.graphics_engine.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd
cwd = getcwd()

blob_array = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["/back_arrow.png", "Back", ""], ["/blobs/quirkless_blob.png", "Quirkless Blob", "No Ability"], ["/blobs/fire_blob.png", "Fire Blob", "Fireball"], ["/blobs/ice_blob.png", "Ice Blob", "Snowball"], ["/blobs/water_blob.png", "Water Blob", "Geyser"], ["/blobs/rock_blob.png", "Rock Blob", "Spire"], ["/blobs/lightning_blob.png", "Lightning Blob", "Thunderbolt"], ["/blobs/wind_blob.png", "Wind Blob", "Gale"],],
[["/rules_icon.png", "Rules", ""], ["/blobs/judge_blob.png", "Judge Blob", "C&D"], ["/blobs/doctor_blob.png", "Doctor Blob", "Pill"], ["/blobs/king_blob.png", "King Blob", "Tax"], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/gear_icon.png", "Settings", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/almanac_icon.png", "Almanac", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/cpu_icon.png", "Toggle CPU", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
]

bic_cached = False
blob_image_cache = [
]
big_image_cache = []

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
    for row in blob_array: #Temporary, until we make more blobs
            blob_image_cache.append([])
            big_image_cache.append([])
            for icon in row:
                if(blob_image_cache[-1] == []):
                    blob_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, 91)))
                    big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (100, 100)))
                else:
                    blob_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (91, 51)))
                    big_image_cache[-1].append(pg.transform.scale(pg.image.load(directory+icon[0]).convert_alpha(), (195, 109)))
    return blob_image_cache, big_image_cache

def css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position, settings):
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
        bic_cached = True
            
    for row in blob_image_cache: #Temporary, until we make more blobs
        y += 1
        for icon in row:
            x += 1
            blob = blob_image_cache[y-1][x-1]
            if(x == 1):
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(45/768))))
            else:
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(20/768))))
        x = 0
    
    p1_selected_blob = big_image_cache[p1_selector_position[1]][p1_selector_position[0]]
    p1_selected_blob = p1_selected_blob.convert_alpha()
    if(p1_selector_position[2] == 0):
        p1_selected_blob.set_alpha(200)
    else:
        p1_selected_blob.set_alpha(255)

    p1_selected_blob = pg.transform.flip(p1_selected_blob, True, False)
    if(p1_selector_position[0] == 0):
        game_display.blit(p1_selected_blob, (191, 576))
    else:
        game_display.blit(p1_selected_blob, (136, 576))

    if(p1_selector_position[3] == 0):
        menu_text = font_cache['blob_description'].render('Human', False, (50, 50, 255))
    else:
        menu_text = font_cache['blob_description'].render('CPU', False, (50, 50, 255))

    text_rect = menu_text.get_rect()
    text_rect.center = (75, 650)
    game_display.blit(menu_text, text_rect)

    p2_selected_blob = big_image_cache[p2_selector_position[1]][p2_selector_position[0]]
    p2_selected_blob = p2_selected_blob.convert_alpha()
    if(p2_selector_position[2] == 0):
        p2_selected_blob.set_alpha(200)
    else:
        p2_selected_blob.set_alpha(255)

    if(p2_selector_position[0] == 0):
        game_display.blit(p2_selected_blob, (1079, 576))
    else:
        game_display.blit(p2_selected_blob, (1024, 576))

    if(p2_selector_position[3] == 0):
        menu_text = font_cache['blob_description'].render('Human', False, (50, 50, 255))
    else:
        menu_text = font_cache['blob_description'].render('CPU', False, (50, 50, 255))

    text_rect = menu_text.get_rect()
    text_rect.center = (1291, 650)
    game_display.blit(menu_text, text_rect)

    menu_text = font_cache['blob_name'].render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][1]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*screen_size[0]//6, 11*screen_size[1]//12)
    game_display.blit(menu_text, text_rect)
    menu_text = font_cache['blob_name'].render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][1]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//6, 11*screen_size[1]//12)
    game_display.blit(menu_text, text_rect)

    menu_text = font_cache['blob_description'].render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][2]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*screen_size[0]//6, 24*screen_size[1]//25)
    game_display.blit(menu_text, text_rect)
    menu_text = font_cache['blob_description'].render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][2]), False, (50, 50, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//6, 24*screen_size[1]//25)
    game_display.blit(menu_text, text_rect)

def draw_css(screen_size, game_display, p1_selector_position, p2_selector_position, settings):
    global cwd
    draw_background(game_display, "css", settings)
    css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position, settings)
    #back_arrow = pg.image.load(cwd + "/resources/images/back_arrow.png")
    #back_arrow = pg.transform.scale(back_arrow, (screen_size[1]//15, screen_size[1]//15))
    #game_display.blit(back_arrow, (screen_size[0]*(1/8), screen_size[1]//10))
    if(not p1_selector_position[3]): #Are we a CPU?
        if(p1_selector_position[2] == 0):
            p1_ball = token_cache['p1_ball']
        else:
            p1_ball = token_cache['p1_selected']
    else:
        if(p1_selector_position[2] == 0):
            p1_ball = token_cache['cpu1_ball']
        else:
            p1_ball = token_cache['cpu1_selected']

    if(not p2_selector_position[3]):
        if(p2_selector_position[2] == 0):
            p2_ball = token_cache['p2_ball']
        else:
            p2_ball = token_cache['p2_selected']
    else:
        if(p2_selector_position[2] == 0):
            p2_ball = token_cache['cpu2_ball']
        else:
            p2_ball = token_cache['cpu2_selected']

    game_display.blit(p1_ball, ((screen_size[0]//10 * (p1_selector_position[0] + 1) + screen_size[0]*(1/135)), (screen_size[1]*(100/768)) * (p1_selector_position[1] + 1) - (screen_size[1] * (25/768))))
    game_display.blit(p2_ball, ((screen_size[0]//10 * (p2_selector_position[0] + 1) + screen_size[0]*(8/135)), (screen_size[1]*(100/768)) * (p2_selector_position[1] + 1) - (screen_size[1] * (25/768))))

    if(p1_selector_position[2] >= 1 and p2_selector_position[2] >= 1):
        pg.draw.rect(game_display, (255, 255, 0), (0, screen_size[1]*(2/5), screen_size[0], screen_size[1]/5))
        menu_font = font_cache['ready_confirmation']
        menu_text = menu_font.render('CONFIRM READY WITH "ABILITY"', False, (50, 50, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]//2, screen_size[1]//2)
        game_display.blit(menu_text, text_rect)
        if(p1_selector_position[2] == 2):
            game_display.blit(p1_ball, ((screen_size[0]*(1/10), screen_size[1]*(2/5))))
        if(p2_selector_position[2] == 2):
            game_display.blit(p2_ball, ((screen_size[0]*(9/10), screen_size[1]*(2/5))))