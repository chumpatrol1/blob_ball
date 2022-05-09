from resources.graphics_engine.background_handler import draw_background as draw_background
from resources.graphics_engine.display_controller_pop_up import controller_popup_queue
from engine.handle_input import return_mapkey_names
import pygame as pg
from os import getcwd
cwd = getcwd()
blob_cwd = cwd + "/resources/images/blobs/"

old_pop_up = None
pop_up_image = None
pop_up_timer = 0

def draw_pop_up(game_display, info_getter, settings):
    draw_background(game_display, 'green_background', settings)
    global old_pop_up
    global pop_up_image
    global pop_up_timer
    if(pop_up_timer):
        pop_up_timer -= 1

    if not(old_pop_up == info_getter):
        old_pop_up = info_getter
        pop_up_timer = 2
    
    if(pop_up_timer == 1):
        pop_up_image = pg.image.load(blob_cwd+info_getter[0]).convert_alpha()

    if(pop_up_image is not None):
        game_display.blit(pop_up_image, (683 - pop_up_image.get_width()//2, 250 - pop_up_image.get_height()//2))

    big_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 80)
    text_color = (0, 0, 255)
    menu_text = "" 
    if(info_getter is not None):
        temp_dict = {
            0: "Blob Unlocked!",
            2: "Costume Unlocked!"
        }
        menu_text = temp_dict[info_getter[3]]

    menu_text = big_font.render(menu_text, False, text_color)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (683, 100)
    game_display.blit(menu_text, menu_rect)

    menu_text = ""
    if(info_getter is not None):
        menu_text = info_getter[1]
    menu_text = big_font.render(menu_text, False, text_color)
    menu_rect = menu_text.get_rect()
    menu_rect.center = (683, 450)
    game_display.blit(menu_text, menu_rect)

    small_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 40)
    text_array = []
    try:
        for i in info_getter[2].split("/"):
            text_array.append(small_font.render(i, False, text_color))
    except:
        pass

    text_y = 525
    for text_box in text_array:
        text_rect = text_box.get_rect()
        text_rect.center = (683, text_y)
        game_display.blit(text_box, text_rect)
        text_y += 50

def create_generic_popup(pop_up):
    pop_up_surface = pg.Surface((450, 200), pg.SRCALPHA)
    pop_up_surface2 = pg.Surface((450, 200), pg.SRCALPHA)
    pg.draw.rect(pop_up_surface, (150, 150, 0), (0, 0, 450, 200), border_top_left_radius = 20, border_top_right_radius=20, border_bottom_left_radius=20, border_bottom_right_radius=20)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    if(pop_up.entry.event_id == 0):
        text_array = [
            menu_font.render("", False, (0, 0, 0)),
            menu_font.render("Failed to Load Replay", False, (0, 0, 0)),
            menu_font.render("(Incompatible Version)", False, (0, 0, 0)),
        ]
        text_y = 10
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50

    pop_up_surface.set_alpha(10)
    pop_up_surface2.set_alpha(10)
    pop_up.surface = pop_up_surface
    pop_up.surface2 = pop_up_surface2

