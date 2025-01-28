'''
engine/menus/almanac_menu.py

File that handles the almanac menu and many submenus

> prompt_file(): Creates a Tkinter file dialog and opens a replay. Cleans up when finished
> almanac_navigation(): Handles the "top level" of the almanac menu
> almanac_stats_navigation_1(): Handles the first page of the "Game Statistics" submenu (Match Statistics)
> almanac_stats_navigation_2(): Handles the second page of the "Game Statistics" submenu (General Statistics)
> almanac_stats_navigation_3(): Handles the third page of the "Game Statistics" submenu (Matchup Chart)
> almanac_art_navigation(): Handles the art submenu of the almanac.
> almanac_art_backgrounds_navigation(): Handles the background reel in the art submenu of the almanac.
> almanac_art_blobs_navigation(): Handles the blob reel in the art submenu of the almanac.
> credits_navigation(): Handles the credits screen of the almanac
'''

import engine.handle_input
from engine.replays import decompress_replay_file, return_replay_info
from resources.graphics_engine.display_controller_pop_up import create_generic_pop_up
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button
from os import getenv
import tkinter
import tkinter.filedialog

def prompt_file():
    '''
    Creates a Tkinter file dialog and opens a replay. Cleans up when finished. Called by almanac_navigation.

    Output:
        - file_name [str]: The path to a specified replay that we have selected
    '''
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top, title = "Open Blob Ball Replay", filetypes=[("Blob Ball Replay Files", ".bbr")], initialdir=getenv('APPDATA')+"/BlobBall"+"/replays")
    top.destroy()
    return file_name

selector_position = 0
almanac_main_buttons = [
    Button(50, 110, 400, 950),
    Button(125, 185, 400, 950),
    Button(200, 260, 400, 950),
    Button(275, 335, 400, 950),
    Button(350, 410, 400, 950),
    Button(425, 500, 400, 950),
]
def almanac_navigation(timer, previous_screen, ruleset):
    '''
    TODO: Standardize return!
    Handles the "top level" of the almanac menu. This can be accessed from the main menu or the character select screen

    Inputs:
        - timer [int]: A lockout timer which prevents menus from navigating too quickly
        - previous_screen [str]: A string representing the game_state we previously came from, either "main_menu" or "css"
        - ruleset [dict]: A dictionary. We pull the game version from here - if the replay version is not the same as the ruleset version we won't open the file
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.

    Outputs:
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.
        - game_state [str]: The updated game state. Defaults to "almanac"
    '''
    game_state = "almanac"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 5
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 5:
            selector_position = 0
        else:
            selector_position += 1

    def update_gamestate():
        '''
        Updates the game state when we detect a click or button press.

        Inputs:
            - selector_position [int] (global): The position of the selector, ranging from 0-5
        
        Outputs:
            - game_state [str]: The updated game state. Game will crash if selector position is not an int between 0-5 inclusive.
        '''
        global selector_position
        createSFXEvent('select')
        if(selector_position == 0): #Blobs
            game_state = "blob_info"
        elif(selector_position == 1):
            game_state = "almanac"
            replay_file = prompt_file()
            
            if(replay_file != ""):
                decompress_replay_file(replay_file)
                if(return_replay_info()[1]["version"] == ruleset['version']):
                    game_state = "replay_match"
                else:
                    create_generic_pop_up(0)
                

            selector_position = 1
            # Will be temporarily disabled
        elif(selector_position == 2):
            game_state = "almanac_stats"
        elif(selector_position == 3):
            selector_position = 0
            game_state = "almanac_art"
        elif(selector_position == 4):
            game_state = "credits"
        elif(selector_position == 5): #Go back
            game_state = previous_screen
            selector_position = 0
        return game_state

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        game_state = update_gamestate()
            
    for i in range(len(almanac_main_buttons)):
        if(almanac_main_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0] or mouse[1][2]):
                createSFXEvent('select')
                game_state = update_gamestate()
                
    return selector_position, game_state

