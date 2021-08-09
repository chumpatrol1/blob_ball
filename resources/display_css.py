from resources.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd
cwd = getcwd()

blob_array = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "Quirkless Blob", "No Ability"], ["\\blobs\\fire_blob.png", "Fire Blob", "Fireball"], ["\\blobs\\ice_blob.png", "Ice Blob", "Snowball"], ["\\blobs\\water_blob.png", "Water Blob", "Geyser"], ["\\blobs\\rock_blob.png", "Rock Blob", "Spire"], ["\\blobs\\lightning_blob.png", "Lightning Blob", "Thunderbolt"], ["\\blobs\\wind_blob.png", "Wind Blob", "Gale"],],
[["\\rules_icon.png", "Rules", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\gear_icon.png", "Settings", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\almanac_icon.png", "Almanac", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
]

bic_cached = False
blob_image_cache = [
]

font_cache = {}
token_cache = {}

def load_blobs(blob_image_cache, directory):
    for row in blob_array: #Temporary, until we make more blobs
            blob_image_cache.append([])
            for icon in row:
                blob_image_cache[-1].append(pg.image.load(directory+icon[0]))
    return blob_image_cache

def css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position, settings):
    '''
    Draws the blobs on screen, and handles "mousing over" blobs.
    '''
    global cwd
    global bic_cached
    global blob_image_cache
    x = 0
    y = 0
    directory = cwd + "\\resources\\images"
    if not bic_cached:
        blob_image_cache = load_blobs(blob_image_cache, directory)
        font_cache['blob_name'] = pg.font.Font(cwd + "\\resources\\fonts\\neuropol-x-free.regular.ttf", 50)
        font_cache['blob_description'] = pg.font.Font(cwd + "\\resources\\fonts\\neuropol-x-free.regular.ttf", 30)
        font_cache['ready_confirmation'] = pg.font.Font(cwd + "\\resources\\fonts\\neuropol-x-free.regular.ttf", 80)
        token_cache['p1_ball'] = pg.image.load(cwd + "\\resources\\images\\p1_token.png")
        token_cache['p1_selected'] = pg.image.load(cwd + "\\resources\\images\\p1_check.png")
        token_cache['p2_ball'] = pg.image.load(cwd + "\\resources\\images\\p2_token.png")
        token_cache['p2_selected'] = pg.image.load(cwd + "\\resources\\images\\p2_check.png")
        bic_cached = True
            
    for row in blob_image_cache: #Temporary, until we make more blobs
        y += 1
        for icon in row:
            x += 1
            blob = blob_image_cache[y-1][x-1]
            if(x == 1):
                blob = pg.transform.scale(blob, (screen_size[0]//15, screen_size[0]//15))
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(45/768))))
            else:
                blob = pg.transform.scale(blob, (screen_size[0]//15, screen_size[1]//15))
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(20/768))))
        x = 0
    p1_selected_blob = blob_image_cache[p1_selector_position[1]][p1_selector_position[0]]
    if(p1_selector_position[0] == 0):
        p1_selected_blob = pg.transform.scale(p1_selected_blob, (screen_size[0]//7, screen_size[0]//7))
    else:
        p1_selected_blob = pg.transform.scale(p1_selected_blob, (screen_size[0]//7, screen_size[1]//7))
    p1_selected_blob = p1_selected_blob.convert_alpha()
    if(p1_selector_position[2] == 0):
        p1_selected_blob.set_alpha(200)
    else:
        p1_selected_blob.set_alpha(255)
    p1_selected_blob = pg.transform.flip(p1_selected_blob, True, False)
    game_display.blit(p1_selected_blob, (screen_size[0]/10, screen_size[1]*(3/4)))
    p2_selected_blob = blob_image_cache[p2_selector_position[1]][p2_selector_position[0]]
    if(p2_selector_position[0] == 0):
        p2_selected_blob = pg.transform.scale(p2_selected_blob, (screen_size[0]//7, screen_size[0]//7))
    else:
        p2_selected_blob = pg.transform.scale(p2_selected_blob, (screen_size[0]//7, screen_size[1]//7))
    p2_selected_blob = p2_selected_blob.convert_alpha()
    if(p2_selector_position[2] == 0):
        p2_selected_blob.set_alpha(200)
    else:
        p2_selected_blob.set_alpha(255)
    game_display.blit(p2_selected_blob, (screen_size[0]*(3/4), screen_size[1]*(3/4)))

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
    #back_arrow = pg.image.load(cwd + "\\resources\\images\\back_arrow.png")
    #back_arrow = pg.transform.scale(back_arrow, (screen_size[1]//15, screen_size[1]//15))
    #game_display.blit(back_arrow, (screen_size[0]*(1/8), screen_size[1]//10))
    if(p1_selector_position[2] == 0):
        p1_ball = token_cache['p1_ball']
    else:
        p1_ball = token_cache['p1_selected']
    if(p2_selector_position[2] == 0):
        p2_ball = token_cache['p2_ball']
    else:
        p2_ball = token_cache['p2_selected']

    p1_ball = pg.transform.scale(p1_ball, (screen_size[1]//15, screen_size[1]//15))
    p2_ball = pg.transform.scale(p2_ball, (screen_size[1]//15, screen_size[1]//15))
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