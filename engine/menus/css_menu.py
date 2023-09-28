'''
engine/menus/css_menu.py

File that handles the character select screen, albeit a little messily. Should be rewritten at some point.

> css_navigation(): Takes keyboard and mouse inputs to move the selectors
> css_handler(): Handles the selector position itself and updates the game state/selected blobs depending on the state of each selector.
> popup_handler(): Handles the splash screen for unlocks. Mostly it just needs to detect a click or button press to move on
'''
import math
import engine.handle_input
from engine.unlocks import load_blob_unlocks, return_blob_unlocks, return_css_selector_blobs, update_css_blobs
from engine.unlock_event import clear_unlock_events, get_unlock_events
from engine.game_handler import set_timer
from resources.graphics_engine.display_almanac import load_almanac_static_text, unload_almanac_static_text
from resources.graphics_engine.display_css import force_load_blobs
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button        
from engine.menus.css_selector import CSS_PLAYER
from engine.menus.css_blobs import CSS_BLOBS

# X position, Y position, Confirmation, CPU/Human
#p1_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
#p2_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
#p1_ghost_position = None
#p2_ghost_position = None
#p1_blob = "quirkless"
#p2_blob = "quirkless"
blob_list = return_css_selector_blobs()
blob_selection_obj = CSS_BLOBS()
players_ready = 0
ui_button_timer = 0

player_menus = {
    1: CSS_PLAYER(1, 85, 525, blob_selection_obj),
    2: CSS_PLAYER(2, 412, 525, blob_selection_obj),
    3: CSS_PLAYER(3, 739, 525, blob_selection_obj),
    4: CSS_PLAYER(4, 1067, 525, blob_selection_obj),
}

token_list = []
for player_menu in player_menus:
    token_list.append(player_menus[player_menu].token)
player_menus[0] = CSS_PLAYER(0)

ui_buttons = {
    "casual_match": Button(470, 509, 0, 1366, 'disabled'),
    "main_menu": Button(0, 70, 0, 178),
    "rules": Button(0, 70, 180, 1066),
    "almanac": Button(0, 70, 1070, 1200),
    "settings": Button(0, 70, 1220, 1366),
}

def temp_disable_cursors():
    global player_menus
    for player in player_menus:
        player_menus[player].cursor.clicking = True
        player_menus[player].cursor.was_clicking = True    

def css_handler():
    '''
    
    '''

    # Import globals
    global player_menus
    global players_ready
    global ui_button_timer
    game_state = "css"
    if(ui_button_timer):
        ui_button_timer -= 1
    # TODO: We need to refactor the things below to get 3 and 4 player support to work

    # Navigate through the CSS 
    # TODO: Verify below
    # Controller failure - cannot swap players here
    pressed = engine.handle_input.get_keypress()
    
    for player_menu in player_menus:
        player_menus[player_menu].cursor.player_interaction(pressed)
        player_menus[player_menu].cursor.called_detach_from_cursor = False
        if(player_menus[player_menu].cursor.clicking and not player_menus[player_menu].cursor.was_clicking and not player_menus[player_menu].cursor.held_token):
        # Click with empty cursor
            for token_obj in token_list:
                if(player_menus[player_menu].cursor.dist_to_element(token_obj) < 50 and not token_obj.attached_to and (token_obj.player == player_menus[player_menu].cursor.player or token_obj)):
                    token_obj.attach_to_cursor(player_menus[player_menu].cursor)
                    player_menus[player_menu].cursor.current_image = player_menus[player_menu].cursor.grab_image
                    player_menus[player_menu].cursor.called_detach_from_cursor = True
                    break
            else:
                if(player_menus[player_menu].menu.x_pos <= player_menus[player_menu].cursor.x_pos <= player_menus[player_menu].menu.x_pos + 217 and player_menus[player_menu].menu.y_pos <= player_menus[player_menu].cursor.y_pos <= player_menus[player_menu].menu.y_pos + 200 and player_menus[player_menu].token.current_blob):
                    player_menus[player_menu].token.update_selected_costume()
            continue
            
        if(player_menus[player_menu].cursor.clicking and not player_menus[player_menu].cursor.was_clicking and  player_menus[player_menu].cursor.held_token):
        # Click with filled cursor
            player_menus[player_menu].cursor.held_token.detach_from_cursor()
            player_menus[player_menu].cursor.current_image = player_menus[player_menu].cursor.idle_image
            player_menus[player_menu].cursor.called_detach_from_cursor = True
            continue
    mouse = engine.handle_input.handle_mouse()
    mouse_pos = mouse[0]
    mouse_pressed = mouse[1]
    mouse_pick_up = False
    player_menus[0].cursor.was_clicking = player_menus[0].cursor.clicking
    if((mouse_pressed[0] or mouse_pressed[1] or mouse_pressed[2]) and not player_menus[0].cursor.held_token):
        player_menus[0].cursor.clicking = True
        
        for token_obj in token_list:
            #print(math.dist(mouse_pos, [token_obj.x_pos, token_obj.y_pos]))
            if(math.dist(mouse_pos, [token_obj.x_pos, token_obj.y_pos]) < 50 and not token_obj.attached_to):
                token_obj.attach_to_cursor(player_menus[0].cursor)
                mouse_pick_up = True
                player_menus[0].cursor.called_detach_from_cursor = True
                break
    else:
        player_menus[0].cursor.clicking = False
    if((mouse_pressed[0] or mouse_pressed[1] or mouse_pressed[2]) and player_menus[0].cursor.held_token and not mouse_pick_up):
        #print()
        player_menus[0].cursor.held_token.detach_from_cursor()
        player_menus[0].cursor.called_detach_from_cursor = True
    player_menus[0].cursor.follow_mouse(mouse_pos)
    players_ready = 0

    for token_obj in token_list:
        players_ready += bool(token_obj.current_blob and not token_obj.attached_to)
    
    for player_menu in player_menus:
        player_menus[player_menu].token.check_costume_toggle(pressed)
        player_menus[player_menu].token.costume_toggle_cooldown(pressed)

        
    if(players_ready >= 2):
        ui_buttons["casual_match"].state = "idle"
    else:
        ui_buttons["casual_match"].state = "disabled"
    
    for ui_button_key in ui_buttons:
        ui_button = ui_buttons[ui_button_key]
        button_override = False
        hover_lock = False
        if(ui_button.check_button_enabled()):
            for player_menu in player_menus:
                player_cursor = player_menus[player_menu].cursor
                cursor_pos = [[player_cursor.x_pos, player_cursor.y_pos], [player_cursor.clicking, player_cursor.clicking, player_cursor.clicking]]
                if(ui_button.check_hover(cursor_pos, True)):
                    hover_lock = True
                if(ui_button.check_hover(cursor_pos, button_override) and ui_button.check_left_click(cursor_pos) and not player_cursor.was_clicking and not ui_button_timer and not player_cursor.held_token and not player_cursor.called_detach_from_cursor):
                    print(player_cursor.called_detach_from_cursor)
                    game_state = ui_button_key
                    ui_button_timer = 20
                    button_override = True
                    temp_disable_cursors()
                #print(ui_button_key, ui_button.check_hover(cursor_pos, button_override), ui_button.state)
            ui_button.state = 'hover' if hover_lock else 'idle'

    return game_state, [player_menus, players_ready, ui_buttons]

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