def create_controller_popup(pop_up):
    pop_up_surface = pg.Surface((450, 200), pg.SRCALPHA)
    pop_up_surface2 = pg.Surface((450, 200), pg.SRCALPHA)
    pg.draw.rect(pop_up_surface, (150, 150, 0), (0, 0, 450, 200), border_top_left_radius = 20, border_top_right_radius=20, border_bottom_left_radius=20, border_bottom_right_radius=20)
    menu_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 20)
    if(pop_up.entry.event_id == -1):
        text_array = [
            menu_font.render("Disconnected Controller " + str(pop_up.entry.controller_number), False, (0, 0, 0)),
            menu_font.render("Type: " + str(pop_up.entry.controller_name), False, (0, 0, 0)),
            menu_font.render("from Blob Ball!", False, (0, 0, 0)),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 0):
        text_array = [
            menu_font.render("Controller " + str(pop_up.entry.controller_number) + " Connected!", False, (0, 0, 0)),
            menu_font.render("Type: " + str(pop_up.entry.controller_name), False, (0, 0, 0)),
            menu_font.render("Press DPad Left/Right to bind", False, (0, 0, 0)),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 1):
        text_color = (255, 0, 0)
        text_array = [
            menu_font.render("", False, text_color),
            menu_font.render("Successfully Assigned " + str(pop_up.entry.controller_number), False, text_color),
            menu_font.render("to Player 1!", False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 2):
        text_color = (0, 0, 255)
        text_array = [
            menu_font.render("", False, text_color),
            menu_font.render("Successfully Assigned " + str(pop_up.entry.controller_number), False, text_color),
            menu_font.render("to Player 2!", False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 3):
        text_color = (255, 0, 0)
        text_array = [
            menu_font.render("", False, text_color),
            menu_font.render("Successfully Reassigned " + str(pop_up.entry.controller_number), False, text_color),
            menu_font.render("to Player 1!", False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 4):
        text_color = (0, 0, 255)
        text_array = [
            menu_font.render("", False, text_color),
            menu_font.render("Successfully Reassigned " + str(pop_up.entry.controller_number), False, text_color),
            menu_font.render("to Player 2!", False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 5):
        text_color = (255, 0, 0)
        text_array = [
            menu_font.render("Successfully Replaced", False, text_color),
            menu_font.render("Player 1's Controller with", False, text_color),
            menu_font.render("Controller " + str(pop_up.entry.controller_number), False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 6):
        text_color = (0, 0, 255)
        text_array = [
            menu_font.render("Successfully Replaced", False, text_color),
            menu_font.render("Player 2's Controller with", False, text_color),
            menu_font.render("Controller " + str(pop_up.entry.controller_number), False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 7):
        text_color = (255, 0, 0)
        text_array = [
            menu_font.render("Successfully Unbound", False, text_color),
            menu_font.render("Controller " + str(pop_up.entry.controller_number), False, text_color),
            menu_font.render("from Player 1", False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id == 8):
        text_color = (0, 0, 255)
        text_array = [
            menu_font.render("Successfully Unbound", False, text_color),
            menu_font.render("Controller " + str(pop_up.entry.controller_number), False, text_color),
            menu_font.render("from Player 2", False, text_color),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    elif(pop_up.entry.event_id >= 10):
        text_array = [
            menu_font.render("Successfully Swapped", False, (0, 0, 0)),
            menu_font.render("Controllers " + str(pop_up.entry.controller_number) + " and " + str(pop_up.entry.event_id - pop_up.entry.controller_number - 10), False, (0, 0, 0)),
            menu_font.render("from Player 1", False, (0, 0, 0)),
        ]
        text_y = 25
        for text_box in text_array:
            text_rect = text_box.get_rect()
            text_rect.midtop = (225, text_y)
            pop_up_surface2.blit(text_box, text_rect)
            text_y += 50
    pop_up_surface.set_alpha(10)
    pop_up_surface2.set_alpha(10)
    pop_up.surface = pop_up_surface
    pop_up.surface2 = pop_up_surface2

def process_controller_popups(game_display):
    pop_up = controller_popup_queue.process()
    if(pop_up is None):
        return
    if(pop_up.surface is None):
        if(pop_up.entry.pop_type == "Controller"):
            create_controller_popup(pop_up)
        else:
            create_generic_popup(pop_up)
    if(pop_up.timer < 20):
        pop_up.surface.set_alpha(200 * pop_up.timer/20)
    if(pop_up.fade_in >= 0):
        pop_up.surface.set_alpha(200 * (8 - pop_up.fade_in)/8)
    game_display.blit(pop_up.surface, (891, 518))
    if(pop_up.surface2 is not None):
        if(pop_up.timer < 20):
            pop_up.surface2.set_alpha(255 * pop_up.timer/20)
        if(pop_up.fade_in >= 0):
            pop_up.surface2.set_alpha(255 * (8 - pop_up.fade_in)/8)
        game_display.blit(pop_up.surface2, (891, 518))
    # Then game_display.blit