def almanac_stats_navigation_1(timer):
    '''
    # TODO: Standardize return!
    Handles the first page of the "Game Statistics" submenu (Match Statistics)

    Inputs:
        - timer [int]: A lockout timer which prevents menus from navigating too quickly
    
    Outputs:
        - game_state [str]: The updated game state. Defaults to "almanac_stats"
    '''
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "almanac_stats"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed or mouse[1][0] or mouse[1][2]):
        createSFXEvent('select')
        game_state = "almanac_stats_page_2"
    return [game_state]

def almanac_stats_navigation_2(timer):
    '''
    # TODO: Standardize return!
    Handles the first page of the "Game Statistics" submenu (General Statistics)

    Inputs:
        - timer [int]: A lockout timer which prevents menus from navigating too quickly
    
    Outputs:
        - game_state [str]: The updated game state. Defaults to "almanac_stats_page_2"
    '''
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "almanac_stats_page_2"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed or mouse[1][0] or mouse[1][2]):
        createSFXEvent('select')
        game_state = "almanac_stats_page_3"
        global p1_selector_position
        p1_selector_position = [3, 2, 0, 0]
    return [game_state]

almanac_mu_chart_selector = [3, 2, 0]
almanac_mu_chart_ghost = None
almanac_mu_chart_buttons = []
for i in range(9): # 9 columns
    for j in range(3): # 3 rows
        almanac_mu_chart_buttons.append(Button(25+120*j, 125+120*j, 75 + i*137, 220 + i*137)) # Left half of slot is for P1
        

