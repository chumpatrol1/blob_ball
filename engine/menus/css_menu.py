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

p1_css_menu_buttons = [
]
p2_css_menu_buttons = [
]
for i in range(8): # 8 columns
    for j in range(5): # 5 rows
        p1_css_menu_buttons.append(Button(50+100*j, 150+100*j, 136 + i*136, 204 + i*136)) # Left half of slot is for P1
        p2_css_menu_buttons.append(Button(50+100*j, 150+100*j, 204 + i*136, 272 + i*136)) # Right half of slot is for P2
        


# X position, Y position, Confirmation, CPU/Human
p1_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p2_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p1_ghost_position = None
p2_ghost_position = None
p1_blob = "quirkless"
p2_blob = "quirkless"

blob_list = return_css_selector_blobs()

def css_navigation(player, selector, timer, other_selector, ghost_selector, other_ghost):
    '''
    Takes keyboard and mouse inputs to move the selectors

    Inputs:
        - player [int]: The player's number passed. Primarily used to prevent controllers from being detected twice in a frame
        - selector [array]: Array with 3 elements indicating position and selection status
        - timer [int]: The player's timer, which prevents the selectors from moving too quickly
        - other_selector [array]: Same as selector, but for the other player
        - ghost_selector [array]: Array with 2 elements for using with mouse hovering 
        - other_ghost: Same as ghost_selector, but for the other player

    Ouputs
        - selector [array]: Array with 3 elements indicating position and selection status
        - timer [int]: The player's timer, which prevents the selectors from moving too quickly
        - other_selector [array]: Same as selector, but for the other player
        - ghost_selector [array]: Array with 2 elements for using with mouse hovering 
        - other_ghost: Same as ghost_selector, but for the other player
    '''
    
    # Convert player controls
    pressed_conversions = engine.handle_input.player_to_controls(player)
    detect_new_controllers = True
    if(player == 2):
        detect_new_controllers = False
    pressed_buttons = engine.handle_input.css_input(detect_new_controllers = detect_new_controllers)
    if(player == 1):
        mouse = engine.handle_input.handle_mouse(False)
        cur_blob = p1_blob
    else:
        mouse = engine.handle_input.handle_mouse()
        cur_blob = p2_blob

    pressed = []
    override = {'return', 'escape'}
    for button in pressed_buttons:
        if(button in pressed_conversions):
            pressed.append(pressed_conversions[button])
        elif(button in override):
            pressed.append(button)
    if pressed == []:
        timer = 0

    if not timer == 0:
        pressed = []
        
    if not (pressed == []):
        if('ability' in pressed or 'escape' in pressed):
            timer = 15
        else:
            timer = 30
    
    
    if(selector[2] == 0):
        if('up' in pressed):
            selector[4] = 0
            if selector[1] == 0:
                selector[1] = 4
            else:
                selector[1] -= 1
            
        elif('down' in pressed):
            selector[4] = 0
            if selector[1] == 4:
                selector[1] = 0
            else:
                selector[1] += 1
        if('left' in pressed):
            selector[4] = 0
            if selector[0] == 0:
                selector[0] = 7
            else:
                selector[0] -= 1
        elif('right' in pressed):
            selector[4] = 0
            if selector[0] == 7:
                selector[0] = 0
            else:
                selector[0] += 1

    if('block' in pressed and selector[0] > 0 and not (cur_blob == 'quirkless' and selector[0] != 0 and selector[1] != 0)):
        selector[4] += 1
        costumes = return_available_costumes()
        if(selector[4] >= len(costumes[cur_blob])):
            selector[4] = 0
    
    if('return' in pressed):
        print("return pressed")

    if(selector[2] == 0):
        if('ability' in pressed):
            selector[2] = 1
            ghost_selector = None
        elif('escape' in pressed):
            if(other_selector[2] == 0 and selector[3] == 0):
                other_selector[2] = 2
                other_selector[3] = 1

    elif('kick' in pressed):
        selector[2] = 0
        if(other_selector[2] == 2):
            #Deconfirms the other player's selection if the other player has confirmed
            other_selector[2] = 1
    elif(selector[2] >= 1 and other_selector[2] >= 1):
        if('ability' in pressed):
            selector[2] = 2
            ghost_selector = None
        elif('return' in pressed or 'escape' in pressed):
            selector[2] = 2
            other_selector[2] = 2
            ghost_selector = None
    elif(selector[2] >= 1 and other_selector[2] == 0):
        if('escape' in pressed and selector[3] == 0):
            selector[2] = 2
            other_selector[2] = 2
            other_selector[3] = 1
            ghost_selector = None


    if(player == 1):
        css_menu_buttons = p1_css_menu_buttons
    else:
        css_menu_buttons = p2_css_menu_buttons

    for i in range(len(css_menu_buttons)):
        if(css_menu_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]) and selector[2] == 0: # Did we move the mouse? 
                ghost_selector = [i//5, i%5] # Change the selector position

            if(mouse[1][0]):
                # Functionality:
                # both unselected: set to select
                # me select, other unselect: nothing
                # me unselect, other select: set to select
                # both select: both confirm
                if(selector[2] >= 1 and other_selector[2] >= 1):
                    selector[2] = 2
                    other_selector[2] = 2
                    ghost_selector = None
                    other_ghost = None
                elif(not selector[2]):
                    selector[0] = i//5
                    selector[1] = i%5
                    selector[2] = 1
                    ghost_selector = None
                
            elif(mouse[1][2]):
                selector[2] = 0
                other_selector[2] = 0
                ghost_selector = None
                other_ghost = None
                
    return selector, timer, other_selector, ghost_selector, other_ghost
    
p1_timer = 0
p2_timer = 0
def css_handler():
    '''
    Handles the selector position itself and updates the game state/selected blobs depending on the state of each selector.

    Inputs:
        - p1_selector_position [array]: Array with 3 elements indicating position and selection status
        - p2_selector_position [array]: Array with 3 elements indicating position and selection status
        - p1_ghost_position [array]: Array with 2 elements used for mouse hovering
        - p2_ghost_position [array]: Array with 2 elements used for mouse hovering
        - p1_blob [string]: The player's selected blob, such as "quirkless" or "fire"
        - p2_blob [string]: The player's selected blob, such as "quirkless" or "fire"
        - p1_timer [int]: The player's timer, which prevents the selectors from moving too quickly
        - p2_timer [int]: The player's timer, which prevents the selectors from moving too quickly

    Outputs:
        - game_state [string]: The updated game state. Defaults to "css"
        - info_getter [array]
            - p1_selector_position: Array with 3 elements indicating position and selection status.
            - p2_selector_position: Array with 3 elements indicating position and selection status
            - p1_blob: The player's selected blob, such as "quirkless" or "fire"
            - p2_blob: The player's selected blob, such as "quirkless" or "fire"
            - p1_ghost_position: Array with 2 elements used for mouse hovering
            - p2_ghost_position: Array with 2 elements used for mouse hovering
    '''

    # Import globals
    global p1_selector_position
    global p2_selector_position
    global p1_ghost_position
    global p2_ghost_position
    global p1_blob
    global p2_blob
    global p1_timer
    global p2_timer
    game_state = "css"

    # TODO: We need to refactor the things below to get 3 and 4 player support to work

    # Navigate through the CSS 
    # TODO: Verify below
    # Controller failure - cannot swap players here
    p1_selector_position, p1_timer, p2_selector_position, p1_ghost_position, p2_ghost_position = css_navigation(1, p1_selector_position, p1_timer, p2_selector_position, p1_ghost_position, p2_ghost_position)
    p2_selector_position, p2_timer, p1_selector_position, p2_ghost_position, p1_ghost_position = css_navigation(2, p2_selector_position, p2_timer, p1_selector_position, p2_ghost_position, p1_ghost_position)
    
    # Depending on the selection state, do something!
    if(p1_selector_position[2] == 1):
        if(p1_selector_position[0] == 0):
            unload_almanac_static_text()
            if(p1_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0, 0, 0]
                p2_selector_position = [4, 2, 0, 0, 0]
                p1_ghost_position = None
                p2_ghost_position = None
            elif(p1_selector_position[1] == 1):
                game_state = "rules"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 2):
                game_state = "settings"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 3):
                game_state = "almanac"
                load_almanac_static_text()
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 4):
                p1_selector_position[2] = 0
                p1_selector_position[3] = not p1_selector_position[3]
    
    if(p1_selector_position[0] > 0):
        p1_blob = blob_list[p1_selector_position[1]][p1_selector_position[0]]
    
    if(p2_selector_position[2] == 1):
        if(p2_selector_position[0] == 0):
            if(p2_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0, 0, 0]
                p2_selector_position = [4, 2, 0, 0, 0]
                p1_ghost_position = None
                p2_ghost_position = None
            elif(p2_selector_position[1] == 1):
                game_state = "rules"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 2):
                game_state = "settings"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 3):
                game_state = "almanac"
                load_almanac_static_text()
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 4):
                p2_selector_position[2] = 0
                p2_selector_position[3] = not p2_selector_position[3]

            #TODO: Fix this spaghetti
    
    if(p2_selector_position[0] > 0):
        p2_blob = blob_list[p2_selector_position[1]][p2_selector_position[0]]

    # If Both players have confirmed, start the match

    if(p1_selector_position[2] == 2 and p2_selector_position[2] == 2):
        game_state = "casual_match"
        p1_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed
        p2_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed
        p1_ghost_position = None
        p2_ghost_position = None

    # Reduce player timers

    if(p1_timer > 0):
        p1_timer -= 1
    if(p2_timer > 0):
        p2_timer -= 1

    return game_state, [p1_selector_position, p2_selector_position, p1_blob, p2_blob, p1_ghost_position, p2_ghost_position]

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