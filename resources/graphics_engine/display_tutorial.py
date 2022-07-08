from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_gameplay import draw_gameplay
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
    6: "Enemy incoming! Time your block to perform a parry./Standing on the yellow zone near your/goal increases damage taken!"
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

    draw_tutorial_text(gameplay_display, info_getter, settings)