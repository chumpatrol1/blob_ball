from resources.graphics_engine.background_handler import draw_background
from resources.graphics_engine.display_almanac import load_mu_chart
from engine.popup_list import find_blob_unlock
from engine.blob_stats import species_to_stars
from engine.blob_tips import return_selected_blob_tips
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
ghost = None
ball_state = 'deselected'
mu_chart = None

def load_blobs(blob_image_cache, directory): # TODO: Add mini cache with minified blobs
    for row in blob_array: #Temporary, until we make more blobs
        blob_image_cache.append([])
        for icon in row:
            blob_image_cache[-1].append(pg.image.load(directory+icon[0]))
    return blob_image_cache


# TODO: Create a load blob info cache function accessible by blob_info_menu
# It should load: Matchup Chart info (at least for this blob), 
# the Blob Popup (which we can grab from popup_list.py),
# Blob Hard Stats (Speed, Traction, Friction etc.)
# Tips (I'll probably make a tip_list.py file)
# Alternate costume images (if they have any... we'll work on those in a future update)
selected_blob = None
selected_blob_image = None
selected_blob_matchups = None
selected_blob_description = None
selected_blob_stars = None
selected_blob_tips = None
selected_blob_costumes = None
def load_individual_blob(selector_position):
    # Done based off of the selector position - this function only gets called by blob_info_menu.py
    global selected_blob
    global selected_blob_image
    global selected_blob_matchups
    global selected_blob_description
    global selected_blob_stars
    global selected_blob_tips
    selected_blob = blob_array[selector_position[1]][selector_position[0]]
    if(selected_blob[1] == ''):
        selector_position = [0, 0, 1]
        selected_blob = blob_array[selector_position[1]][selector_position[0]]
    selected_blob_image = pg.image.load(cwd + "/resources/images" + selected_blob[0])
    selected_blob_matchups = load_mu_chart()[selected_blob[2]]
    selected_blob_description = find_blob_unlock(selected_blob[2])[2]
    selected_blob_stars = species_to_stars(selected_blob[2], {})
    selected_blob_tips = return_selected_blob_tips(selected_blob[2])
    #print(selected_blob_stars)
    

def draw_blob_selector(game_display, info_getter, settings):
    global bic_cached
    global blob_image_cache
    global ball
    global ghost
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
        menu_font.render("Ability/Select to view the info,", False, (0, 0, 255)),
        menu_font.render("stats, and tips and more of a blob.", False, (0, 0, 255)),
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

def blob_page_1(game_display):
    global selected_blob
    global selected_blob_image
    global selected_blob_matchups
    global selected_blob_description
    # Draw the blob itself and print its name on screen
    game_display.blit(selected_blob_image, (583, 200))
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 60)
    text_color = (0, 0, 255)
    text_array = [
        menu_font.render(selected_blob[1], False, text_color),
    ]
    text_y = 100
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

    # Print Wins, Losses and Ties
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_color = (0, 0, 255)
    wlt = []
    for i in ['wins', 'losses', 'ties']:
        if i in selected_blob_matchups:
            wlt.append(str(selected_blob_matchups[i]))
        else:
            wlt.append("0")
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 50)
    text_array = [
        menu_font.render(wlt[0] +"W-" + wlt[1] + "L-" + wlt[2] + "T", False, text_color),
    ]
    text_y = 350
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

    # Print the Blob Popup Description
    small_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
    text_array = []
    try:
        for i in selected_blob_description.split("/"):
            text_array.append(small_font.render(i, False, text_color))
    except:
        pass

    text_y = 525
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 50

    # Print Basic Blob Stats
    hp_star = {
        1: "Frail",
        2: "Weak",
        3: "Average",
        4: "Sturdy",
        5: "Tanky"
    }

    speed_star = {
        1: 'Sluggish',
        2: 'Slow',
        3: 'Average',
        4: 'Fast',
        5: 'Hasty',
    }

    gravity_star = {
        1: 'Feather',
        2: 'Light',
        3: 'Average',
        4: 'Heavy',
        5: 'Extreme',
    }
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_array = [
        menu_font.render("HP: " + str(hp_star[selected_blob_stars['max_hp']]), False, text_color),
        menu_font.render("Speed: " + speed_star[selected_blob_stars['top_speed']], False, text_color),
        menu_font.render("Gravity: " + gravity_star[selected_blob_stars['gravity']], False, text_color),
    ]
    text_y = 100
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

