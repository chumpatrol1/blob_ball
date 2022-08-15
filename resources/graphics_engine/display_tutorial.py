from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_gameplay import draw_gameplay
from resources.graphics_engine.display_almanac import create_time_string
from os import getcwd
import pygame as pg
cwd = getcwd()

image_cache = {"initialized": False, "ui_initialized": False}

tutorial_text = {
    -1: "Welcome to Blob Ball, the funnest game around!",
    0: "Initializing... please wait!",
    1: "Press Left or Right to move sideways!/Push the ball into the opposing/goal to score a point!",
    2: "Press Up to jump, and hold up to go higher!/You can still move while in the air./Push the ball into the blue goal!",
    3: "There's an invisible wall!/You'll need to press your kick button/to hit the ball and score a goal!",
    4: "There is no ball, only an opponent!/Your kicks will do 2 damage to any nearby enemies./You can score a point by reducing enemy HP to 0!",
    5: "Press your block button to create a forcefield!/Stop the ball as it tries to fly into your goal!",
    6: "Enemy incoming! Time your block/ to perform a parry. Standing on the yellow/zone near your goal increases damage taken!",
    7: "The meter that's charging up in the UI/is your Energy Meter. You can spend it/by pressing your Boost button,/activating a speed boost!",
    8: "This enemy blob is regenerating HP!/If you kick while your speed boost/is active, you can do enough/ damage to stop the regeneration!",
    9: "Your Energy Meter charges passively/over the course of a match./You can charge it faster by/pressing and holding down!/Fill it up completely by the time limit!",
    10: "Every blob has a unique ability!/If you have enough energy, you can/press the ability button to activate it!/Stop the ball using Cop Blob's Ability!",
    11: "Some abilities need to be/held down for maximum effect./Focus your energy and push the ball/ into the goal using Wind Blob's Ability!",
    12: "The enemy blob is moving around the field!/Boxer Blob's Ability is close ranged/and has a delay, so time your/ability press carefully!"
}

loaded_text = {"page": -1, "content": [], "text_color": (0, 0, 255)}

def draw_tutorial_text(game_display, info_getter, settings):
    tutorial_font = image_cache["tutorial_font"]
    if(loaded_text["page"] != info_getter[0]):
        loaded_text["content"] = []
        loaded_text["page"] = info_getter[0]
        for i in tutorial_text[info_getter[0]].split("/"):
            loaded_text["content"].append(tutorial_font.render(i, False, loaded_text["text_color"]))
    text_y = 20
    if(settings['ui_mode']):
        text_y = 130
    
    for text_box in loaded_text["content"]:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 50

def draw_tutorial(gameplay_display, info_getter, settings):
    draw_gameplay(gameplay_display, info_getter[1], settings)

    if(not image_cache["initialized"]):
        image_cache["initialized"] = True
        image_cache["tutorial_font"] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 25)
        image_cache["big_font"] = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 50)
        image_cache["locked_blob"] = pg.transform.scale(pg.image.load(cwd + "/resources/images/blobs/locked_blob.png").convert_alpha(), (100, 55))
        image_cache["cpu_icon"] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/cpu_icon.png").convert_alpha(), (100, 100))
        image_cache["almanac_icon"] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/almanac_icon.png").convert_alpha(), (100, 100))
        image_cache["rules_icon"] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/rules_icon.png").convert_alpha(), (100, 100))
        image_cache["gear_icon"] = pg.transform.scale(pg.image.load(cwd + "/resources/images/css_icons/gear_icon.png").convert_alpha(), (100, 100))
        
    draw_tutorial_text(gameplay_display, info_getter, settings)

def draw_tutorial_completion(game_display, info_getter, settings):
    draw_background(game_display, "green_background", settings)
    
    menu_font = image_cache['big_font']
    menu_text = menu_font.render("Tutorial Complete!", False, (0, 0, 255))
    text_rect = menu_text.get_rect()
    text_rect.center = (683, 60)
    game_display.blit(menu_text, text_rect)

    menu_font = image_cache["tutorial_font"]
    if(info_getter[0] > 45):
        menu_text = menu_font.render("PRESS ABILITY TO RETURN TO MENU", False, (0, 0, 255))
        text_rect = menu_text.get_rect()
        text_rect.center = (683, 150)
        game_display.blit(menu_text, text_rect)

    

    text_color = (0, 0, 255)
    text_array = [
        menu_font.render('Total: {}'.format(create_time_string(info_getter[1][12], smallest = ".")), False, text_color),
        menu_font.render('Stage 1: {}'.format(create_time_string(info_getter[1][1], smallest = ".")), False, text_color),
        menu_font.render('Stage 2: {}'.format(create_time_string(info_getter[1][2] - info_getter[1][1], smallest = ".")), False, text_color),
        menu_font.render('Stage 3: {}'.format(create_time_string(info_getter[1][3] - info_getter[1][2], smallest = ".")), False, text_color),
        menu_font.render('Stage 4: {}'.format(create_time_string(info_getter[1][4] - info_getter[1][3], smallest = ".")), False, text_color),
        menu_font.render('Stage 5: {}'.format(create_time_string(info_getter[1][5] - info_getter[1][4], smallest = ".")), False, text_color),
        menu_font.render('Stage 6: {}'.format(create_time_string(info_getter[1][6] - info_getter[1][5], smallest = ".")), False, text_color),
        menu_font.render('Stage 7: {}'.format(create_time_string(info_getter[1][7] - info_getter[1][6], smallest = ".")), False, text_color),
        menu_font.render('Stage 8: {}'.format(create_time_string(info_getter[1][8] - info_getter[1][7], smallest = ".")), False, text_color),
        menu_font.render('Stage 9: {}'.format(create_time_string(info_getter[1][9] - info_getter[1][8], smallest = ".")), False, text_color),
        menu_font.render('Stage 10: {}'.format(create_time_string(info_getter[1][10] - info_getter[1][9], smallest = ".")), False, text_color),
        menu_font.render('Stage 11: {}'.format(create_time_string(info_getter[1][11] - info_getter[1][10], smallest = ".")), False, text_color),
        menu_font.render('Stage 12: {}'.format(create_time_string(info_getter[1][12] - info_getter[1][11], smallest = ".")), False, text_color),
    ]

    text_y = 200
    text_x = 50
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (text_x, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40

    text_array = [
        menu_font.render('Want to learn more? Check out the Almanac!', False, text_color),
        menu_font.render('', False, text_color),
        menu_font.render('Want to practice more?', False, text_color),
        menu_font.render('You can play against a CPU!', False, text_color),
        menu_font.render('', False, text_color),
        menu_font.render('Want to unlock more?', False, text_color),
        menu_font.render('Simply play some matches!', False, text_color),
        menu_font.render('', False, text_color),
        menu_font.render('Check out the Rules menu', False, text_color),
        menu_font.render('to change the rules of the game!', False, text_color),
        menu_font.render('', False, text_color),
        menu_font.render('Check out the Settings menu', False, text_color),
        menu_font.render('to adjust volume, controls, game', False, text_color),
        menu_font.render('appearance and much more!', False, text_color),
    ]

    text_y = 200
    text_x = 550
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.topleft = (text_x, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 40

    game_display.blit(image_cache["almanac_icon"], (425, 170))
    game_display.blit(image_cache["cpu_icon"], (425, 270))
    game_display.blit(image_cache["locked_blob"], (425, 410))
    game_display.blit(image_cache["rules_icon"], (425, 510))
    game_display.blit(image_cache["gear_icon"], (425, 650))