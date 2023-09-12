'''
engine/menus/css_menu.py

File that handles the character select screen, albeit a little messily. Should be rewritten at some point.

> css_navigation(): Takes keyboard and mouse inputs to move the selectors
> css_handler(): Handles the selector position itself and updates the game state/selected blobs depending on the state of each selector.
> popup_handler(): Handles the splash screen for unlocks. Mostly it just needs to detect a click or button press to move on
'''
import math
import engine.handle_input
from engine.unlocks import load_blob_unlocks, return_blob_unlocks, return_css_selector_blobs, update_css_blobs, return_available_costumes
from engine.unlock_event import clear_unlock_events, get_unlock_events
from engine.game_handler import set_timer
from resources.graphics_engine.display_almanac import load_almanac_static_text, unload_almanac_static_text
from resources.graphics_engine.display_css import force_load_blobs
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button        
from engine.menus.css_selector import CSS_PLAYER
from engine.menus.css_blobs import CSS_BLOBS

# X position, Y position, Confirmation, CPU/Human
p1_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p2_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p1_ghost_position = None
p2_ghost_position = None
p1_blob = "quirkless"
p2_blob = "quirkless"
blob_list = return_css_selector_blobs()
blob_selection_obj = CSS_BLOBS()

player_menus = {
    1: CSS_PLAYER(1, 150, 600, blob_selection_obj),
    2: CSS_PLAYER(2, 475, 600, blob_selection_obj),
    3: CSS_PLAYER(3, 800, 600, blob_selection_obj),
    4: CSS_PLAYER(4, 1125, 600, blob_selection_obj),
}

token_list = []
for player_menu in player_menus:
    token_list.append(player_menus[player_menu].token)
player_menus[0] = CSS_PLAYER(0)

    
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
        if(player_menus[player_menu].cursor.clicking and not player_menus[player_menu].cursor.was_clicking and not player_menus[player_menu].cursor.held_token):
        # Click with empty cursor
            for token_obj in token_list:
                if(player_menus[player_menu].cursor.dist_to_element(token_obj) < 50 and not token_obj.attached_to and (token_obj.player == player_menus[player_menu].cursor.player or token_obj)):
                    token_obj.attach_to_cursor(player_menus[player_menu].cursor)
                    player_menus[player_menu].cursor.current_image = player_menus[player_menu].cursor.grab_image
                    break
            continue
        if(player_menus[player_menu].cursor.clicking and not player_menus[player_menu].cursor.was_clicking and  player_menus[player_menu].cursor.held_token):
        # Click with filled cursor
            player_menus[player_menu].cursor.held_token.detach_from_cursor()
            player_menus[player_menu].cursor.current_image = player_menus[player_menu].cursor.idle_image
            continue
    mouse = engine.handle_input.handle_mouse()
    mouse_pos = mouse[0]
    mouse_pressed = mouse[1]
    mouse_pick_up = False
    if((mouse_pressed[0] or mouse_pressed[1] or mouse_pressed[2]) and not player_menus[0].cursor.held_token):
        for token_obj in token_list:
            #print(math.dist(mouse_pos, [token_obj.x_pos, token_obj.y_pos]))
            if(math.dist(mouse_pos, [token_obj.x_pos, token_obj.y_pos]) < 50 and not token_obj.attached_to):
                token_obj.attach_to_cursor(player_menus[0].cursor)
                mouse_pick_up = True
                break
    if((mouse_pressed[0] or mouse_pressed[1] or mouse_pressed[2]) and player_menus[0].cursor.held_token and not mouse_pick_up):
        #print()
        player_menus[0].cursor.held_token.detach_from_cursor()
    player_menus[0].cursor.follow_mouse(mouse_pos)
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