from resources.background_handler import draw_background as draw_background
import pygame as pg
from os import getcwd
cwd = getcwd()

blob_array = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "Quirkless Blob", "No Ability"], ["\\blobs\\fire_blob.png", "Fire Blob", "Fireball"], ["\\blobs\\ice_blob.png", "Ice Blob", "Snowball"], ["\\blobs\\water_blob.png", "Water Blob", "Geyser"], ["\\blobs\\rock_blob.png", "Rock Blob", "Spire"], ["\\blobs\\lightning_blob.png", "Lightning Blob", "Thunderbolt"], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\rules_icon.png", "Rules", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\gear_icon.png", "Settings", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
[["\\back_arrow.png", "Back", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""], ["\\blobs\\quirkless_blob.png", "", ""],],
]

def css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position, settings):
    '''
    Draws the blobs on screen, and handles "mousing over" blobs.
    '''
    global cwd
    
    x = 0
    y = 0
    directory = cwd + "\\resources\\images"
    for row in blob_array: #Temporary, until we make more blobs
        y += 1
        for icon in row:
            x += 1
            blob = pg.image.load(directory + icon[0])
            if(x == 1):
                blob = pg.transform.scale(blob, (screen_size[0]//15, screen_size[0]//15))
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(45/768))))
            else:
                blob = pg.transform.scale(blob, (screen_size[0]//15, screen_size[1]//15))
                game_display.blit(blob, (screen_size[0]*(x/10)+(screen_size[0]*(20/1366)), screen_size[1]*(y * (100/768)) - (screen_size[1]*(20/768))))
        x = 0
    p1_selected_blob = pg.image.load(directory + blob_array[p1_selector_position[1]][p1_selector_position[0]][0])
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
    p2_selected_blob = pg.image.load(directory + blob_array[p2_selector_position[1]][p2_selector_position[0]][0])
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

    menu_font = pg.font.SysFont('Arial', round(50*(screen_size[1]/768)))
    menu_text = menu_font.render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][1]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*screen_size[0]//6, 11*screen_size[1]//12)
    game_display.blit(menu_text, text_rect)
    menu_text = menu_font.render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][1]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//6, 11*screen_size[1]//12)
    game_display.blit(menu_text, text_rect)

    menu_font = pg.font.SysFont('Arial', round(30*(screen_size[1]/768)))
    menu_text = menu_font.render(str(blob_array[p2_selector_position[1]][p2_selector_position[0]][2]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (5*screen_size[0]//6, 24*screen_size[1]//25)
    game_display.blit(menu_text, text_rect)
    menu_text = menu_font.render(str(blob_array[p1_selector_position[1]][p1_selector_position[0]][2]), False, (255, 124, 0))
    text_rect = menu_text.get_rect()
    text_rect.center = (screen_size[0]//6, 24*screen_size[1]//25)
    game_display.blit(menu_text, text_rect)

def draw_casual_css(screen_size, game_display, p1_selector_position, p2_selector_position, settings):
    global cwd
    draw_background(game_display, "casual_css", settings)
    for x in range(0, 8):
        for y in range (0, 5):
            pg.draw.rect(game_display, (255, 255, 255), ((x*screen_size[0]*0.1) + (screen_size[0]/10), (y*screen_size[1]*(100/768))+(screen_size[1]*50/768), screen_size[0]*0.1, screen_size[1]*(100/768)), width = 3)
    css_blobs(screen_size, game_display, p1_selector_position, p2_selector_position, settings)
    #back_arrow = pg.image.load(cwd + "\\resources\\images\\back_arrow.png")
    #back_arrow = pg.transform.scale(back_arrow, (screen_size[1]//15, screen_size[1]//15))
    #game_display.blit(back_arrow, (screen_size[0]*(1/8), screen_size[1]//10))
    if(p1_selector_position[2] == 0):
        p1_ball = pg.image.load(cwd + "\\resources\\images\\p1_token.png")
    else:
        p1_ball = pg.image.load(cwd + "\\resources\\images\\p1_check.png")
    if(p2_selector_position[2] == 0):
        p2_ball = pg.image.load(cwd + "\\resources\\images\\p2_token.png")
    else:
        p2_ball = pg.image.load(cwd + "\\resources\\images\\p2_check.png")

    p1_ball = pg.transform.scale(p1_ball, (screen_size[1]//15, screen_size[1]//15))
    p2_ball = pg.transform.scale(p2_ball, (screen_size[1]//15, screen_size[1]//15))
    game_display.blit(p1_ball, ((screen_size[0]//10 * (p1_selector_position[0] + 1) + screen_size[0]*(1/135)), (screen_size[1]*(100/768)) * (p1_selector_position[1] + 1) - (screen_size[1] * (25/768))))
    game_display.blit(p2_ball, ((screen_size[0]//10 * (p2_selector_position[0] + 1) + screen_size[0]*(8/135)), (screen_size[1]*(100/768)) * (p2_selector_position[1] + 1) - (screen_size[1] * (25/768))))

    if(p1_selector_position[2] >= 1 and p2_selector_position[2] >= 1):
        pg.draw.rect(game_display, (255, 255, 0), (0, screen_size[1]*(2/5), screen_size[0], screen_size[1]/5))
        menu_font = pg.font.SysFont('Arial', round(80*(screen_size[1]/768)))
        menu_text = menu_font.render('CONFIRM READY WITH "ABILITY"', False, (255, 124, 0))
        text_rect = menu_text.get_rect()
        text_rect.center = (screen_size[0]//2, screen_size[1]//2)
        game_display.blit(menu_text, text_rect)
        if(p1_selector_position[2] == 2):
            game_display.blit(p1_ball, ((screen_size[0]*(1/10), screen_size[1]*(2/5))))
        if(p2_selector_position[2] == 2):
            game_display.blit(p2_ball, ((screen_size[0]*(9/10), screen_size[1]*(2/5))))