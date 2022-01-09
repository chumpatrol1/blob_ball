import engine.handle_input
import engine.popup_event
from resources.sound_engine.sfx_event import createSFXEvent

p1_ready = False
p2_ready = False
flash = 90

def updateFlash():
    global flash
    flash -= 1
    if(flash == 0):
        flash = 90
    return flash

def reset_ready():
    global p1_ready
    global p2_ready
    p1_ready = False
    p2_ready = False

def handle_win_screen(game_stats):
    global p1_ready
    global p2_ready
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "casual_win"

    if('p1_ability' in pressed):
        p1_ready = True
    elif('p1_kick' in pressed):
        p1_ready = False
    
    if('p2_ability' in pressed):
        p2_ready = True
    if('p2_kick' in pressed):
        p2_ready = False

    if('return' in pressed or mouse[1][0]):
        p1_ready = True
        p2_ready = True
    elif(mouse[1][2]):
        p1_ready = False
        p2_ready = False
    
    if(p1_ready and p2_ready):
        game_state = "css"
        if not (engine.popup_event.get_pop_up_events() == []):
            createSFXEvent("chime_milestone")
            game_state = "pop_up"

    flash = updateFlash()


    info_getter = [p1_ready, p2_ready, flash, game_stats]

    return game_state, info_getter