def almanac_stats_navigation_3():
    '''
    Handles the first page of the "Game Statistics" submenu (Matchup Chart)

    Inputs:
        - almanac_mu_chart_selector [array]: Array of ints - first one is x pos, second is y pos, third is whether or not we selected the blob
        - almanac_mu_chart_ghost [array]: Array of ints - first one is x pos, second is y pos, third is whether or not we selected the blob. Ghost is used for mouse hovering
    
    Outputs:
        - game_state [str]: The updated game state. Defaults to "almanac_stats_page_3"
        - info_getter [array]
            - almanac_mu_chart_selector [array]: 
            - almanac_mu_chart_ghost [array]:
    '''
    global almanac_mu_chart_selector
    game_state = "almanac_stats_page_3"
    pressed = engine.handle_input.css_input()
    pressed = engine.handle_input.merge_inputs(pressed)
    mouse = engine.handle_input.handle_mouse()
    global almanac_mu_chart_ghost

    if('up' in pressed):
            if almanac_mu_chart_selector[1] == 0:
                almanac_mu_chart_selector[1] = 2
                
            else:
                almanac_mu_chart_selector[1] -= 1
    elif('down' in pressed):
            if almanac_mu_chart_selector[1] == 2:
                almanac_mu_chart_selector[1] = 0
            else:
                almanac_mu_chart_selector[1] += 1
    if('left' in pressed):
        if almanac_mu_chart_selector[0] == 0:
            almanac_mu_chart_selector[0] = 8
        else:
            almanac_mu_chart_selector[0] -= 1
    elif('right' in pressed):
        if almanac_mu_chart_selector[0] == 8:
            almanac_mu_chart_selector[0] = 0
        else:
            almanac_mu_chart_selector[0] += 1
    
    if(almanac_mu_chart_selector[2] == 0):
        if('ability' in pressed or 'return' in pressed):
            if(almanac_mu_chart_selector == [4, 1, 0]):
                createSFXEvent('select')
                game_state = "almanac"
            else:
                almanac_mu_chart_selector[2] = 1
    if(almanac_mu_chart_selector[2] == 1 and 
    ('up' in pressed or 'down' in pressed or 'left' in pressed or 'right' in pressed)):
        almanac_mu_chart_selector[2] = 0
    if('kick' in pressed):
        almanac_mu_chart_selector[2] = 0

    for i in range(len(almanac_mu_chart_buttons)):
        if(almanac_mu_chart_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                
                almanac_mu_chart_ghost = [i//3, i%3] # Change the selector position

            if(mouse[1][0]):
                # Functionality:
                # both unselected: set to select
                # me select, other unselect: nothing
                # me unselect, other select: set to select
                # both select: both confirm
                createSFXEvent('select')
                almanac_mu_chart_selector = [i//3, i%3, 1]
                if(almanac_mu_chart_selector[:2] == [4, 1]):
                    game_state = "almanac"
                    almanac_mu_chart_ghost = None
                    almanac_mu_chart_selector[2] = 0
                
            elif(mouse[1][2]):
                almanac_mu_chart_selector[2] = 0

    return game_state, [almanac_mu_chart_selector, almanac_mu_chart_ghost]

almanac_art_buttons = list(almanac_main_buttons)

def almanac_art_navigation(timer):
    '''
    # TODO: Standardize return!
    Handles the art submenu of the almanac.

    Inputs:
        - timer [int]: A lockout timer which prevents menus from navigating too quickly
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.

    Outputs:
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.
        - game_state [str]: The updated game state. Defaults to "almanac_art"
    '''
    game_state = "almanac_art"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 5
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 5:
            selector_position = 0
        else:
            selector_position += 1

    def update_gamestate():
        global selector_position
        if(selector_position == 5): #Casual
            game_state = "almanac"
            selector_position = 3
        elif(selector_position == 0):
            game_state = "almanac_art_backgrounds"
        elif(selector_position == 1):
            selector_position = 0
            game_state = "almanac_art_blobs"
        else:
            game_state = "almanac_art"
        return game_state

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        game_state = update_gamestate()
            
    for i in range(len(almanac_main_buttons)):
        if(almanac_main_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0] or mouse[1][2]):
                createSFXEvent('select')
                game_state = update_gamestate()

    return selector_position, game_state

def almanac_art_backgrounds_navigation(timer):
    '''
    # TODO: Standardize return!
    Handles the background reel in the art submenu of the almanac.

    Inputs:
        - timer [int]: A lockout timer which prevents menus from navigating too quickly
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.

    Outputs:
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.
        - game_state [str]: The updated game state. Defaults to "almanac_art_backgrounds"
    '''
    game_state = "almanac_art_backgrounds"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 6
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed or mouse[1][0]):
        if selector_position == 6:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p1_kick' in pressed or 'p2_ability' in pressed or 'p2_kick' in pressed or 'return' in pressed or mouse[1][2]):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def almanac_art_blobs_navigation(timer):
    '''
    # TODO: Standardize return!
    Handles the blob reel in the art submenu of the almanac.

    Inputs:
        - timer [int]: A lockout timer which prevents menus from navigating too quickly
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.

    Outputs:
        - selector_position [int] (global): Represents the position of the selector, and ranges from 0 to 5.
        - game_state [str]: The updated game state. Defaults to "almanac_art_blobs"
    '''
    game_state = "almanac_art_blobs"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 26
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed or mouse[1][0]):
        if selector_position == 26:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p1_kick' in pressed or 'p2_ability' in pressed or 'p2_kick' in pressed or 'return' in pressed or mouse[1][2]):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def credits_navigation(timer):
    '''
    # TODO: Standardize return!
    Handles the credits screen of the almanac

    Inputs:
        - timer [int]: A lockout timer which prevents menus from navigating too quickly

    Outputs:
        - game_state [str]: The updated game state. Defaults to "credits"
    '''
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "credits"
    if(not timer) and ('p1_ability' in pressed or 'p1_kick' in pressed or 'p2_ability' in pressed or 'p2_kick' in pressed or 'return' in pressed or mouse[1][0] or mouse[1][2]):
        createSFXEvent('select')
        game_state = "almanac"
    return [game_state]
