from resources.graphics_engine.background_handler import draw_background
import pygame as pg
from os import getcwd

cwd = getcwd()
bic_cached = False
blob_image_cache = [
]

blob_array = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["/blobs/quirkless_blob.png", "Quirkless Blob", "quirkless"], ["/blobs/fire_blob.png", "Fire Blob", "fire"], ["/blobs/ice_blob.png", "Ice Blob", "ice"], ["/blobs/water_blob.png", "Water Blob", "water"], ["/blobs/rock_blob.png", "Rock Blob", "rock"], ["/blobs/lightning_blob.png", "Lightning Blob", "lightning"], ["/blobs/wind_blob.png", "Wind Blob", "wind"],],
[["/blobs/judge_blob.png", "Judge Blob", "judge"], ["/blobs/doctor_blob.png", "Doctor Blob", "doctor"], ["/blobs/king_blob.png", "King Blob", "king"], ["/blobs/cop_blob.png", "Cop Blob", "cop"], ["/blobs/boxer_blob.png", "Boxer Blob", "boxer"], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/css_icons/back_arrow.png", "", ""], ["/css_icons/almanac_icon.png", "", ""], ["/css_icons/rules_icon.png", "", ""], ["/css_icons/gear_icon.png", "", ""], ["/css_icons/cpu_icon.png", "", ""],],
] # TODO: Do something about this redundancy

ball = None
ball_state = 'deselected'
mu_chart = None

def load_blobs(blob_image_cache, directory):
    for row in blob_array: #Temporary, until we make more blobs
        blob_image_cache.append([])
        for icon in row:
            blob_image_cache[-1].append(pg.image.load(directory+icon[0]))
    return blob_image_cache

def draw_blob_selector(game_display, info_getter, settings):
    global bic_cached
    global blob_image_cache
    global ball
    global ball_state
    selector_position = info_getter[0]
    ghost_position = info_getter[1]
    directory = cwd + "/resources/images"
    if not bic_cached:
        blob_image_cache = load_blobs(blob_image_cache, directory)
        bic_cached = True
        ball = pg.transform.scale(pg.image.load(directory+"/balls/soccer_ball.png"), (50, 50))
        ghost = ball.convert_alpha()
        ghost.set_alpha(200)

    x = 0
    y = 0
    for row in blob_image_cache[:-1]: #Temporary, until we make more blobs
        for icon in row:
            blob = blob_image_cache[y][x]
            blob = pg.transform.scale(blob, (122, 68))
            game_display.blit(blob, (1366*((x + 0.5)/8)+ 20, ((y + 0.5) * 100)))
            x += 1
        x = 0
        y += 1
    if(selector_position[2] == 1 and ball_state == "deselected"):
        ball_state = "selected"
        ball = ball = pg.transform.scale(pg.image.load(directory+"/balls/goal_ball.png"), (50, 50))
    if(selector_position[2] == 0 and ball_state == "selected"):
        ball_state = "deselected"
        ball = pg.transform.scale(pg.image.load(directory+"/balls/soccer_ball.png"), (50, 50))
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    if(selector_position[2] == 1):
        mu_chart_text = "Cloud strife my baby" # But Gucci is my real baby... poor puppy :,(
        
        text_x = 170
        text_y = 130
        for row in mu_chart_text:
            for mu in row:
                text_box = menu_font.render(mu, False, (255, 255, 255))
                text_rect = text_box.get_rect()
                text_rect.center = (text_x, text_y)
                game_display.blit(text_box, text_rect)
                text_x += 170
            text_y += 100
            text_x = 170
    game_display.blit(ball, ((selector_position[0] + 0.85) * 170, (selector_position[1] + 0.5) * 100))
    if(ghost_position is not None and ghost_position != selector_position[:2]):
        game_display.blit(ghost, ((ghost_position[0] + 0.85) * 170, (ghost_position[1] + 0.5) * 100))
    game_display.blit(blob_image_cache[selector_position[1]][selector_position[0]], (825, 575))

    text_array = [
        menu_font.render("INSTRUCTIONS: Use movement keys", False, (0, 0, 255)),
        menu_font.render("to navigate the screen. Press", False, (0, 0, 255)),
        menu_font.render("Ability/Select to view the winrate", False, (0, 0, 255)),
        menu_font.render("of a blob compared to others.", False, (0, 0, 255)),
        menu_font.render("Select the middlemost blob to return", False, (0, 0, 255)),
        menu_font.render("   to the almanac.", False, (0, 0, 255)),
    ]

    text_y = 530
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 30

    text_box = menu_font.render(blob_array[selector_position[1]][selector_position[0]][1], False, (0, 0, 255))
    text_rect = text_box.get_rect()
    text_rect.center = (925, 700)
    game_display.blit(text_box, text_rect)

def draw_blob_info(game_display, info_getter, settings):
    draw_background(game_display, 'green_background', settings)
    draw_blob_info(game_display, info_getter, settings)