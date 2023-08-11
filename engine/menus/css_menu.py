'''
engine/menus/css_menu.py

File that handles the character select screen, albeit a little messily. Should be rewritten at some point.

> css_navigation(): Takes keyboard and mouse inputs to move the selectors
> css_handler(): Handles the selector position itself and updates the game state/selected blobs depending on the state of each selector.
> popup_handler(): Handles the splash screen for unlocks. Mostly it just needs to detect a click or button press to move on
'''

import engine.handle_input
from engine.unlocks import load_blob_unlocks, return_blob_unlocks, return_css_selector_blobs, update_css_blobs, return_available_costumes
from engine.unlock_event import clear_unlock_events, get_unlock_events
from engine.game_handler import set_timer
from resources.graphics_engine.display_almanac import load_almanac_static_text, unload_almanac_static_text
from resources.graphics_engine.display_css import force_load_blobs
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button        
from engine.menus.css_selector import CSS_PLAYER

# X position, Y position, Confirmation, CPU/Human
p1_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p2_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p1_ghost_position = None
p2_ghost_position = None
p1_blob = "quirkless"
p2_blob = "quirkless"

player_menus = {
    1: CSS_PLAYER(1)
}

blob_list = return_css_selector_blobs()

    
p1_timer = 0
p2_timer = 0
def css_handler():
    '''
    
    '''

    # Import globals
    global player_menus
    game_state = "css"

    # TODO: We need to refactor the things below to get 3 and 4 player support to work

    # Navigate through the CSS 
    # TODO: Verify below
    # Controller failure - cannot swap players here
    pressed = engine.handle_input.get_keypress()
    for player_menu in player_menus:
        player_menus[player_menu].cursor.player_interaction(pressed)

    return game_state, [player_menus]

unlock_counter = 0
def unlock_splash_handler(timer):
    '''
    # TODO: Standardize return!
    Handles the splash screen for unlocks. Mostly it just needs to detect a click or button press to move on

    Inputs:
        - timer [int]: Prevents the player from skipping the unlockables too quickly!
        - unlock_counter [int] (global): The current unlock we're looking at
        - blob_list [array] (global): A 2D array of strings that lets us know which blob we're selecting
        - get_unlock_events [array]: A function call which looks at what unlocks we got from this particular game

    Outputs:
        - game_state [string]: The updated game state. Defaults to "unlock_splash"
        - unlock_splash: An UnlockEvent class item containing important things like the unlock's name and description
    '''
    global unlock_counter
    global blob_list
    game_state = "unlock_splash"
    if(unlock_counter >= len(get_unlock_events())):
        unlock_counter = 0
        last_info = get_unlock_events()[-1].info
        clear_unlock_events()
        blob_list = return_css_selector_blobs()
        return "css", last_info
    
    unlock_splash = get_unlock_events()[unlock_counter].info
    
    pressed = engine.handle_input.get_keypress()
    mouse = engine.handle_input.handle_mouse()

    if("p1_ability" in pressed or "p2_ability" in pressed or "return" in pressed or mouse[1][0] or mouse[1][2]) and timer <= 0:
        unlock_counter += 1
        set_timer(60)
        if(unlock_counter < len(get_unlock_events())):
            createSFXEvent("chime_milestone")

    return game_state, unlock_splash