def blob_page_2(game_display):
    text_color = (0, 0, 255)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_array = [
        menu_font.render("HP: " + str(selected_blob_stars['max_hp']) + "*", False, text_color),
        menu_font.render("Speed: " + str(selected_blob_stars['top_speed']) + "*", False, text_color),
        menu_font.render("Ground Traction: " + str(selected_blob_stars['traction']) + "*", False, text_color),
        menu_font.render("Air Friction: " + str(selected_blob_stars['friction']) + "*", False, text_color),
        menu_font.render("Gravity: " + str(selected_blob_stars['gravity']) + "*", False, text_color),
        menu_font.render("SA Cost: " + str(selected_blob_stars['special_ability_cost']), False, text_color),
        menu_font.render("SA Maintenance: " + str(selected_blob_stars['special_ability_maintenance']), False, text_color),
    ]
    text_y = 100
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

    text_array = [
        menu_font.render("Kick CD: " + str(selected_blob_stars['kick_cooldown_rate']) + "*", False, text_color),
        menu_font.render("Block CD: " + str(selected_blob_stars['block_cooldown_rate']) + "*", False, text_color),
        menu_font.render("Boost Cost: " + str(selected_blob_stars['boost_cost']), False, text_color),
        menu_font.render("Boost CD: " + str(selected_blob_stars['boost_cooldown_max']) + "*", False, text_color),
        menu_font.render("Boost Duration: " + str(selected_blob_stars['boost_duration']) + "*", False, text_color),
        menu_font.render("SA Delay: " + str(selected_blob_stars['special_ability_delay']), False, text_color),
        menu_font.render("SA CD: " + str(selected_blob_stars['special_ability_cooldown']), False, text_color),
    ]
    text_y = 100
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (550, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

    text_array = [
        menu_font.render("Some blob stats are measured in stars (*),", False, text_color),
        menu_font.render("which range from 1 to 5", False, text_color),
    ]
    text_y = 628
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

def blob_page_3(game_display):
    pass

def blob_page_4(game_display):
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_color = (0, 0, 255)
    text_array = [
        menu_font.render("Coming Soon!", False, text_color),
    ]
    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (400, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

def blob_page_5(game_display):
    global selected_blob_tips

    text_y = 100
    for text_box in selected_blob_tips:
        text_rect = text_box.get_rect()
        text_rect.topleft = (50, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 36

def draw_blob_page(game_display, info_getter, settings):
    blob_tab = info_getter[2]
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30)
    text_color = (0, 0, 255)
    text_array = [
        menu_font.render("Overview", False, text_color),
        menu_font.render("Blob Stats", False, text_color),
        menu_font.render("Matchups", False, text_color),
        menu_font.render("Costumes", False, text_color),
        menu_font.render("Tips", False, text_color),
        menu_font.render("Back", False, text_color),
    ]
    text_y = 76
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (1068, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 66

    ball = pg.image.load(cwd + "/resources/images/balls/soccer_ball.png")
    ball = pg.transform.scale(ball, (38, 38)) # TODO: please stop loading this every frame
    game_display.blit(ball, (1000, 76 + (66 * blob_tab)))

    page_directory = {
        0: blob_page_1,
        1: blob_page_2,
        2: blob_page_4,
        3: blob_page_4,
        4: blob_page_5,
        5: blob_page_5,
    }

    page_directory[blob_tab](game_display)



def draw_blob_info(game_display, info_getter, settings):
    draw_background(game_display, 'green_background', settings)
    selector_position = info_getter[0]
    if not selector_position[2]:
        draw_blob_selector(game_display, info_getter, settings)
    else:
        draw_blob_page(game_display, info_getter, settings)