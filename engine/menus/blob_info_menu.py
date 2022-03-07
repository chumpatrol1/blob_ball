from engine.button import Button
from resources.sound_engine.sfx_event import createSFXEvent
from resources.graphics_engine.display_blob_info import load_individual_blob
import engine.handle_input
selector_position = [3, 2, 0]
selector_ghost = None
ghost_tab = 0
blob_tab = 0
almanac_mu_chart_buttons = []
for i in range(7): # 7 columns
    for j in range(5): # 5 rows
        almanac_mu_chart_buttons.append(Button(25+100*j, 125+100*j, 75 + i*175, 250 + i*175)) # Left half of slot is for P1
selected_blob = "None"

blob_info_buttons = []
for i in range(6):
    blob_info_buttons.append(Button(76+66*i, 142+66*i,1050,1360))

def blob_selector_navigation(pressed, mouse): # Handles the CSS
    global selector_position
    global selector_ghost
    game_state = 'blob_info'
    if('up' in pressed):
            if selector_position[1] == 0:
                selector_position[1] = 4
                
            else:
                selector_position[1] -= 1
    elif('down' in pressed):
            if selector_position[1] == 4:
                selector_position[1] = 0
            else:
                selector_position[1] += 1
    if('left' in pressed):
        if selector_position[0] == 0:
            selector_position[0] = 6
        else:
            selector_position[0] -= 1
    elif('right' in pressed):
        if selector_position[0] == 6:
            selector_position[0] = 0
        else:
            selector_position[0] += 1

    if(selector_position[2] == 0):
        if('ability' in pressed):
            if(selector_position == [3, 2, 0]):
                createSFXEvent('select')
                game_state = "almanac"
            else:
                createSFXEvent('select')
                load_individual_blob(selector_position)
                selector_position[2] = 1
                
    if(selector_position[2] == 1 and 
    ('up' in pressed or 'down' in pressed or 'left' in pressed or 'right' in pressed)):
        selector_position[2] = 0
    if('kick' in pressed):
        selector_position[2] = 0

    for i in range(len(almanac_mu_chart_buttons)):
        if(almanac_mu_chart_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                
                selector_ghost = [i//5, i%5] # Change the selector position

            if(mouse[1][0]):
                # Functionality:
                # both unselected: set to select
                # me select, other unselect: nothing
                # me unselect, other select: set to select
                # both select: both confirm
                createSFXEvent('select')
                selector_position = [i//5, i%5, 1]
                if(selector_position[:2] == [3, 2]):
                    game_state = "almanac"
                    selector_ghost = None
                    selector_position[2] = 0
                else:
                    load_individual_blob(selector_position)
                
            elif(mouse[1][2]):
                selector_position[2] = 0
    
    return game_state

def blob_info_navigation(pressed, mouse): # Handles individual blob selection
    global selector_position
    global blob_tab
    global ghost_tab

    if('up' in pressed):
        ghost_tab -= 1
        if(ghost_tab < 0):
            ghost_tab = 5
    elif('down' in pressed):
        ghost_tab += 1
        if(ghost_tab > 5):
            ghost_tab = 0
    elif('ability' in pressed):
        blob_tab = ghost_tab

    for i in range(len(blob_info_buttons)):
        if(blob_info_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                ghost_tab = i # Change the selector position

            if(mouse[1][0] or mouse[1][2]):
                createSFXEvent('select')
                blob_tab = ghost_tab

    if(blob_tab == 5): # Back
        selector_position[2] = 0
        blob_tab = 0
        ghost_tab = 0

    # Overview (WLT, Popup Description, HP, Speed (Sluggish, Slow, Average, Fast, Hasty), Gravity (Feather, Light, Average, Heavy, Extreme))
    # Blob Stats
    # MU Spread
    # Unlocked Costumes
    # Tips
    # Back


def general_navigation(): # Handles everything
    global selector_position
    game_state = 'blob_info'

    pressed = engine.handle_input.css_input()
    pressed = engine.handle_input.merge_inputs(pressed)
    mouse = engine.handle_input.handle_mouse()
    global selector_ghost

    if(selector_position[2] == 0):
        game_state = blob_selector_navigation(pressed, mouse)
    else:
        blob_info_navigation(pressed, mouse)
    
    info_getter = [selector_position, selector_ghost, blob_tab, ghost_tab]
    return game_state, info_getter